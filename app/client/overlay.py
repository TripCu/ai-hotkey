from __future__ import annotations

import multiprocessing as mp
import platform
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class OverlayAppearance:
    width: int = 480
    opacity: float = 0.9
    duration: float = 15.0  # seconds; 0 disables auto-close


def _render_overlay(text: str, appearance: OverlayAppearance) -> None:
    if platform.system().lower() == "darwin":
        if _render_overlay_macos(text, appearance):
            return
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
    background = "#ffffff"
    foreground = "#000000"

    frame = tk.Frame(root, bg=background, padx=18, pady=18)
    frame.pack(anchor="ne")

    label = tk.Label(
        frame,
        text=text,
        font=("Helvetica", 14),
        justify="right",
        wraplength=appearance.width,
        bg=background,
        fg=foreground,
    )
    label.pack(anchor="ne")

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


def show_overlay(text: str, appearance: OverlayAppearance) -> mp.Process | None:
    try:
        if sys.platform in {"win32", "darwin"}:
            ctx = mp.get_context("spawn")
        else:
            ctx = mp.get_context("fork")
    except ValueError:  # pragma: no cover - fallback when preferred context unavailable
        ctx = mp.get_context()

    try:
        process = ctx.Process(target=_render_overlay, args=(text, appearance), daemon=True)
        process.start()
        return process
    except Exception as exc:  # pragma: no cover - last resort fallback
        print(f"[overlay] Failed to launch overlay process: {exc}")
        print(text)
        return None


def _render_overlay_macos(text: str, appearance: OverlayAppearance) -> bool:
    try:
        import objc
        from AppKit import (
            NSApp,
            NSApplication,
            NSPanel,
            NSScreen,
            NSTextView,
            NSColor,
            NSFont,
            NSMakeRect,
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            NSWindowCollectionBehaviorCanJoinAllSpaces,
            NSWindowCollectionBehaviorFullScreenAuxiliary,
            NSStatusWindowLevel,
        )
        from Foundation import NSObject, NSTimer
        from PyObjCTools import AppHelper
    except Exception as exc:  # pragma: no cover
        print(f"[overlay] macOS overlay unavailable: {exc}")
        return False

    class OverlayController(NSObject):
        def init(self):
            self = objc.super(OverlayController, self).init()
            if self is None:
                return None
            self.panel = None
            return self

        def show_(self, _sender=None):
            width = appearance.width + 40
            line_estimate = max(1, text.count("\n") + len(text) // max(1, appearance.width // 8))
            height = max(120, min(600, 50 + line_estimate * 24))

            screen = NSScreen.mainScreen()
            if screen is not None:
                frame = screen.visibleFrame()
                x = frame.origin.x + frame.size.width - width - 60
                y = frame.origin.y + frame.size.height - height - 80
            else:
                x, y = 100, 100

            panel = NSPanel.alloc().initWithContentRect_styleMask_backing_defer_(
                NSMakeRect(x, y, width, height),
                NSWindowStyleMaskBorderless,
                NSBackingStoreBuffered,
                False,
            )
            panel.setLevel_(NSStatusWindowLevel)
            panel.setOpaque_(False)
            panel.setAlphaValue_(max(0.05, min(appearance.opacity, 1.0)))
            panel.setBackgroundColor_(NSColor.clearColor())
            panel.setHasShadow_(True)
            behaviors = (
                NSWindowCollectionBehaviorCanJoinAllSpaces
                | NSWindowCollectionBehaviorFullScreenAuxiliary
            )
            panel.setCollectionBehavior_(behaviors)

            text_view = NSTextView.alloc().initWithFrame_(NSMakeRect(20, 20, width - 40, height - 40))
            text_view.setEditable_(False)
            text_view.setSelectable_(False)
            text_view.setDrawsBackground_(False)
            text_view.setString_(text)
            text_view.setTextColor_(NSColor.whiteColor())
            text_view.setFont_(NSFont.systemFontOfSize_(16))
            panel.contentView().addSubview_(text_view)

            panel.makeKeyAndOrderFront_(None)
            app.activateIgnoringOtherApps_(True)
            self.panel = panel

            if appearance.duration > 0:
                NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                    appearance.duration,
                    self,
                    "close:",
                    None,
                    False,
                )

        def close_(self, _sender=None):
            if self.panel is not None:
                self.panel.orderOut_(None)
                self.panel.close()
            AppHelper.stopEventLoop()

    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(1)  # accessory
    controller = OverlayController.alloc().init()
    controller.show_(None)
    AppHelper.runConsoleEventLoop()
    return True
