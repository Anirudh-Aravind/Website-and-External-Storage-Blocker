# ==================================================================
# Author       : Anirudh P M
# CreatedDate  : 07-01-2024
# version      : 1.0
# Updated Date :
# Changes Done :
# ==================================================================

"""
1. This script has two contents
   * The script attempts to block the URLs we provide, but it also offers the option to unblock those web URLs from their blocked state
   * An alert notice will appear and prevent you from using the system normally until you unplug any external storage devices that attempt to connect to it
2. Design & Implementation:
   * The script is deployed with a Tkinter GUI
   * Creates the main Tkinter window (root) with a fixed size and title
   * Labels, text entry (Text), and buttons are placed on the window for website blocking functionality
   * The status_label is used to display the status of website blocking operations
   * A separate thread (drive_monitor_thread) is created to run the drive monitoring loop concurrently
   * Initiates the main event loop for the Tkinter GUI, ensuring continuous execution of the GUI and drive monitoring threads
3. External Storage Monitoring:
   * Runs in an infinite loop, continuously checking for connected drives
   * It utilizes PowerShell through subprocess to retrieve information about the connected drives
   * Parses the JSON output to obtain details like drive letter, volume name, and drive type (e.g., Removable Disk, Local Disk)
   * If a removable disk is detected, it creates a new Tkinter window (interrupt_tk) to display a warning message for 3 seconds
   * The Tkinter window attributes are set for full screen, topmost, and disabled to grab user attention, which display a message with red, bold text in the center of the window
4. Website Blocking:
   * The script utilizes the hosts file located at 'C:\Windows\System32\drivers\etc\hosts'
   * The hosts file is a system file that maps hostnames to IP addresses
   * The IP address '127.0.0.1' is commonly known as the loopback address or localhost
   * In this script, it is used to redirect blocked website URLs to the local machine
   * The block_website function reads the entered website URLs from the Tkinter Text widget
   * It checks whether each website URL is already present in the hosts file
   * If a website is not present, it adds an entry in the hosts file, mapping the website URL to the localhost IP address
   * The unblock_website function reads the entered website URLs from the Tkinter Text widget
   * It reads the content of the hosts file and excludes the entries corresponding to the specified website URLs
   * The modified content is then written back to the hosts file, effectively unblocking the specified websites
   * The update_status_label function updates a Tkinter label (status_label) to provide feedback on the success or failure of blocking/unblocking operations
   * The Tkinter GUI includes buttons labeled 'Block' and 'Unblock.'
   * These buttons trigger the block_website and unblock_website functions, respectively, when clicked
   * When a website is successfully blocked, the status label displays "Blocked."
   * If a user attempts to block a website that is already blocked, the status label shows "Already Blocked."
   * Unblocking a website results in the status label displaying "Unblocked."
   * By mapping blocked website URLs to the localhost IP address in the hosts file, attempts to access those websites redirect to the local machine
   * This effectively prevents the user from accessing the blocked websites

Note:
The effectiveness of website blocking using the hosts file depends on the user's system permissions
The script require elevated privileges to modify the hosts file
"""

# Importing the required libraries
import tkinter as tk
from tkinter import *
import threading
from time import sleep
import json
import subprocess
from urllib.parse import urlparse

