import aes_cryptography as aes
import os 
import aes_cryptography as crypt
import time 

'''
    PDW and salt should be in bytes and masterpassword should be a string
'''
# signs up -> redirect to profile generation
def profile_generator(UID):
    location = os.path.abspath("")
    dir_list = os.listdir(location)
    # first create the User profile directory if not created earlier,
    # usually happens at the begining of the KWD initiation 
    if "KWD_User_Profiles" not in dir_list:
        os.mkdir(location)
    
    # create the user directory 
    # assuming previously the UID is unique, therefore there is no previous 
    # user profile on the same UID created
    os.mkdir(location + "\{}".format(UID))

    # now create the credential file
    cred = open(location + "\{}\credential.txt".format(UID))
    cred.clsoe()
    
    # profile summary
    profile_summary = open(location + "\{}\profile_summary.txt".format(UID))
    profile_summary.close()
    
    # log file
    log_file = open(location + "\{}\log.txt".format(UID))
    cur_time = time.time()
    cur_time_readable = time.ctime(cur_time)
    log_file.write("SignUp @ {}\n".format(cur_time_readable))
    log_file.close()

def password_encryption(PWD, masterpassword, salt):
    PWD = PWD.encode()
    salt = salt.encode()
    # private key for primary encryption
    pk1 = crypt.generate_high_entropy_key(masterpassword, salt)
    # E1_PWD is the primary encrypted PWD
    E1_PWD = crypt.aes_encrypt(pk1, PWD)

    # private key for secondary encryption
    pk2 = crypt.generate_high_entropy_key(masterpassword[::-1], salt)
    # E2_PWD is the secondary encrypted PWD
    E2_PWD = crypt.aes_encrypt(pk2, E1_PWD)
    return E2_PWD

def password_decryption(E2_PWD, masterpassword, salt):
    salt = salt.encode()
    # private key for secondary encryption
    pk2 = crypt.generate_high_entropy_key(masterpassword[::-1], salt)
    E1_PWD = crypt.aes_decrypt(pk2, E2_PWD)
    
    # private key for primary encryption
    pk1 = crypt.generate_high_entropy_key(masterpassword, salt)
    PWD = crypt.aes_decrypt(pk1, E1_PWD)
    return PWD

# pwd = "kjjgfdhiugfihhjl"
# master = "123"
# salt = "789khhjgg"
# cipher = password_encryption(pwd, master, salt)
# print(cipher)
# file = open('temp@0.bin', 'wb')
# file.write(cipher)
# file.close()

# file = open('temp@0.bin', 'rb')
# t = file.readline()
# file.close()
# print(t)
# # print(password_decryption(cipher, master, salt))
# print(password_decryption(t, master, salt))


# PWD password manager functions

# appending new login credential
def append():
    pass

# deleting existing login credential
def delete():
    pass

# requesting the login-PWD pairs
def request():
    pass

# updating an existing login credential
def update():
    pass

# requesting the transaction history 
def history():
    pass