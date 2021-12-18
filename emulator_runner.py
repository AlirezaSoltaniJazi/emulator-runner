import os
import threading
import tkinter as tk
from subprocess import Popen, PIPE

emulator_list = list()
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
frame.focus()
emulator_command = 'emulator'
get_emulator_list_command = '-list-avds'


def get_emulator_list():
    with Popen([emulator_command, get_emulator_list_command], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[1:-1]:
            device_name = val.decode('UTF-8').strip()
            emulator_list.append(device_name)


def create_emulator_button():
    for emulator_device in emulator_list:
        button = tk.Button(frame,
                           text=emulator_device,
                           fg="black")
        # button.configure(command=lambda: on_click(emulator_device))
        root.bind('<Button>', on_click)
        button.pack(side=tk.LEFT)


def on_click(event):
    # Get the text of the button that clicked
    emulator_name_text = event.widget.cget('text')
    # Use multithreading to avoid "not responding" problem
    x = threading.Thread(target=start_emulator, args=(emulator_name_text,))
    x.start()
    print("Starting", emulator_name_text, "...")


# start_emulator(emulator_name_text)


def start_emulator(emulator_name):
    os.system(rf'emulator @{emulator_name}')


# Get emulator list with adb
get_emulator_list()
# Create button based on emulator list
create_emulator_button()
root.title('Emulator Runner')
root.mainloop()
