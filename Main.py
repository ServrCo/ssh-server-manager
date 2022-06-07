from tkinter.messagebox import askquestion
from paramiko import SSHClient
import configparser
from tkinter import *

client = SSHClient()

# Load config file
config = configparser.ConfigParser()
config.read('config.ini')


# Connect over SSH
def start():
    # Determine authentication method
    auth_type = config['DEFAULT']['auth-type']
    if auth_type == 'password':
        username = config['LOGIN']['username']
        password = config['LOGIN']['password']
        client.connect(hostname, username=username, password=password)
    elif auth_type == 'key':
        username = config['LOGIN']['username']
        key_path = config['DEFAULT']['key-path']
        ssh_passphrase = config['LOGIN']['ssh-passphrase']
        client.connect(hostname, username=username, key_filename=key_path, passphrase=ssh_passphrase)

# Poweroff System
def poweroff():
    stdin, stdout, stderr = client.exec_command('sudo shutdown -h now')

# Restart System
def restart():
    stdin, stdout, stderr = client.exec_command('sudo reboot')

# Update packages
def update_packages():
    stdin, stdout, stderr = client.exec_command('sudo apt update')

# Upgrade packages
def upgrade_packages():
    stdin, stdout, stderr = client.exec_command('sudo apt upgrade')

# Purge package
def purge_package():
    def purge_p():
        stdin, stdout, stderr = client.exec_command('sudo apt purge ' + pkg_name.get())
    win = Toplevel(root)
    win.title("Purge Package")
    win.resizable(0, 0)
    pkg_name = Entry(win)
    pkg_name.grid(row=0, column=0)
    purge_btn = Button(win, text="Purge", command=purge_p)
    purge_btn.grid(row=0, column=1)

def system_maintenance():
    # Dialog box asking for user confirmation
    answer = askquestion("Run Maintenance", "Are you sure you want to continue? This will reboot the system.")
    if answer == True:
        stdin, stdout, stderr = client.exec_command('sudo apt update && sudo apt upgrade')
        # Update and Upgrade
        stdin, stdout, stderr = client.exec_command('sudo apt update')
        stdin, stdout, stderr = client.exec_command('sudo apt upgrade')
        # Dist-Upgrade
        stdin, stdout, stderr = client.exec_command('sudo apt dist-upgrade')
        # Auto-Fix
        stdin, stdout, stderr = client.exec_command('sudo apt autoremove')
        stdin, stdout, stderr = client.exec_command('sudo apt autoclean')
        stdin, stdout, stderr = client.exec_command('sudo apt clean')
        # fsck
        stdin, stdout, stderr = client.exec_command('sudo fsck -AR -y')
        # Reboot
        stdin, stdout, stderr = client.exec_command('sudo reboot')
    else:
        print("Cancelled")
    

# Power Management
def power():
    win = Toplevel(root)
    win.title("Power Management")
    win.resizable(0, 0)
    power_off = Button(win, text="Power Off", command=poweroff)
    power_off.grid(row=0, column=0)
    restart_btn = Button(win, text="Restart", command=restart)
    restart_btn.grid(row=0, column=1)

# Manage packages
def package_mgmt():
    win = Toplevel(root)
    win.title("Packages")
    win.resizable(0, 0)
    update = Button(win, text="Update-Packages", command=update_packages)
    update.grid(row=0, column=0)
    upgrade = Button(win, text="Upgrade-Packages", command=upgrade_packages)
    upgrade.grid(row=0, column=1)
    purge_pkg = Button(win, text="Purge-Package", command=purge_package)
    purge_pkg.grid(row=0, column=2)\

def security():
    win = Toplevel(root)
    win.title("Maintenance")
    win.resizable(0, 0)
    update_all = Button(win, text="Run System Maintenance", command=system_maintenance)
    update_all.grid(row=0, column=0)


# Main Window
root = Tk()
root.title("SSH Client")
root.resizable(0, 0)
power_btn = Button(root, text="Power", command=power)
power_btn.grid(row=0, column=0)
security_btn = Button(root, text="Security", command=security)
security_btn.grid(row=0, column=1)


root.mainloop()

