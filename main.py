import getpass
import hashlib
import os
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_file(filename, key):
    key = hashlib.sha256(key.encode()).digest()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, "rb") as f:
        file_data = f.read()

    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    with open("enc_" + filename, "wb") as f:
        f.write(iv + encrypted_data)


def decrypt_file(filename, key):
    key = hashlib.sha256(key.encode()).digest()

    with open(filename, "rb") as f:
        file_data = f.read()

    iv = file_data[:16]
    encrypted_data = file_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)

    with open("dec_" + filename, "wb") as f:
        f.write(unpadded_data)


def print_help():
    help_text = """
Usage: python script.py <filename> <action>
<filename>   : The name of the file to encrypt or decrypt.
<action>     : "-e" to encrypt the file, "-d" to decrypt the file.

Example:
    python script.py file.txt -e
    python script.py file.txt -d
"""
    print(help_text)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] in ("--help", "-h"):
        print_help()
    else:
        filename = sys.argv[1]
        action = sys.argv[2]

        if not os.path.isfile(filename):
            print(f"Error: The file {filename} does not exist.")
            sys.exit(1)

        key = getpass.getpass(prompt="Enter the encryption/decryption key: ")

        if action == "-e":
            encrypt_file(filename, key)
            print(f"The file {filename} has been encrypted.")
        elif action == "-d":
            try:
                decrypt_file(filename, key)
                print(f"The file {filename} has been decrypted.")
            except ValueError:
                print("Error: Incorrect key.")
                sys.exit(1)
        else:
            print(f"Error: Unknown action {action}.")
            print_help()
            sys.exit(1)
