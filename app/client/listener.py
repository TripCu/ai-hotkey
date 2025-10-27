from __future__ import annotations

import json
import queue
import threading
import time
from dataclasses import dataclass
from typing import Optional, Tuple, Union

import requests
import pyperclip
from pyperclip import PyperclipException
from pynput import keyboard

from app.client.config import ClientConfig, load_client_config
from app.client.overlay import OverlayAppearance, show_overlay


SPECIAL_KEYS = {
    "ESC": keyboard.Key.esc,
    "ENTER": keyboard.Key.enter,
    "RETURN": keyboard.Key.enter,
    "SPACE": keyboard.Key.space,
    "TAB": keyboard.Key.tab,
    "BACKSPACE": keyboard.Key.backspace,
    "BACKSLASH": getattr(keyboard.Key, "backslash", None),
}


def _decode_token(token: str) -> str:
    try:
        return bytes(token, "utf-8").decode("unicode_escape")
    except Exception:
        return token


def parse_binding(token: str) -> Tuple[str, Union[str, keyboard.Key]]:
    token = _decode_token((token or "").strip())
    if not token:
        raise ValueError("Key binding must not be empty")
    upper = token.upper()
    if upper in SPECIAL_KEYS and SPECIAL_KEYS[upper] is not None:
        return "special", SPECIAL_KEYS[upper]
    if upper.startswith("F") and upper[1:].isdigit():
        key_attr = upper.lower()
        binding = getattr(keyboard.Key, key_attr, None)
        if binding:
            return "special", binding
    return "char", token


def matches(binding: Tuple[str, Union[str, keyboard.Key]], key: Union[keyboard.Key, keyboard.KeyCode]) -> bool:
    kind, value = binding
    if kind == "special":
        return key == value
    if isinstance(key, keyboard.KeyCode) and key.char:
        return key.char == value
    return False


@dataclass
class PromptResult:
    response: str
    final_line: Optional[str]
    validation_status: Optional[bool]
    validation_payload: Optional[dict]

    def overlay_text(self) -> str:
        sections = [self.response.strip() or "<no response>"]
        if self.final_line:
            sections.append(self.final_line.strip())
        if self.validation_status is not None:
            status = "PASS" if self.validation_status else "FAIL"
            sections.append(f"Validator: {status}")
        return "\n\n".join(filter(None, sections)).strip()


class HotkeyClient:
    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        self.collecting = False
        self.buffer: list[str] = []
        self.queue: "queue.Queue[str]" = queue.Queue()
        self.running = True
        self.start_binding = parse_binding(config.start_key)
        self.exit_binding = parse_binding(config.exit_key)
        self.clipboard_binding = parse_binding(config.clipboard_key)
        self._session = requests.Session()
        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

    def stop(self) -> None:
        self.running = False
        try:
            self.queue.put_nowait("")
        except queue.Full:
            pass

    # Listener callbacks --------------------------------------------------

    def on_press(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> Optional[bool]:
        if matches(self.exit_binding, key):
            print("Exit key detected. Quitting listener.")
            self.stop()
            return False

        if matches(self.clipboard_binding, key):
            try:
                clip_text = (pyperclip.paste() or "").strip()
            except PyperclipException as exc:
                print(f"[client] Clipboard read failed: {exc}")
                return True
            if clip_text:
                preview = clip_text if len(clip_text) <= 80 else clip_text[:77] + "..."
                print(f"\n[client] Sending clipboard: {preview}")
                self.collecting = False
                self.buffer.clear()
                self.queue.put(clip_text)
            else:
                print("[client] Clipboard is empty; nothing to send.")
            return True

        if not self.collecting:
            if matches(self.start_binding, key):
                self.collecting = True
                self.buffer.clear()
                print("\nCapture started. Type your prompt and press Enter to send.")
            return True

        if matches(self.start_binding, key):
            return True

        if key == keyboard.Key.enter:
            text = "".join(self.buffer).strip()
            self.buffer.clear()
            self.collecting = False
            if text:
                preview = text if len(text) <= 80 else text[:77] + "..."
                print(f"\n[client] Sending prompt: {preview}")
                self.queue.put(text)
            else:
                print("Prompt was empty, ignoring.")
            return True

        if key == keyboard.Key.backspace:
            if self.buffer:
                self.buffer.pop()
            return True

        if key == keyboard.Key.space:
            self.buffer.append(" ")
            return True

        if key == keyboard.Key.tab:
            self.buffer.append("\t")
            return True

        if isinstance(key, keyboard.KeyCode) and key.char:
            self.buffer.append(key.char)
            return True

        return True

    def on_release(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> Optional[bool]:
        if not self.running:
            return False
        return True

    # Worker ---------------------------------------------------------------

    def _worker_loop(self) -> None:
        while self.running:
            try:
                prompt = self.queue.get(timeout=0.5)
            except queue.Empty:
                continue
            if not prompt:
                continue
            self._dispatch_prompt(prompt)

    def _dispatch_prompt(self, prompt: str) -> None:
        payload = {"prompt": prompt, "context": {}}
        if self.config.question_domain:
            payload["context"]["question_type"] = self.config.question_domain

        url = f"http://{self.config.host}:{self.config.port}/generate"
        headers = {"x-api-key": self.config.api_key}
        try:
            response = self._session.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            print(f"[error] Request failed: {exc}")
            return
        except json.JSONDecodeError:
            print("[error] Backend returned invalid JSON.")
            return

        result = self._parse_result(data)
        self._print_to_console(result)
        if self.config.overlay_enabled:
            self._show_overlay(result)

    def _parse_result(self, data: dict) -> PromptResult:
        final_line = data.get("final_answer")
        if final_line:
            label, _, value = final_line.partition(":")
            cleaned = value.strip() or final_line.strip()
            final_line = f"FINAL: {cleaned}" if label.lower().startswith("answer") else final_line

        return PromptResult(
            response=data.get("response", "<no response>"),
            final_line=final_line,
            validation_status=data.get("valid"),
            validation_payload=data.get("validation"),
        )

    def _print_to_console(self, result: PromptResult) -> None:
        print("\n--- Response ------------------------------------------")
        print(result.response)
        if result.final_line:
            print(result.final_line)
        if result.validation_status is not None:
            status = "PASS" if result.validation_status else "FAIL"
            print(f"Validator: {status}")
            if isinstance(result.validation_payload, dict):
                print(json.dumps(result.validation_payload, indent=2))
        print("-------------------------------------------------------\n")

    def _show_overlay(self, result: PromptResult) -> None:
        text = result.overlay_text()
        if not text:
            return
        appearance = OverlayAppearance(
            width=self.config.overlay_width,
            opacity=self.config.overlay_opacity,
            duration=self.config.overlay_duration,
        )
        show_overlay(text, appearance)


def main() -> int:
    config = load_client_config()
    print(
        "Hotkey listener ready.\n"
        f"Start key: {config.start_key} | Exit key: {config.exit_key}\n"
        "Press the start key, type your prompt, then press Enter.\n"
        "Press the exit key at any time to quit."
    )
    client = HotkeyClient(config)
    with keyboard.Listener(on_press=client.on_press, on_release=client.on_release) as listener:
        while client.running and listener.running:
            time.sleep(0.2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
