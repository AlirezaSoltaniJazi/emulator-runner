import os
import threading
import tkinter as tk
from subprocess import Popen, PIPE

emulator_list = list()
root = tk.Tk()
# Set title for the windows
root.title('Emulator Runner')
# root.geometry("450x350")
frame = tk.Frame(root)
frame.pack()
frame.focus()
emulator_command = 'emulator'
get_emulator_list_command = '-list-avds'


def get_emulator_list():
    # Get the list of all emulators installed
    with Popen([emulator_command, get_emulator_list_command], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[:]:
            # Convert byte to string
            device_name = val.decode('UTF-8').strip()
            emulator_list.append(device_name)


def create_emulator_button():
    item_counter = 0
    row = 0
    column = 0
    # get maximum device name that exist in the emulator list
    maximum_device_name = max(len(x) for x in emulator_list)
    for emulator_device in emulator_list:
        # Create button with some attributes - fg=text color/text=button text/command(optional)
        button = tk.Button(frame,
                           text=emulator_device,
                           fg="black",
                           height=1,
                           width=maximum_device_name)
        # Bind keys to use them with event
        root.bind('<Button>', on_click)
        # Order bottoms like a calculator
        if item_counter < 4:
            button.grid(row=row, column=column)
            column += 1
            item_counter += 1
        else:
            button.grid(row=row, column=column)
            item_counter = 0
            column = 0
            row += 1


def on_click(event):
    # Get the text of the button that clicked
    emulator_name_text = event.widget.cget('text')
    # Use multithreading to avoid "not responding" problem in tkinter lib
    x = threading.Thread(target=start_emulator, args=(emulator_name_text,))
    x.start()
    print("Starting", emulator_name_text, "...")


def start_emulator(emulator_name):
    os.system(rf'emulator @{emulator_name}')


if __name__ == '__main__':
    # Get emulator list with adb
    get_emulator_list()
    # Create button based on emulator list
    create_emulator_button()
    root.mainloop()
