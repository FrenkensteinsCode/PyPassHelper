from PyPassHelper_backend import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import platform

# Info and ReadMe functions
def get_info_dialog():
    m_text = "\
**********************\n\
Title: PyPassHelper\n\
Author: @FrenkensteinsCode\n\
Version: 1.3.2\n\
**********************"
    messagebox.showinfo(message=m_text, title = "About")

def get_readme_generator():
    rg_text = "\
The user needs to enter a length value for their password and a brief name or description for the service for which they wish to create a password for.\n\
\n\
By clicking the <Generate password> button, the password will be written to the password file. The checkbutton <Passphrase> can be pressed in order to generate a \n\
passphrase consisting of random words of the wordlists instead of a password. In this case, the length is not needed as an input.\n\
\n\
The password-file can be stored anywhere the user wants. It can be selected via the appropriate file browser."
    messagebox.showinfo(message=rg_text, title = "ReadMe PW-Generator")

def get_readme_safe():
    rs_text = "\
At first, the user needs to create the PyPassHelper directory at the default location via the File-menu.\n\
Afterwards, the user needs to create a personal secret key via the File-menu. This key needs to be stored securely at all times.\n\
The key as well as the password file can be stored anywhere the user wants. It can later be selected via the appropriate file browser. The key serves as an encryption/decryption key for the password file.\n\
\n\
The encryption and decryption can be performed via the buttons in the File-menu. The File-menu can also be used to view the contents of the password file.\n\
\n\
An already existing password can be entered via the <Existing password> and <Service-description> fields. Please note: The file has to be decrypted before making new entries. Otherwise no entry can be made!\n\
\n\
Procedure: Decrypt file -> Write to file -> Encrypt file again"
    messagebox.showinfo(message=rs_text, title = "ReadMe PW-Safe")

def genPw():
    try:
        length = int(pw_length.get())
        service = description.get()
        password = create_password(length)
        password = shuffle(password, length)
        option_label.config(text=f"Password for service {service} written to {get_pwfile_location()}")
        write_password(password, service)
    except ValueError:
        option_label.config(text=f"Oops, something went wrong. Did you set the Password-length?")

def genPp():
    if platform.system() == "Windows":
        separator = "\\"
    else:
        separator ="/"

    l1 = os.getcwd() + separator + "wordlists" + separator + "word1_list.txt"
    l2 = os.getcwd() + separator + "wordlists" + separator + "word2_list.txt"
    l3 = os.getcwd() + separator + "wordlists" + separator + "word3_list.txt"
    l4 = os.getcwd() + separator + "wordlists" + separator + "word4_list.txt"

    service = description.get()
    passphrase = create_passphrase_from_wordlists([l1,l2,l3,l4])
    option_label.config(text=f"Passphrase for service {service} written to {get_pwfile_location()}")
    write_password(passphrase, service)

def addPw():
    user_pass = existing_pass.get()
    existing_service = existing_description.get()
    existing_password = user_pass
    option_label.config(text=f"Password for service {existing_service} written to {get_pwfile_location()}")
    write_password(existing_password, existing_service)

def strength_check():
    password = existing_pass.get()
    strength = check_password_strength(password)
    strength_label.config(text=f"Password-strength: {strength}")

# Button actions
def button_action_keygen():
    key_dir = os.path.dirname(key_location)
    try:
        key_gen()
        option_label.config(text=f"{key_location} has been created. Keep secure at all times!")
    except FileNotFoundError:
        option_label.config(text=f"The directory {key_dir} has not been found.\nPlease make sure it exists before creating a new key.")

def button_action_pwdirgen():
    default_pwdir_gen()
    option_label.config(text=f"{path} has been created.")

def button_action_enc():
    encrypt_file()
    option_label.config(text="Encrypted successfully!")

def button_action_dec():
    decrypt_file()
    option_label.config(text="Decrypted successfully!")

def button_action_open_file():
    pw_file = get_pwfile_location()
    if(os.path.isfile(pw_file)):
        if platform.system() == "Windows":
            os.system(f"start {pw_file}")
        else:
            os.system(f"xdg-open {pw_file}")
        option_label.config(text=f"Opened file at {pw_file}")
    else:
        option_label.config(text=f"No password file found at {pw_file}")

