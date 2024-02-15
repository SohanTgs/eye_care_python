import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time
import tkinter as tk


class CountdownApp:
    def __init__(self, master, minutes):
        self.first = True
        self.master = master
        self.master.title("Countdown Timer")
        self.master.geometry("300x150+{}+{}".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 150))
        self.master.resizable(False, False)

        self.label = tk.Label(master, font=('Helvetica', 24))
        self.label.pack(pady=30)

        self.total_seconds = minutes * 60
        threading.Thread(target=self.countdown).start()

        self.master.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.master.wm_attributes("-topmost", 1)
        self.master.wm_attributes("-alpha", 0.7)

    def countdown(self):
        interval = 3  # Set the interval in seconds
        while self.total_seconds > 0:
            minutes, seconds = divmod(self.total_seconds, 60)
            time_string = f'{minutes:02d}:{seconds:02d}'
            self.label.config(text=time_string)
            
            if self.total_seconds % interval == 0:  # Check if it's a multiple of the interval
                if self.first == True:
                    self.first = False
                else: 
                    self.blink()
                # self.show_tooltip("Blink your eyes")

            self.total_seconds -= 1
            time.sleep(1)

        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0') 
        sys.exit()

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


    def show_message(self, message):
        messagebox.showinfo("Countdown Timer", message)
        self.master.destroy()

    def show_tooltip(self, text):
        tooltip_window = tk.Toplevel(self.master)
        tooltip_window.wm_overrideredirect(True)
        tooltip_window.wm_attributes('-topmost', True)
        tooltip_window.wm_attributes('-alpha', 1.0)  # Set opacity to 100%
        tooltip_window.configure(bg='orange')  # Change the background color

        tooltip_label = tk.Label(tooltip_window, text=text, bg='orange', padx=10, pady=5, font=('Helvetica', 12, 'bold'))
        tooltip_label.pack()

        close_button = tk.Button(tooltip_window, text="Close", command=tooltip_window.destroy)
        close_button.pack(pady=5)

        x, y, _, _ = self.label.bbox('all')

        # Check if the tooltip would appear off-screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        tooltip_width = tooltip_window.winfo_width()
        tooltip_height = tooltip_window.winfo_height()

        if x + 20 + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 20
        if y - 30 - tooltip_height < 0:
            y = 30 + tooltip_height

        tooltip_window.wm_geometry(f"+{x+20}+{y-30}")
        tooltip_window.lift(self.master)

        def close_tooltip():
            tooltip_window.destroy()

        tooltip_label.after(3000, close_tooltip)

    def do_nothing(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root, minutes=20)
    root.mainloop()
