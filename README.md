# PyPassHelper
A lightweight password-manager written in Python!

## Prerequisites
* Python3
* cryptography-module (<code>pip install cryptography</code>)

## Usage
* Download or clone the repository to your disk
* Execute the PyPassHelper-file
  * <code>Python3 .\PyPassHelper.py</code>
* To exit the program, click the X or go to File -> Exit

## Password Generator
The user needs to enter a length value for their password and a brief name or description for the service for which they wish to create a password for.

By clicking the "Generate password" button, the password will be written to the password file. The checkbutton "Passphrase" can be pressed in order to generate a passphrase consisting of random words of the wordlists instead of a password. In this case, the length is not needed as an input.

The password-file can be stored anywhere the user wants. It can be selected via the appropriate file browser.

## Password Safe
At first, the user needs to create the PyPassHelper directory at the default location via the File-menu.
Afterwards, the user needs to create a personal secret key via the File-menu. This key needs to be stored securely at all times. The key as well as the password file can be stored anywhere the user wants. It can later be selected via the appropriate file browser. The key serves as an encryption/decryption key for the password file.

The encryption and decryption can be performed via the buttons in the File-menu. The File-menu can also be used to view the contents of the password file.

An already existing password can be entered via the "Existing password" and "Service-description" fields. Please note: The file has to be decrypted before making new entries. Otherwise no entry can be made!

Procedure: Decrypt file -> Write to file -> Encrypt file again

## Considerations
This program has been tested on the following platforms:
- Windows 10 (22H2) - Python 3.11.2
  - WSL (kali-rolling 2024.2) - Python 3.11.8
- Windows 11 (23H2) - Python 3.11.2
- Rocky Linux 8.10 - Python 3.12.3

## Preview
![image](https://github.com/user-attachments/assets/ab5bd79f-61d7-4e18-aa3c-24d0db402035)
