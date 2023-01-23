# Author      : Dario Masante
# Date     : 2019-04-18
# Dependencies:
# Reverse : DB_extraction.R
# Purpose  : obscure and decode user:password combos with encoding (user)
# and encryption (password) and use of a portable yaml file
## ATTENTION: despite hashing, passwords encoded this way are not entiraly safe
## to be exposed to the world (no "salt" included to make the hash)
# Example: obscure('masterKey','E:/test.yml','schema0:pass0','schema1:pass1')
# From cmd: python obfuscate.py decode masterkey E:/test.yml aSchema

'''
Login with production user credentials on server, then execute from terminal the following (edit items within square brackets [ ]):
   python3 .../obfuscate.py encode [masterkey /home/t.yml schema:pass]
   python3 .../obfuscate.py make_nopass [masterkey]
These encrypt the schema:pass combo into a given .yml file, and store also the masterkey encrypted inside the user home. To test, try the following, which should return the pass associated to the schema requested from the encrypted file.
   python3 .../obfuscate.py get_nopass [/home/t.yml schema]

Now that the system is setup,  any program to retrieve schema:pass combo without typing the masterkey will load module obfuscate.py and execute the following function:
get_nopass('/home/t.yml', 'schema')
This will return a dictionary: {'schema': 'pass'}
'''

import os
import sys
import subprocess
import yaml, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import pwd


## Function to encrypt or decipher a string.
# key is the master password
# text is the string to encrypt
# encrypt : True to encrypt, False to decrypt an encrypted string with the key
def string_interpreter(text, key, encrypt=False):
    if not isinstance(text, bytes):
        text = text.encode()
    if not isinstance(key, bytes):
        key = key.encode()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key)
    dkey = base64.urlsafe_b64encode(digest.finalize())
    f = Fernet(dkey)
    if encrypt:
        return f.encrypt(text)
    else:
        return f.decrypt(text)

## Function to encode user:password items and save it to a yml file.
# full_path is the .yml file storing encoded id:password combos (creates file if not existing)
# key is the master password
# *args is a dictionary or a (list of) string of id and password combo, provided as 'schema:pass','schema2:pass2', etc.
def encode(key, full_path, *args):
    if len(args) > 0:
        exFile = os.path.isfile(full_path)
        d = dict()
        dictionary = type(args[0]) is dict
        if dictionary or type(args[0]) is list:
            args = args[0]
        try:
            for a in args:
                if dictionary:
                    schema = a
                    pw = args[a]
                else:
                    sp = a.split(":")
                    schema = sp[0]
                    pw = sp[1]
                enc_pw = string_interpreter(pw, key, encrypt=True).decode()
                if exFile:
                    rec = raw_string(key, full_path, schema)
                    if len(rec) > 0: # change existing, don't add
                        enc_schema = list(rec)[0]
                    else:
                        enc_schema = string_interpreter(schema, key, encrypt=True).decode()
                else:
                    enc_schema = string_interpreter(schema, key, encrypt=True).decode()
                d[enc_schema] = enc_pw
        except:
            pass
        if exFile:
            with open(full_path) as outfile:
                f = yaml.safe_load(outfile)
            f.update(d)
        else:
            f = d
        if sys.version_info > (3, 0):
            with open(full_path, "w", encoding="utf8") as outfile:
                yaml.safe_dump(f, outfile)
        else:
            with open(full_path, 'wb') as outfile:
                yaml.safe_dump(f, outfile)
        outfile.close()
        return d

## Function to retrieve a password providing the user part, with the master password and the yml file to look at.
## Returns a dictionary
# key : the master password
# full_path : the .yml file storing encoded id:password combos
# *args : the id for which retrieve the password, e.g. the oracle schema to access in form of 'a','b',... or as list.
def decode(key, full_path, *args):
    with open (full_path) as f:
        d = yaml.safe_load(f)
    if type(args[0]) is list:
        args = args[0]
    o = dict()
    for i in d: # search encoded schema and get string
        try:
            decoded_schema = string_interpreter(i, key).decode()
        except:
            pass
        else:
            for req_schema in args:
                if req_schema == decoded_schema:
                    p = string_interpreter(d[i], key).decode()
                    o[req_schema] = p
    return o

