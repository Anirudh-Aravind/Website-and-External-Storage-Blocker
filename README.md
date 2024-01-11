# Website-and-External-Storage-Blocker
This Python script, designed for Windows, provides a dual functionality to enhance system security and control user access:

 ###    ![image](https://github.com/Anirudh-Aravind/Website-and-External-Storage-Blocker/assets/84184475/24f37165-63f6-4da0-aeba-e67292c492cf)


## Website Blocker:

The script allows users to block specific websites by redirecting their URLs to the local machine's IP address.
Blocking is achieved by manipulating the system's hosts file.
A simple Tkinter GUI provides a user-friendly interface to input and manage the list of blocked websites.


## External Storage Blocker:

The script monitors connected external storage devices, such as USB drives.
When an external storage device is detected, it displays a warning message, prompting the user to disconnect the device.
This feature helps prevent unauthorized use of external storage devices, enhancing security.

### Features:
##### Website Blocking:

Add or remove websites from the blocklist with ease.
User-friendly GUI for managing blocked websites.
Status updates on blocking/unblocking operations.

##### External Storage Blocking:

Instant alert when an external storage device is connected.
Full-screen warning message for user attention.
Temporary system interruptions until the external device is removed.

### Usage:
##### Website Blocking:

Launch the script, input website URLs in the GUI, and click "Block" to prevent access.
To unblock a website, use the GUI and click "Unblock."
##### External Storage Blocking:

The script continuously monitors connected drives.
If a removable disk is detected, a warning message is displayed.
System interruptions occur until the external device is disconnected.

### Requirements:
Python 3.x
Tkinter (for GUI)
Windows Operating System

### How to Run:
Clone the repository.
Run the web_storage_blocker.py script using Python.

## Note: 
### The effectiveness of website blocking using the hosts file depends on the user's system permissions. The script require elevated privileges to modify the hosts file located at 'C:\Windows\System32\drivers\etc\hosts'


