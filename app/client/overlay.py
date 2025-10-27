from __future__ import annotations

import multiprocessing
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class OverlayAppearance:
    width: int = 480
    opacity: float = 0.9
    duration: float = 15.0  # seconds; 0 disables auto-close


def _render_overlay(text: str, appearance: OverlayAppearance) -> None:
    try:
        import tkinter as tk
    except ImportError:
        print("[overlay] tkinter not available; displaying response in console only.")
        print(text)
        time.sleep(max(appearance.duration, 3.0))
        return

    root = tk.Tk()
    root.title("AI Response")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.attributes("-alpha", max(0.05, min(appearance.opacity, 1.0)))

    # Transparent background support varies; using a neutral background for stability.
    background = "#202124"
    foreground = "#f1f3f4"

    frame = tk.Frame(root, bg=background, padx=18, pady=18)
    frame.pack()

    label = tk.Label(
        frame,
        text=text,
        font=("Helvetica", 14),
        justify="left",
        wraplength=appearance.width,
        bg=background,
        fg=foreground,
    )
    label.pack()

    screen_width = root.winfo_screenwidth()
    x = max(20, screen_width - appearance.width - 80)
    y = 60
    root.geometry(f"+{x}+{y}")

    if appearance.duration > 0:
        root.after(int(appearance.duration * 1000), root.destroy)

    root.bind("<Escape>", lambda _event: root.destroy())
    root.bind("<Button-1>", lambda _event: root.destroy())

    try:
        root.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)


def show_overlay(text: str, appearance: OverlayAppearance) -> multiprocessing.Process:
    process = multiprocessing.Process(target=_render_overlay, args=(text, appearance), daemon=True)
    process.start()
    return process