def list_drives():
    """
    Get a list of drives using WMI
    :return: list of drives
    """
    proc = subprocess.run(
        args=[
            'powershell',
            '-noprofile',
            '-command',
            'Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json'
        ],
        text=True,
        stdout=subprocess.PIPE
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print('Failed to enumerate drives')
        return []
    devices = json.loads(proc.stdout)

    drive_types = {
        0: 'Unknown',
        1: 'No Root Directory',
        2: 'Removable Disk',
        3: 'Local Disk',
        4: 'Network Drive',
        5: 'Compact Disc',
        6: 'RAM Disk',
    }

    return [
        {'letter': d['deviceid'], 'label': d['volumename'], 'drive_type': drive_types[d['drivetype']]}
        for d in devices
    ]

def watch_drives():
    """
    This function continuously monitors connected drives and displays a Tkinter pop-up alert if any external driver detected
    :return: None
    """
    while True:
        drives = list_drives()
        for drive in drives:
            interrupt_tk = tk.Tk()
            if drive['drive_type'] == 'Removable Disk':
                alert_msg = "Detected an external storage device connection. Please disconnect the device immediately. " \
                            "Otherwise, the system will experience interruptions at 3-second intervals until the external device is removed."
                # Display the alert message in the middle with red bold letters
                label = tk.Label(interrupt_tk, text=alert_msg, font=('Arial', 16, 'bold'), fg='red', wraplength=400)
                label.pack(expand=True, pady=(50, 50), padx=(20, 20))

                interrupt_tk.attributes("-fullscreen", True, "-topmost", True, "-disabled", True)

                time_interrupt = 3000 # Time screen is active in ms
                interrupt_tk.after(time_interrupt, interrupt_tk.destroy)

                interrupt_tk.mainloop()
            else:
                interrupt_tk.destroy()

        sleep(1)

def block_website():
    """
    This function reads user-entered website URLs from a Tkinter Text widget, checks whether each URL is already blocked in
    the host file, and updates the status label accordingly, either indicating that the website is already blocked or
    blocking the website and updating the status label
    :return: None
    """
    website_lists = Websites.get(1.0, END)
    website_list = list(website_lists.split(","))
    with open(host_path, 'r+') as host_file:
        file_content = host_file.read()
        for web in website_list:
            if urlparse(web).netloc in file_content:
                update_status_label('Already Blocked')
            else:
                host_file.write(ip_address + " " + urlparse(web).netloc + '\n')
                update_status_label('Blocked')

def unblock_website():
    """
    This function retrieves the list of blocked websites from the Tkinter Text widget, reads the existing host file, removes
    the entries corresponding to the specified websites, and updates the status label to indicate successful unblocking.
    :return: None
    """
    website_lists = Websites.get(1.0, END)
    website_list = list(website_lists.split(","))
    with open(host_path, 'r') as host_file:
        lines = host_file.readlines()
    with open(host_path, 'w') as host_file:
        for line in lines:
            if not any(urlparse(web).netloc in line for web in website_list):
                host_file.write(line)
        update_status_label('Unblocked')

def update_status_label(message):
    """
    This function updates the text content of the status_label widget in the Tkinter GUI with the provided message
    :param message: URL blocking or unblocking message
    :return: None
    """
    status_label.config(text=message)

# Tkinter GUI setup
root = Tk()
root.geometry('500x300')
root.resizable(0, 0)
root.title("Website Blocker")

Label(root, text='Website Blocker', font='arial 20 bold').pack()
host_path = 'C:\Windows\System32\drivers\etc\hosts'
ip_address = '127.0.0.1'

Label(root, text='Enter Website :', font='arial 13 bold').place(x=5, y=60)
Websites = Text(root, font='arial 10', height='2', width='40')
Websites.place(x=140, y=60)

status_label = Label(root, text='', font='arial 12 bold', width=20)
status_label.place(x=200, y=200)

block_button = Button(root, text='Block', font='arial 12 bold', pady=5, command=block_website, width=6,
                      bg='royal blue1', activebackground='sky blue')
block_button.place(x=150, y=150)

unblock_button = Button(root, text='Unblock', font='arial 12 bold', pady=5, command=unblock_website, width=6,
                        bg='orange', activebackground='yellow')
unblock_button.place(x=250, y=150)

# Create a separate thread for drive monitoring
drive_monitor_thread = threading.Thread(target=watch_drives)
drive_monitor_thread.daemon = True  # Set as a daemon thread to terminate with the main thread
drive_monitor_thread.start()

root.mainloop()
