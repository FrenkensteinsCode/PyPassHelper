from PyPassHelper_backend import *
from tkinter import *
from tkinter import messagebox
from pathlib import Path

pwfile_path = Path(pwfile_location)

# Info and ReadMe functions
def get_info_dialog():
    m_text = "\
**********************\n\
Title: PyPassHelper\n\
Author: @FrenkensteinsCode\n\
Version: 1.0.0\n\
**********************"
    messagebox.showinfo(message=m_text, title = "About")

def get_readme_generator():
    rg_text = "\
The user needs to enter a length value for their password and a brief name or description for the service for which they wish to create a password for.\n\
By clicking the <Generate password> button, the password will be written to the password file."
    messagebox.showinfo(message=rg_text, title = "ReadMe PW-Generator")

def get_readme_safe():
    rs_text = "\
At first, the user needs to create a personal secret key via the File-menu.\n\
This key needs to be stored securely at all times.\n\
It serves as an encryption/decryption key for the password file.\n\
The encryption and decryption can be performed via the buttons in the File-menu.\n\
An already existing password can be entered via the <Existing password> and <Service-description> fields.\n\
Please note: The file has to be decrypted before making new entries. Otherwise no entry can be made!\n\
Procedure: Decrypt file -> Write to file -> Encrypt file again"
    messagebox.showinfo(message=rs_text, title = "ReadMe PW-Safe")

def genPw():
        length = int(pw_length.get())
        service = description.get()
        password = create_password(length)
        password = shuffle(password, length)
        option_label.config(text=f"Password for service {service} written to {pwfile_location}")
        write_password(password, service)

def addPw():
        user_pass = existing_pass.get()
        existing_service = existing_description.get()
        existing_password = user_pass
        option_label.config(text=f"Password for service {existing_service} written to {pwfile_location}")
        write_password(existing_password, existing_service)

# Button actions
def button_action_keygen():
    key_gen()
    option_label.config(text=f"{key_location} has been created. Keep secure at all times!")

def button_action_enc():
    encrypt_file()
    option_label.config(text="Encrypted successfully!")

def button_action_dec():
    decrypt_file()
    option_label.config(text="Decrypted successfully!")    

def button_action_genpw():
    if not(pwfile_path.is_file()):
        genPw()
    elif not (os.access(pwfile_location, os.W_OK)):
        option_label.config(text=f"{pwfile_location} is set to read-only mode. Please decrypt first!")
    else:
        genPw()

def button_action_add_exist_pw():
    if not(pwfile_path.is_file()):
        addPw()
    elif not (os.access(pwfile_location, os.W_OK)):
        option_label.config(text=f"{pwfile_location} is set to read-only mode. Please decrypt first!")
    else:
        addPw()

# Show or hide password input
def show_hide_pwd():
    if(visibility.get()):
        existing_pass.config(show="")
    else:
        existing_pass.config(show="*") 

# Create window and title
window = Tk()
window.title("PyPassHelper")

# Headline and hint
headline_label = Label(window, text="A random-password generator and password safe written in Python!")
option_label = Label(window, text="Please enter corresponding values!")

# Create file and help menu
menu = Menu(window)
file_menu = Menu(menu, tearoff=0)
help_menu = Menu(menu, tearoff=0)

file_menu.add_command(label="Generate Secret Key File", command=button_action_keygen)
file_menu.add_separator()
file_menu.add_command(label="Encrypt File", command=button_action_enc)
file_menu.add_separator()
file_menu.add_command(label="Decrypt File", command=button_action_dec)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

help_menu.add_command(label="Open Generator ReadMe", command=get_readme_generator)
help_menu.add_separator()
help_menu.add_command(label="Open Safe ReadMe", command=get_readme_safe)
help_menu.add_separator()
help_menu.add_command(label="About", command=get_info_dialog)

# Buttons
pwgen_button = Button(window, text="Generate password", command=button_action_genpw)
userpw_button = Button(window, text="Add existing password", command=button_action_add_exist_pw)

# Hidden password button
visibility = IntVar()
pw_visibility_button = Checkbutton(window, text ="Show", variable=visibility, onvalue=1, offvalue=0,
                             height=2, width=5, command=show_hide_pwd)

# Labels
length_label = Label(window, text="Password-length: ")
pw_length = Entry(window, bd=5, width=40)

description_label = Label(window, text="Service-description: ")
description = Entry(window, bd=5, width=40)

existing_pass_label = Label(window, text="Existing password: ")
existing_pass = Entry(window, bd=5, width=40, show="*")

existing_description_label = Label(window, text="Service-description: ")
existing_description = Entry(window, bd=5, width=40)

# Add to window
headline_label.grid(row=0, column=2, pady=20, padx= 0)
option_label.grid(row=1, column=2, pady=0, padx=0)

pwgen_button.grid(row=3, column=4, pady=20, padx=20)
userpw_button.grid(row=5, column=4, pady=20, padx=20)

length_label.grid(row=3, column=0, pady=0, padx=0)
pw_length.grid(row=3, column=1, pady=0, padx=0)

description_label.grid(row=3, column=2, pady=0, padx=0)
description.grid(row=3, column=3, pady=0, padx=0)

existing_pass_label.grid(row=5, column=0, pady=0, padx=0)
existing_pass.grid(row=5, column=1, pady=0, padx=0)

existing_description_label.grid(row=5, column=2, pady=0, padx=0)
existing_description.grid(row=5, column=3, pady=0, padx=0)

pw_visibility_button.grid(row=6, column=0, pady=0, padx=0)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Help", menu=help_menu)

window.config(menu=menu)  

# Main loop
window.mainloop()
