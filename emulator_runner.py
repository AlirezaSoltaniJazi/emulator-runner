import os
import subprocess
import threading
import tkinter as tk
from subprocess import Popen, PIPE

# Create AVD manager form
form_frame_avd = tk.Tk()
# Set title for the windows
form_frame_avd.title('AVD Manager')
form_gui_avd = tk.Frame(form_frame_avd)
form_gui_avd.pack()
# Focus on this form
form_gui_avd.focus()

# Create ADB manager form
form_frame_adb = tk.Tk()
form_frame_adb.title('ADB Manager')
form_gui_adb = tk.Frame(form_frame_adb)
form_gui_adb.pack()

# Static data
avd_command = 'emulator'
get_emulator_list_command = '-list-avds'
adb_command = 'adb'
get_device_list_command = 'devices'

# Setup global variables
emulator_list = list()
device_list = list()


def get_emulator_list():
    # Get the list of all emulators installed
    with Popen([avd_command, get_emulator_list_command], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[:]:
            # Convert byte to string
            device_name = val.decode('UTF-8').strip()
            emulator_list.append(device_name)
    print(emulator_list)


def get_device_list():
    # Get the list of all emulators installed
    with Popen([adb_command, get_device_list_command], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[1:-1]:
            print(val)
            # Convert byte to string
            device_name = val.decode('UTF-8').replace('device', '').strip()
            device_list.append(device_name)
    print(device_list)


def create_emulator_button_avd():
    item_counter = 0
    row = 0
    column = 0
    # get maximum device name that exist in the emulator list
    maximum_emulator_name = max(len(x) for x in emulator_list)
    for emulator in emulator_list:
        # Create button with some attributes - fg=text color/text=button text/command(optional)
        button = tk.Button(form_gui_avd,
                           text=emulator,
                           fg="black",
                           height=1,
                           width=maximum_emulator_name)
        # Bind keys to use them with event
        form_frame_avd.bind('<Button>', on_click_avd)
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


def create_emulator_button_adb():
    item_counter = 0
    row = 0
    column = 0
    # get maximum device name that exist in the emulator list
    maximum_device_name = max(len(x) for x in device_list)
    for device in device_list:
        # Create button with some attributes - fg=text color/text=button text/command(optional)
        button = tk.Button(form_gui_adb,
                           text=device,
                           fg="black",
                           height=1,
                           width=maximum_device_name)
        # Bind keys to use them with event
        form_frame_adb.bind('<Button>', on_click_adb)
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


def on_click_avd(event):
    # Get the text of the button that clicked
    emulator_name_text = event.widget.cget('text')
    # Use multithreading to avoid "not responding" problem in tkinter lib
    x = threading.Thread(target=start_emulator, args=(emulator_name_text,))
    x.start()
    print("Starting", emulator_name_text, "...")


def on_click_adb(event):
    try:
        # Get the text of the button that clicked
        device_name_text = event.widget.cget('text')
        # Use multithreading to avoid "not responding" problem in tkinter lib
        x = threading.Thread(target=start_device, args=(device_name_text,))
        x.start()
        print("Starting", device_name_text, "...")
    except Exception as e:
        print("----------------------")
        print(e)


def start_emulator(emulator_name):
    try:
        # use subprocess to catch os error
        subprocess.run([rf'emulator @{emulator_name}'], check=True)
    except Exception as e:
        print(e)
        os.system(rf'emulator @{emulator_name}')


def start_device(device_name):
    check_fine = 0
    check_fine = os.system(rf'scrcpy -s {device_name}')
    print("Normal SCRCPY doesn't work")
    # Handle start device with different encoders
    if check_fine == 1:
        check_fine = os.system(rf'scrcpy -s {device_name} --encoder OMX.google.h264.encoder')
        print("SCRCPY with OMX.google.h264.encoder encoder doesn't work")
        if check_fine == 1:
            print("SCRCPY with OMX.google.h264.encoder encoder doesn't work")
            check_fine = os.system(rf'scrcpy -s {device_name} --encoder c2.android.avc.encoder')
            print("SCRCPY with c2.android.avc.encoder encoder doesn't work")
            if check_fine == 1:
                os.system(rf'scrcpy -s {device_name} --encoder OMX.qcom.video.encoder.avc')


if __name__ == '__main__':
    # Get emulator list
    get_emulator_list()
    # Create button based on emulator list
    create_emulator_button_avd()

    # Get device list
    get_device_list()
    # Create button based on emulator list
    create_emulator_button_adb()

    form_frame_avd.mainloop()
    form_frame_adb.mainloop()