## Same function as decode, but will return the encrypted string of requested id:password combo.
## Returns a dictionary
# key : the master password
# full_path : the .yml file storing encoded id:password combos
# *args : the id for which retrieve the password, e.g. the oracle schema to access in form of 'a','b',... or as list.
def raw_string(key, full_path, *args):
    with open (full_path) as f:
        d = yaml.safe_load(f)
    if type(args[0]) is list:
        args = args[0]
    o = dict()
    for i in d: # search encoded schema and get string
        try:
            decoded_schema = string_interpreter(i, key).decode()
        except:
            pass
        else:
            for req_schema in args:
                if req_schema == decoded_schema:
                    o[i] = d[i]
    return o

## Function to access and decode passwords in enabled user/machine combos, without the need
## to type or hardcode passwords.
# id : the service id for which to retrieve the password, e.g. the oracle schema to access
# full_path : the .yml file storing encoded id:password combos
# use_keyring : should use keyring module and system vault instead of yml file?
# self_path : path to the yaml file to identify itself. Defaults to the user home directory.
def get_nopass(full_path, id, use_keyring=False, self_path=None):
    if os.name == 'nt': # check Windows OS
        myself = os.getenv('username')
        uid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        fdir = 'C:/Users/' + myself + '/myself.yml'
    else:
        myself = pwd.getpwuid(os.getuid()).pw_name
        uid = open('/var/lib/dbus/machine-id','r').read().split('\n')[0]
        fdir = '/home/' + myself + '/myself.yml'
    if use_keyring:
        pass
    else:
        if self_path != None:
            fdir = self_path
        k = decode(myself, fdir, uid)[uid]
    o = decode(k, full_path, id)
    return o

## Function to encrypt a master password and enable a given user/machine to access id:password combos
## without the need to type or hardcode passwords.
# key : the password to hide
# delete : do you need to delete the current master password?
# use_keyring : should use keyring module and system vault instead of yml file?
# self_path : path to the yaml file to identify itself. Defaults to the user home directory
def make_nopass(key, delete=False, use_keyring=False, selfpth=None):
    if os.name == 'nt':
        myself = os.getenv('username')
        uid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        fdir = 'C:/Users/' + myself + '/myself.yml'
    else:
        myself = pwd.getpwuid(os.getuid()).pw_name
        uid = open('/var/lib/dbus/machine-id','r').read().split('\n')[0]
        fdir = '/home/' + myself + '/myself.yml'
    if use_keyring:
        pass
    else:
        if selfpth != None:
            fdir = selfpth
        if delete:
            k = decode(myself, fdir, uid)[uid]
            if k == key:
                os.remove(fdir)
        else:
            comb = uid + ':' + key
            encode(myself, fdir, comb)

## Function to change the master password, thus updating the dependent yml
# old: the old master password
# new: the new master password
# full_path: the .yml file containing the words to re-encode
def change_key(old, new, full_path):
    with open (full_path) as f:
        d = yaml.safe_load(f)
    newd = dict()
    for i in d: # loop through keys, decode and re-encode
        try:
            id = string_interpreter(i, old)
            p = string_interpreter(d[i], old)
            if sys.version_info > (3, 0):
                id = id.decode()
                p = p.decode()
            id = string_interpreter(id, new, encrypt=True).decode()
            newd[id] = string_interpreter(p, new, encrypt=True).decode()
        except:
            newd[i] = d[i] # print('Password provided does not match current password')
    if(len(id) > 0):
        if sys.version_info > (3, 0):
            with open(full_path, "w", encoding="utf8") as outfile:
                yaml.safe_dump(newd, outfile)
        else:
            with open(full_path, 'wb') as outfile:
                yaml.safe_dump(newd, outfile)
        outfile.close()

if __name__ == "__main__":
    args = list(sys.argv[0:])
    if os.name != 'nt':  # check if not windows machine
        import pwd  # needed only for linux
    what = args[1]
    if what == 'decode':
        print(decode(args[2], args[3], args[4:]))
    if what == 'obfuscate':
        print(string_interpreter(args[3], args[2], True))
    if what == 'revert':
        print(string_interpreter(args[3], args[2], False))
    if what == 'encode':
        print(encode(args[2], args[3], args[4:]))
    if what == 'get_nopass':
        print(get_nopass(args[2], args[3:]))
    if what == 'make_nopass':
        if len(args) > 3:
            if args[3] == 'delete':
                i = 1
                d = True
            else:
                i = 0
                d = False
            if len(args) > 4+i:
                usek = args[3+i]
            else:
                usek = False
            if len(args) == 5+i:
                sp = args[4+i]
            else:
                sp = None
            make_nopass(args[2], delete=d, use_keyring=usek, selfpth=sp)
        else:
            make_nopass(args[2])
        print('Master password encrypted successfully.')
    if what == 'change':
        change_key(args[2], args[3], args[4])
        print('Master password changed successfully')