def button_action_genpw():
    pwfile_path = Path(get_pwfile_location())
    if not(pwfile_path.is_file()):
        if(secret_type.get()):
            genPp()
        else:
            genPw()
    elif not (os.access(get_pwfile_location(), os.W_OK)):
        option_label.config(text=f"{get_pwfile_location()} is set to read-only mode. Please decrypt first!")
    else:
        if(secret_type.get()):
            genPp()
        else:
            genPw()

def button_action_add_exist_pw():
    pwfile_path = Path(get_pwfile_location())
    if not(pwfile_path.is_file()):
        addPw()
    elif not (os.access(get_pwfile_location(), os.W_OK)):
        option_label.config(text=f"{get_pwfile_location()} is set to read-only mode. Please decrypt first!")
    else:
        addPw()

def button_action_browse_key_file():
    key_location = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select secret key",
                                          filetypes = (("Key files", "*.key"),
                                                        ("All files", "*.*")))
    s_key_loc_label.configure(text = "Currently selected secret key: " + key_location)
    update_key_location(key_location)
    
def button_action_browse_pw_file():
    pwfile_location = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select password file",
                                          filetypes = (("Text files", "*.txt"),
                                                        ("All files", "*.*")))
    pw_file_loc_label.configure(text = "Currently selected password file: " + pwfile_location)
    update_pwfile_location(pwfile_location)

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
headline_label = Label(window, text="A lightweight password-manager written in Python!")
option_label = Label(window, text="Please enter corresponding values!")

# Create file and help menu
menu = Menu(window)
file_menu = Menu(menu, tearoff=0)
help_menu = Menu(menu, tearoff=0)

file_menu.add_command(label="Generate PyPassHelper Directory", command=button_action_pwdirgen)
file_menu.add_separator()
file_menu.add_command(label="Generate Secret Key File", command=button_action_keygen)
file_menu.add_separator()
file_menu.add_command(label="Encrypt File", command=button_action_enc)
file_menu.add_separator()
file_menu.add_command(label="Decrypt File", command=button_action_dec)
file_menu.add_separator()
file_menu.add_command(label="Open File", command=button_action_open_file)
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
strength_check_button = Button(window, text="Check", command=strength_check)
select_key_button = Button(window, text="Browse secret key", command=button_action_browse_key_file)
select_pw_button = Button(window, text="Browse password file", command=button_action_browse_pw_file)

# Hidden password button
visibility = IntVar()
pw_visibility_button = Checkbutton(window, text ="Show", variable=visibility, onvalue=1, offvalue=0,
                                   height=2, width=5, command=show_hide_pwd)

# Button to switch between password and passphrase
secret_type = IntVar()
switch_word_to_phrase_button = Checkbutton(window, text ="Passphrase", variable=secret_type, onvalue=1, offvalue=0,
                                           height=4, width=10)

# Labels
length_label = Label(window, text="Password-length: ")
pw_length = Entry(window, bd=5, width=40)

description_label = Label(window, text="Service-description: ")
description = Entry(window, bd=5, width=40)

existing_pass_label = Label(window, text="Existing password: ")
existing_pass = Entry(window, bd=5, width=40, show="*")

existing_description_label = Label(window, text="Service-description: ")
existing_description = Entry(window, bd=5, width=40)

s_key_loc_label = Label(window, text = f"Default location is:  {get_key_location()}")
s_key_loc = Entry(window, bd=5, width=40)

pw_file_loc_label = Label(window, text = f"Default location is: {get_pwfile_location()}")
pw_file_loc = Entry(window, bd=5, width=40)

strength_label = Label(window)

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
switch_word_to_phrase_button.grid(row=3, column=5, pady=0, padx=0)

strength_check_button.grid(row=6, column=1, pady=0, padx=0)
strength_label.grid(row=7, column=1, pady=0, padx=0)

s_key_loc_label.grid(row=8, column=1, pady=0, padx=0)
pw_file_loc_label.grid(row=9, column=1, pady=10, padx=0)

select_key_button.grid(row=8, column=0, pady=0, padx=0)
select_pw_button.grid(row=9, column=0, pady=10, padx=20)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Help", menu=help_menu)

window.config(menu=menu)  
