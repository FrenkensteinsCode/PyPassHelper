# PyPassHelper
A random-password generator and password safe written in Python!

## Prerequisites
* Python3
* cryptography-module (<code>pip install cryptography</code>)

## Usage
* Download or clone the repository to your disk
* Execute the frontend-file of PyPassHelper
  * <code>Python3 .\PyPassHelper_frontend.py</code>
* To exit the program, click the X or go to File -> Exit

## Password Generator
The user needs to enter a length value for their password and a brief name or description for the service for which they wish to create a password for. By clicking the "Generate password" button, the password will be written to the password file. The checkbutton "Passphrase" can be pressed in order to generate a passphrase consisting of random words of the wordlists instead of a password. In this case, the length is not needed as an input.

## Password Safe
At first, the user needs to create a personal secret key via the File-menu. This key needs to be stored securely at all times. It serves as an encryption/decryption key for the password file. The encryption and decryption can be performed via the buttons in the File-menu. An already existing password can be entered via the "Existing password" and "Service-description" fields.

Please note: The file has to be decrypted before making new entries. Otherwise no entry can be made!

Procedure: Decrypt file -> Write to file -> Encrypt file again

## Considerations
This program has been tested on Windows 10 (22H2) and Linux (kali-rolling 2023.3) so far.

## Preview
![PyPassHelper](https://github.com/FrenkensteinsCode/PyPassHelper/assets/145868868/c005e93b-2b84-4d7e-b316-425b546fd87d)
