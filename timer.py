import tkinter as tk

class PomodoroTimer:
    COLOR_PRIMARY = "#f7f5dd"
    COLOR_SECONDARY = "#9bdeac"
    COLOR_ALERT = "#e2979c"
    COLOR_WARNING = "#e7305b"
    FONT_TYPE = "Courier"
    WORK_DURATION = 25  # in minutes
    BREAK_DURATION_SHORT = 5  # in minutes
    BREAK_DURATION_LONG = 20  # in minutes

    def __init__(self, window):
        self.window = window
        self.session_count = 0
        self.current_timer = None
        
        self.window.title("Pomodoro Timer")
        self.window.config(padx=100, pady=50, bg=self.COLOR_PRIMARY)
        
        # Canvas for the timer display
        self.canvas_area = tk.Canvas(self.window, width=200, height=224, bg=self.COLOR_PRIMARY, highlightthickness=0)
        self.display_timer_text = self.canvas_area.create_text(100, 130, text="00:00", font=(self.FONT_TYPE, 35, "bold"), fill="white")
        self.canvas_area.grid(row=1, column=1)

        # Header label for the timer
        self.header_label = tk.Label(self.window, text="Timer", font=(self.FONT_TYPE, 40, "bold"), fg=self.COLOR_SECONDARY, bg=self.COLOR_PRIMARY)
        self.header_label.grid(row=0, column=1)

        self.progress_marks = tk.Label(self.window, text="", font=(self.FONT_TYPE, 20, "bold"), fg=self.COLOR_SECONDARY, bg=self.COLOR_PRIMARY)
        self.progress_marks.grid(row=3, column=1)

        # Start button
        self.start_button = tk.Button(self.window, text="Start", command=self.initiate_timer, bg=self.COLOR_PRIMARY, highlightthickness=0)
        self.start_button.grid(row=2, column=0)

        # Reset button
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_timer, bg=self.COLOR_PRIMARY)
        self.reset_button.grid(row=2, column=2)

    def reset_timer(self):
        self.window.after_cancel(self.current_timer)
        self.canvas_area.itemconfig(self.display_timer_text, text="00:00")
        self.header_label.config(text="Timer")
        self.progress_marks.config(text="")
        self.session_count = 0

    def initiate_timer(self):
        work_time = self.WORK_DURATION * 60
        short_break_time = self.BREAK_DURATION_SHORT * 60
        long_break_time = self.BREAK_DURATION_LONG * 60

        self.session_count += 1

        if self.session_count % 8 == 0:
            self.countdown(long_break_time)
            self.header_label.config(text="Break", fg=self.COLOR_WARNING)
        elif self.session_count % 2 == 0:
            self.countdown(short_break_time)
            self.header_label.config(text="Break", fg=self.COLOR_ALERT)
        else:
            self.countdown(work_time)
            self.header_label.config(text="Work", fg=self.COLOR_SECONDARY)

    def countdown(self, time_left):
        minutes = time_left // 60
        seconds = time_left % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        if minutes < 10:
            minutes = f"0{minutes}"

        self.canvas_area.itemconfig(self.display_timer_text, text=f"{minutes}:{seconds}")
        if time_left > 0:
            self.current_timer = self.window.after(1000, self.countdown, time_left - 1)
        else:
            self.initiate_timer()
            completed_sessions = self.session_count // 2
            progress = "✔" * completed_sessions
            self.progress_marks.config(text=progress)


def main():
    window = tk.Tk()
    pomodoro_timer = PomodoroTimer(window)
    window.mainloop()

if __name__ == "__main__":
    main()
