import tkinter as tk

from ..core.ports import SpeechControlPort, TriggerControllerPort


class TkinterFloatingController(TriggerControllerPort):
    """Floating GUI controller that maps button clicks to speech control actions."""

    FOCUS_RETURN_DELAY_MS = 120

    def __init__(self, speech_controls: SpeechControlPort, tk_module=tk):
        self._speech_controls = speech_controls
        self._tk = tk_module
        self._has_started = False

    def run(self) -> None:
        root = self._tk.Tk()
        root.title("TTS Controls")
        root.geometry("220x96+40+40")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        focus_command = self._with_focus_return
        controls = [
            ("⏮", focus_command(root, self._speech_controls.speak_prev_sentence), 0, 0),
            ("▶", focus_command(root, self._start_or_resume), 0, 1),
            ("⏸", focus_command(root, self._speech_controls.stop_speaking), 0, 2),
            ("⏭", focus_command(root, self._speech_controls.speak_next_sentence), 0, 3),
            (
                "◎",
                focus_command(root, self._speech_controls.speak_current_sentence),
                1,
                0,
            ),
            ("➕", focus_command(root, self._speech_controls.increment_rate_up), 1, 1),
            (
                "➖",
                focus_command(root, self._speech_controls.increment_rate_down),
                1,
                2,
            ),
            ("✕", root.destroy, 1, 3),
        ]

        for label, command, row, column in controls:
            button = self._tk.Button(root, text=label, command=command, width=3)
            button.grid(row=row, column=column, padx=4, pady=6)

        root.protocol("WM_DELETE_WINDOW", root.destroy)
        root.mainloop()

    def _with_focus_return(self, root, command):
        def wrapped_command():
            # Hide briefly so the previously active app can receive copy hotkeys.
            root.withdraw()
            root.after(
                self.FOCUS_RETURN_DELAY_MS, lambda: self._run_and_restore(root, command)
            )

        return wrapped_command

    def _run_and_restore(self, root, command):
        try:
            command()
        finally:
            root.deiconify()
            root.lift()
            root.attributes("-topmost", True)

    def _start_or_resume(self) -> None:
        # Keep SpeechController untouched: first click loads selection, later clicks resume.
        if not self._has_started:
            self._speech_controls.start_speaking()
            self._has_started = True
            return
        self._speech_controls.speak_current_sentence()
