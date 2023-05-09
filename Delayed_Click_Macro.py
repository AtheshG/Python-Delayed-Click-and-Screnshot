import time
from tkinter import *
from tkinter.ttk import Combobox
import pyautogui
import threading
from datetime import datetime
import os

user_time = 0.0


class window(Tk):
    
    def __init__(self):
        super().__init__()
        #Window properties
        self.title('Delayed Click / Screenshot')
        self.geometry("400x250+100+100")
        self.resizable(False, False)

        #Labels and buttons
        self.H1 = Label(self, text="Select 'Click' for a delayed Left Click", fg='black', font=("Helvetica", 10))
        self.H1.place(relx=0.05, rely=0.1)

        self.H2 = Label(self, text="Select 'Screenshot' for a delayed Screenshot", fg='black', font=("Arial", 10))
        self.H2.place(relx=0.05, rely=0.3)

        self.List_Options = ("Click", "Screenshot")
        self.Selection_List = Combobox(self, values=self.List_Options, state='readonly')
        self.Selection_List.current(0)
        self.Selection_List.place(relx=0.4, rely=0.5, relwidth=0.2)

        self.Entry_Label = Label(self, text="Enter Delay in Seconds: ", fg='black', font=("Arial", 8))
        self.Entry_Label.place(relx=0.05, rely=0.7)

        self.Delay_Entry = Entry(self, text="", bd=2)
        self.Delay_Entry.place(relx=0.4, rely=0.7, relwidth=0.2)

        self.Run_Button = Button(self, text="Run", height=1, width=8, command=self.validate)
        self.Run_Button.place(relx=0.45, rely=0.85)
        self.launch()

    #Left Click after time delay
    def left_click(self):
        time.sleep(user_time)
        pyautogui.click()

    #Create and destroy invalid message label
    def invalid_message(self):
        Invalid_Label = Label(self, text="Invalid Entry", fg='red', font=("Arial", 8))
        Invalid_Label.place(relx=0.05, rely=0.8)
        self.after(2000, Invalid_Label.destroy)

    #Creates a seperate thread for the right click command. This is required as the GUI will crash if "time.sleep" is used on the main thread.
    def launch(self):
        threading.Thread(target=self.left_click).start()
    
    #Input Validation for combo box entry.
    def validate(self):
        
        if self.Delay_Entry.get().isdigit() and int(self.Delay_Entry.get()) > 0:
         global user_time 
         user_time = float(self.Delay_Entry.get())
        
         if self.Selection_List.get() == "Click":
            self.left_click()

         else: 
            self.open_SSwindow()

        else:
            self.invalid_message()

    def open_SSwindow(self):
        window = SSwindow(self)
        window.grab_set()


#GUI for screenshotting information
class SSwindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Screen Shot Options")
        self.geometry("300x200")
        self.resizable(False, False)

        # Label and entry for number of screenshots
        self.screenshot_label = Label(self, text="Number of screenshots:", font=("Helvetica", 10))
        self.screenshot_label.place(x=20, y=20)
        self.Screenshot_Entry = Entry(self, width=10, bd=2)
        self.Screenshot_Entry.place(x=200, y=20)

        # Label and entry for seconds between screenshots
        self.seconds_label = Label(self, text="Seconds between screenshots:", font=("Helvetica", 10))
        self.seconds_label.place(x=0, y=60)
        self.Second_Entry = Entry(self, width=10, bd=2)
        self.Second_Entry.place(x=200, y=60)

        # Button to start taking screenshots
        self.ss_button = Button(self, text="Take Screenshots", width=20, height=2, bg="#4CAF50", fg="white", command=self.validate_screenshot)
        self.ss_button.place(x=80, y=120)

        # Label for error messages
        self.error_label = Label(self, text="", fg="red")
        self.error_label.place(x=20, y=170)

        # Create screenshot folder if it doesn't exist
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")

    #A new thread must also be created for the screenshot method.
    def launch(self):
        threading.Thread(target=self.take_screenshot).start()

    #Input validation for screenshot entry
    def validate_screenshot(self):
        if self.Screenshot_Entry.get().isdigit() == False:
            self.invalid_entry()

        elif int(self.Screenshot_Entry.get()) > 150:
            Invalid_Entry_SS2 = Label(self, text="Max amount of screenshots is 150", fg='red', font=("Arial", 8))
            Invalid_Entry_SS2.place(relx=0.15, rely=0.3)
            self.after(2000, Invalid_Entry_SS2.destroy)

        else:
            self.validate_seconds()

    #Input validation for seconds entry
    def validate_seconds(self):
        if self.Second_Entry.get().isdigit() == False:
            self.invalid_entry()

        elif int(self.Second_Entry.get()) > 300:
            Too_Many_Seconds = Label(self, text="Max amount of seconds is 300", fg='red', font=("Arial", 8))
            Too_Many_Seconds.place(relx=0.05, rely=0.8)
            self.after(2000, Too_Many_Seconds.destroy)
        
        elif (float(self.Second_Entry.get()) < 0.1):
            Too_Fast = Label(self, text = "Max screenshot rate is 1 per 100 miliseconds", fg='red', font=("Arial", 8))
            Too_Fast.place(relx=0.05, rely=0.8)
            self.after(2000, Too_Fast.destroy)
        
        else:
            self.after(int(user_time), self.take_screenshot())

    #Calculates screenshots per seconds and calls screenshot function accordingly
    def take_screenshot(self):
        for x in range(int(self.Screenshot_Entry.get())):   
           time.sleep(float(self.Second_Entry.get()))
           filename = datetime.now().strftime("Screenshots/%Y-%m-%d_%H-%M-%S_%f.png")
           pyautogui.screenshot().save(filename)


    #Invalid entry label
    def invalid_entry(self):
        Invalid_Entry_SS = Label(self, text="Invalid Entry", fg='red', font=("Arial", 8))
        Invalid_Entry_SS.place(relx=0.05, rely=0.8)
        self.after(2000, Invalid_Entry_SS.destroy)      
        
if __name__ == "__main__":
    app = window()
    app.mainloop()