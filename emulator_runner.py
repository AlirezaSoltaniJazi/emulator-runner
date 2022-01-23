import os
import subprocess
import threading
import tkinter as tk
from tkinter.ttk import Notebook
from subprocess import Popen, PIPE

# Create an instance of tkinter frame (root)
form_frame_tab = tk.Tk()
form_frame_tab.title('Emulator/Device Manager')
form_gui_tab = Notebook(form_frame_tab)
# Create tabs in the frame
tab_avd = tk.Frame(form_gui_tab)
tab_adb = tk.Frame(form_gui_tab)
tab_about_us = tk.Frame(form_gui_tab)
# Set title for the tabs
form_gui_tab.add(tab_avd, text='AVD Manager')
form_gui_tab.add(tab_adb, text='ADB Manager')
form_gui_tab.add(tab_about_us, text='About Us')
# Add label to tab
label_about_us = tk.Label(tab_about_us, text='Made with love by Bazaar QA Team ❤')
label_about_us.place(anchor='center', relx=0.5, rely=0.5)
form_gui_tab.pack(expand=1, fill="both")

# Data
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
    # Start adb server
    os.system('adb start-server')
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
            button = tk.Button(tab_avd,
                               text=emulator,
                               fg="black",
                               height=1,
                               width=maximum_emulator_name)
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
        print('Device list is empty...')
        tk.Label(tab_avd, text='You don\'t have any emulator yet! ¯\\_(ツ)_/¯ '
                               '\n Add emulator (s) then re-open application!   ').place(anchor='center', relx=0.5,
                                                                                         rely=0.5)


def create_button_adb():
    if len(device_list) > 0:
        item_counter = 0
        row = 0
        column = 0
        # get maximum device name that exist in the emulator list
        maximum_device_name = max(len(x) for x in device_list)
        for device in device_list:
            # Create button with some attributes - fg=text color/text=button text/command(optional)
            button = tk.Button(tab_adb,
                               text=device,
                               fg="black",
                               height=1,
                               width=maximum_device_name)
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
        tk.Label(tab_adb, text='You don\'t have any device yet! ¯\\_(ツ)_/¯ '
                               '\n Add device (s) then re-open application!   ').place(anchor='center', relx=0.5,
                                                                                       rely=0.5)


def on_click_event(event):
    # Get element type to ignore tab click event
    element_type = str(event.widget.winfo_class())
    current_tab_index = form_gui_tab.index(form_gui_tab.select())
    if current_tab_index == 0 and element_type == 'Button':
        print('AVD tab')
        if len(emulator_list) != 0:
            on_click_avd(event)
        else:
            print('There isn\'t any emulator in the list')
    elif current_tab_index == 1 and element_type == 'Button':
        print('ADB tab')
        if len(device_list) != 0:
            on_click_adb(event)
        else:
            print('There isn\'t any device in the list')
    else:
        print(f'Tab changed to: {current_tab_index}')
        form_creator()


def on_click_avd(event):
    print(event)
    # Get the text of the button that clicked
    emulator_name_text = event.widget.cget('text')
    # Use multithreading to avoid "not responding" problem in tkinter lib
    x = threading.Thread(target=start_emulator, args=(emulator_name_text,))
    x.start()
    print("Starting", emulator_name_text, "...")


def on_click_adb(event):
    print(event)
    # Get the text of the button that clicked
    device_name_text = event.widget.cget('text')
    # Use multithreading to avoid "not responding" problem in tkinter lib
    x = threading.Thread(target=start_device, args=(device_name_text,))
    x.start()
    print("Starting", device_name_text, "...")


def tab_change(event=None):
    form_frame_tab.bind('<Button>', on_click_event)


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


def form_creator():
    emulator_list.clear()
    device_list.clear()

    # Get emulator list
    get_emulator_list()
    # Create button based on emulator list
    create_button_avd()

    # Get device list
    get_device_list()
    # Create button based on device list
    create_button_adb()


def main():
    form_creator()
    form_frame_tab.bind('<<NotebookTabChanged>>', tab_change)
    form_frame_tab.mainloop()


if __name__ == '__main__':
    main()
