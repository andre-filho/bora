import os
import getpass
from cryptography.fernet import Fernet
# from Crypto.Hash import SHA
# https://www.youtube.com/watch?v=H8t4DJ3Tdrg

def create_secure_key():  
    HOMEDIR = os.getenv('HOME')
    
    fp = HOMEDIR + '/.bora/'
    check_folder_structure(fp)
    path = fp + 'key.key'

    if os.path.isfile(path):        # this can be bugged
        return False
    else:
        key = Fernet.generate_key()
        file = open(path, 'wb+')
        file.write(key)
        file.close()
        return True     


def get_key():
    pass    


def check_folder_structure(full_path):
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def write_on_enc_file(github_key, gitlab_key):
    HOMEDIR = os.getenv('HOME')

    full_path = HOMEDIR + '/.bora/'
    fp = full_path + 'enc'

    check_folder_structure(full_path)

    try:
        arqv = open(fp, "a+")
        arqv.write(github_key)
        arqv.write(gitlab_key)
    finally:
        arqv.close()


def read_from_enc_file():
    pass


def encrypt(line, key):
    pass


def decrypt(line, key):
    pass
