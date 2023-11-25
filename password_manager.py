import aes_cryptography as aes
import os 
import aes_cryptography as crypt
import time 
import password_generator as PG
'''
    PDW and salt should be in bytes and masterpassword should be a string
'''


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
# signs up -> redirect to profile generation
def profile_generator(UID):
    location = os.path.abspath("")
    dir_list = os.listdir(location)
    # first create the User profile directory if not created earlier,
    # usually happens at the begining of the KWD initiation 
    if "KWD_User_Profiles" not in dir_list:
        os.mkdir(location + "\KWD_User_Profiles")
    
    # create the user directory 
    # assuming previously the UID is unique, therefore there is no previous 
    # user profile on the same UID created
    os.mkdir(location + "\KWD_User_Profiles\{}".format(UID))

    # now create the credential file
    cred = open(location + "\KWD_User_Profiles\{}\credential.txt".format(UID), "w")
    cred.close()
    
    # log file
    log_file = open(location + "\KWD_User_Profiles\{}\log.txt".format(UID), "w")
    cur_time = time.time()
    cur_time_readable = time.ctime(cur_time)
    log_file.write("SignUp @ {}\n".format(cur_time_readable))
    log_file.close()

# appending new login credential
def append(UID, masterpassword, loginID, PWD = "", text = "Untitled Text", generate = False):
    location = os.path.abspath("")
    # generate the salt
    salt = PG.password_generator()
    
    # expiry date : time period = 3 months 
    # 3 mnths = 3 * 4 weeks = 3 * 4 * 7 days = 3 * 4 * 7 * 24 hrs = 3 * 4 * 7 * 24 * 3600 secs
    expiry_time = time.time() +  float(3 * 4 * 7 * 24 * 3600)

    # unique identifier: UID@DDMMYYHHMnMnSS
    curr_time = str(time.time())
    curr_time = curr_time.replace('.', '')
    identifier = "{}@{}".format(UID, curr_time)
    
    # double encrypted password, E2_PWD
    if generate == True:
        PWD = PG.password_generator()
    E2_PWD = password_encryption(PWD, masterpassword, salt)
    
    # create the User directory, if not generated already
    if not os.path.isdir(location + "\KWD_User_Profiles\{}".format(UID)):
        os.mkdir(location + "\KWD_User_Profiles\{}".format(UID))

    # add to the cred file
    cred = open(location + "\KWD_User_Profiles\{}\credential.txt".format(UID), "a")
    cred.write("{}\u00b6{}\u00b6{}\u00b6{}\u00b6{}\n".format(identifier, text, loginID, expiry_time, salt))
    cred.close()

    # generate the encryption file .enc
    encr = open(location + "\KWD_User_Profiles\{}\{}.enc".format(UID, identifier), "wb")
    encr.write(E2_PWD)
    encr.close()

    print(time.time())

# profile_generator("8637293605")
# append("8637293605", "890", "khritish", "password", "Keywarden")
# append("8637293605", "890", "khritish34", "password", "Keywarden", True)

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