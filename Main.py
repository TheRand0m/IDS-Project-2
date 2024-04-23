
import os
import sys
import tkinter
from tkinter import *
from tkinter import ttk
import customtkinter
from customtkinter import filedialog


class IntrusionDetector:
    def __init__(self):
        self.model = "SVM"
        self.path = r"" # Holds the dataset path

    def launchGUI(self):
        def fileInputButton():
            filename = filedialog.askopenfilename()
            print(filename)

        # Code fetched from : https://www.youtube.com/watch?v=iM3kjbbKHQU
        customtkinter.set_appearance_mode("light")

        root = customtkinter.CTk()
        root.geometry("500x350")

        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Select CSV dataset to train/test:")
        label.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=frame, text="Select File", command=fileInputButton)
        button.pack(pady=12, padx=10)

        # Run GUI application.
        root.mainloop()


def main():
    mIntrusionDetector = IntrusionDetector()



    # .\Main.py --gui parameter will launch GUI version.
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == "--gui":
    #         mIntrusionDetector.launchGUI()
    #
    mIntrusionDetector.print_menu()
    selection = 0
    while selection < 3:
        option = input("Enter option: ")
        if selection == 1:
            csv_path = input("Enter CSV path: ")

    print("Good bye!")

if __name__ == "__main__":
    main()