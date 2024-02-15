import tkinter as tk
import threading
import time
import os
import sys
import ctypes

class CountdownApp:
    def __init__(self, master, minutes):
        self.master = master
        self.master.title("Countdown Timer")
        self.master.geometry("300x150+{}+{}".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 150))
        self.master.resizable(False, False)

        self.label = tk.Label(master, font=('Helvetica', 24))
        self.label.pack(pady=30)

        self.total_seconds = minutes * 60
        self.interval = 10  # Set the interval in seconds to blink every 10 seconds
        self.should_blink = False  # Flag to control initial blink
        self.blink_duration = 30  # Time duration for blinking at the end (in seconds)
        self.blink_interval = 10  # Interval for each blink (in seconds)
        self.blink_count = 3  # Number of blinks during the last 30 seconds

        threading.Thread(target=self.countdown).start()

        self.master.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.master.wm_attributes("-topmost", 1)
        self.master.wm_attributes("-alpha", 0.7)

        self.bind_double_click()

    def on_double_click(self, event):
        self.master.destroy()

    def bind_double_click(self):
        self.master.bind("<Double-Button-1>", self.on_double_click)

    def countdown(self):
        while self.total_seconds > 0:
            minutes, seconds = divmod(self.total_seconds, 60)
            time_string = f'{minutes:02d}:{seconds:02d}'
            self.label.config(text=time_string)

            if self.total_seconds <= self.blink_duration:
                time_left_for_blink = self.total_seconds

                if time_left_for_blink % self.blink_interval == 0 and self.blink_count > 0:
                    self.blink()
                    self.blink_count -= 1

            self.total_seconds -= 1
            time.sleep(1)

        self.finish()

    def blink(self):
        blink_window = tk.Toplevel(self.master)
        blink_window.attributes('-fullscreen', True)
        blink_window.attributes('-alpha', 0.0)  # Set initial transparency to 0%
        blink_window.configure(bg='black')

        label = tk.Label(blink_window, text="Blink your eyes", font=("Helvetica", 48), fg="white", bg="black")
        label.pack(expand=True)

        def fade_in():
            current_alpha = float(blink_window.attributes('-alpha'))
            if current_alpha < 1.0:
                new_alpha = current_alpha + 0.05  # Increase alpha by 5%
                blink_window.attributes('-alpha', new_alpha)
                blink_window.after(50, fade_in)  # Schedule the next step in 50 milliseconds

        def fade_out():
            current_alpha = float(blink_window.attributes('-alpha'))
            if current_alpha > 0.0:
                new_alpha = current_alpha - 0.05  # Decrease alpha by 5%
                blink_window.attributes('-alpha', new_alpha)
                blink_window.after(50, fade_out)  # Schedule the next step in 50 milliseconds
            else:
                remove_text_and_transparency()

        def remove_text_and_transparency():
            label.pack_forget()  # Remove the label
            blink_window.attributes('-alpha', 1.0)  # Set transparency back to 100%
            blink_window.attributes('-fullscreen', False)  # Exit fullscreen mode
            blink_window.destroy()  # Destroy the Toplevel window

        blink_window.after(2000, fade_out)  # Schedule the fade out after 2 seconds
        fade_in()  # Start the fade in effect

    def finish(self):
        ctypes.windll.user32.LockWorkStation()
        # os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0') 
        sys.exit()

    def do_nothing(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root, minutes=20)
    root.mainloop()
