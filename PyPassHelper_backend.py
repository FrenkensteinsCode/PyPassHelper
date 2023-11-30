from cryptography.fernet import Fernet
import math
import os
import random as rd
import stat

## File location routines
home_dir = os.path.expanduser("~")
path = os.path.join(home_dir, "PyPassHelper")
if not os.path.exists(path):
    os.makedirs(path)
key_location = os.path.join(path, "secret.key")
pwfile_location = os.path.join(path, "pwfile.txt")

## Password safe routines
def key_gen(key_location: str):
    ''' Generate an encryption/decryption key at the specified location
    
        Input:
            key_location: Location of encryption key (type: String)
    '''

    encryption_key = Fernet.generate_key()

    with open(key_location, 'wb') as enc_key_file:
        enc_key_file.write(encryption_key)

def encrypt_file():
    ''' Encrypt a file using a key-file.
        This function opens keyfile and writes its key to enc_key.
        Then it reads the original file, encrypts the content
        and writes the encrypted content back to the original file.
    '''

    with open(key_location, 'r') as enc_key_file:
        enc_key = enc_key_file.read()

    fernet = Fernet(enc_key)

    with open(pwfile_location, 'rb') as pwfile:
        original_file = pwfile.read()

    encrypted_content = fernet.encrypt(original_file)

    with open(pwfile_location, 'wb') as encrypted_pw_file:
        encrypted_pw_file.write(encrypted_content)

    os.chmod(pwfile_location, stat.S_IREAD) # Set file to read-only

def decrypt_file():
    ''' Decrypt a file using a key-file.
        This function opens keyfile and writes its key to dec_key.
        Then it reads the original file, decrypts the content
        and writes the decrypted content back to the original file.
    '''
    os.chmod(pwfile_location, stat.S_IRWXU) # Make file writable again

    with open(key_location, 'r') as dec_key_file:
        dec_key = dec_key_file.read()

    fernet = Fernet(dec_key)

    with open(pwfile_location, 'rb') as encrypted_pw_file:
        encrypted_file = encrypted_pw_file.read()

    decrypted_content = fernet.decrypt(encrypted_file)

    with open(pwfile_location, 'wb') as decrypted_pw_file:
        decrypted_pw_file.write(decrypted_content)

def check_password_strength(password: str) -> str:
    ''' Checks the strength of a user defined password and delivers a rating

        Input:
            password: User-defined password (type: String)

        Return: Rating of password strength (type: String)
    '''
    password_length = len(password)
    has_digit = any(char.isdigit() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_special_char = any(not char.isalnum() for char in password)

    characters = sum([has_digit, has_lowercase, has_uppercase, has_special_char]) * 26
    grade = math.log(characters ** password_length, 2) # Common Password entropy function: E = log_2(R^L)

    if grade >= 75:
        return "Excellent"
    elif grade >= 50:
        return "Good"
    elif grade >= 25:
        return "Weak"
    else:
        return "Very Weak"

## Password generator routines
def shuffle(char_string: str, length: int) -> str:
    ''' Shuffles a string of characters in order to randomize it

        Input:
            char_string: String of characters (type: String)
            length: User-defined length for the password (type: int)

        Return:
            Shuffled string of characters in given length (type: String)
    '''

    if not isinstance(char_string, str):
        raise TypeError(f'The value for the string (i.e. {char_string}) must be a string type')
    elif not isinstance(length, int):
        raise TypeError(f'The value for the length (i.e. {length}) must be a int type')
    else:
        temp_list = list(char_string)
        rd.shuffle(temp_list)
        return ''.join(temp_list)[:length]

def create_password(length: int) -> str:
    ''' Creates a string based on randomly chosen ASCII-characters

        Input:
            length: User-defined length for the password to guarantee minimum length (type: int)

        Return:
            String with randomly chosen ASCII-characters (type: String)
    '''

    if not isinstance(length, int):
        raise TypeError(f'The value for the length (i.e. {length}) must be a int type')
    else:
        password = ''

        for char in range(length):
            password += chr(rd.randint(33,43)) # Special characters
            password += chr(rd.randint(65,90)) # Upper case
            password += chr(rd.randint(97,122)) # Lower case
            password += chr(rd.randint(48,57)) # Numbers

        return password
    
def create_passphrase_from_wordlists(wordlists: list[str]) -> str:
    ''' Select random words from different wordlists and concatenate them in order to generate a passphrase.

        Input:
            wordlists: Python list containing the absolute paths of different wordlists. (type: list[str])

        Return:
            A passphrase containing randomly chosen words of given wordlists (type: String)
    '''
    if not isinstance(wordlists, list):
        raise TypeError(f'The value for the wordlists (i.e. {wordlists}) must be a list of strings')
    else:    
        random_words = []
        passphrase = ""
        for wordlist in wordlists:
            with open(wordlist) as w_l:
                full_text = w_l.read()
                words = list(map(str, full_text.split()))
                random_words.append(rd.choice(words))

        for word in random_words:
            passphrase += word

    return passphrase

def write_password(password: str, service: str, pwfile_location: str):
    ''' Generates or opens an exisiting password-file and stores a password and
        its corresponding service-name in it

        Input:
            password: The previously generated or given password (type: String)
            service: The user-given corresponding service name (type: String)
            pwfile_location: Location of password file (type: String)
    '''

    if not isinstance(password, str):
        raise TypeError(f'The value for the password (i.e. {password}) must be a string type')
    elif not isinstance(service, str):
        raise TypeError(f'The value for the service (i.e. {service}) must be a string type')
    else:
        file = open(pwfile_location, 'a+')
        file.write('Service: ' + service
                   + ' | Password: ' + password
                   + '\n')
        file.close()