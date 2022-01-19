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
encoders_list = ['OMX.google.h264.encoder',
                 'c2.android.avc.encoder',
                 'OMX.qcom.video.encoder.avc']

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
    print('Emulator list', emulator_list)


def get_device_list():
    # Get the list of all emulators installed
    with Popen([adb_command, get_device_list_command], shell=True, stdout=PIPE) as proc:
        for val in proc.stdout.readlines()[1:-1]:
            # Convert byte to string
            device_name = val.decode('UTF-8').replace('device', '').strip()
            device_list.append(device_name)
    print('Device list', device_list)


def create_button_avd():
    if len(emulator_list) > 0:
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
    else:
        print('Emulator list is empty...')


def create_button_adb():
    if len(device_list) > 0:
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
    else:
        print('Device list is empty...')


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
        print("on_click_adb => Exception")
        print(e)


def start_emulator(emulator_name):
    try:
        # use subprocess to catch os error
        subprocess.run([rf'emulator @{emulator_name}'], check=True)
    except Exception as e:
        print("start_emulator => Exception")
        print(e)
        os.system(rf'emulator @{emulator_name}')


def start_device(device_name):
    check_fine = os.system(rf'scrcpy -s {device_name}')
    print("SCRCPY doesn't work with default encoder")
    # Try different encoders
    for encoder in encoders_list:
        if check_fine == 1:
            print(f'Try to using this encoder: {encoder}')
            check_fine = os.system(rf'scrcpy -s {device_name} --encoder {encoder}')
        else:
            break


if __name__ == '__main__':
    # Get emulator list
    get_emulator_list()
    # Create button based on emulator list
    create_button_avd()

    # Get device list
    get_device_list()
    # Create button based on emulator list
    create_button_adb()

    form_frame_avd.mainloop()
    form_frame_adb.mainloop()
