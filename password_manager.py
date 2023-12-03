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
    log_file.write("SignUp on {}\n".format(cur_time_readable))
    log_file.close()

    # time file
    time_file = open(location + "/KWD_User_Profiles/{}/time.txt".format(UID), "w")
    time_file.close()

# appending new login credential
def append(UID, masterpassword, loginID, PWD = "", text = "Untitled Text", generate = False):
    location = os.path.abspath("")
    # generate the salt
    salt = PG.password_generator()
    
    # expiry date : time period = 3 months 
    # 3 mnths = 3 * 4 weeks = 3 * 4 * 7 days = 3 * 4 * 7 * 24 hrs = 3 * 4 * 7 * 24 * 3600 secs
    expiry_time = time.time() +  float(3 * 4 * 7 * 24 * 3600)

    # unique identifier: <UID>@<time_from_epoch>
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
    
    log_file = open(location + "\KWD_User_Profiles\{}\log.txt".format(UID), "a")
    log_file.write("New Login credential added '{}' on {}\n".format(text, time.ctime(time.time())))
    log_file.close()
    return True

# profile_generator("8637293605")
# append("8637293605", "890", "khritish", "password", "Keywarden")
# append("8637293605", "890", "khritish34", "password", "Keywarden", True)

# deleting existing login credential
def delete(identifier):
    UID = identifier.split('@')[0]
    user_profile_location = os.path.abspath("") + "/KWD_User_Profiles/{}".format(UID)
    
    # delete the credential entry in credential.txt
    cred = open(user_profile_location + "/credential.txt", "r")
    log_file = open(user_profile_location + "/log.txt".format(UID), "a")
    lines = cred.readlines()
    cred.close()
    # print(lines)
    index_no = None
    text = None
    for i in range(len(lines)):
        line = lines[i]
        uniq_identifier = line.split("\u00b6")[0]
        text = line.split("\u00b6")[1]
        if uniq_identifier == identifier:
            index_no = i
            break
    try:
        del lines[index_no]
    except:
        log_file.write("Unsuccessful attempt to delete an non-existing credential\n")
        return False
    
    cred = open(user_profile_location + "/credential.txt", "w")
    for line in lines:
        cred.write(line)
    cred.close()
    
    # delete the .enc encryption file
    try:
        os.remove(user_profile_location + "/{}.enc".format(identifier))
    except:
        log_file.write("Unsuccessful attempt to delete '{}' credential on {}\n".format(text, time.ctime(time.time())))
        return False
    log_file.write("Successfully deleted '{}' credential on {}\n".format(text, time.ctime(time.time())))
    log_file.close()
    return True
# delete("8637293605@17009268400332103")

# requesting the login id and the password against the identifier
def request(identifier, masterpassword):
    UID = identifier.split('@')[0]
    user_profile_location = os.path.abspath("") + "/KWD_User_Profiles/{}".format(UID)
    
    # get the loginId from the credential.txt with the given identifier
    cred = open(user_profile_location + "/credential.txt", "r")
    loginId = None
    salt = None
    text = None
    while True:
        line = cred.readline()
        temp_identifier = line.split('\u00b6')[0]
        if temp_identifier == identifier:
            loginId = line.split('\u00b6')[2]
            salt = line.rstrip('\n').split('\u00b6')[4]
            text = line.split('\u00b6')[1]
            break
    cred.close()

    # now get the E2_PWD and decrypt using the masterpassword
    encrypted_PWD = open(user_profile_location + "/{}.enc".format(identifier), "rb")
    E2_PWD = encrypted_PWD.readline()
    encrypted_PWD.close()
    PWD = password_decryption(E2_PWD, masterpassword, salt)
    
    # writing in the log file 
    log_file = open(user_profile_location + "/log.txt".format(UID), "a")
    log_file.write("Requested the credential for {} on {}\n".format(text, time.ctime(time.time())))
    log_file.close()
    return loginId, PWD.decode()
# print(request(identifier="8637293605@17009268398154283", masterpassword="890"))

# requesting the identifier and text pairs of the given UID
def request_all(UID):
    user_profile_location = os.path.abspath("") + "/KWD_User_Profiles/{}".format(UID)
    
    # get the loginId from the credential.txt with the given identifier
    cred = open(user_profile_location + "/credential.txt", "r")
    identifier_text = {}
    for line in cred.readlines():
        identifier, text = line.split('\u00b6')[0], line.split('\u00b6')[1]
        identifier_text[identifier] = text
    # writing in the log file 
    log_file = open(user_profile_location + "/log.txt".format(UID), "a")
    log_file.write("Requested all credential for the user: '{}' on {}\n".format(UID, time.ctime(time.time())))
    log_file.close()
    return identifier_text
# print(request_all("8637293605"))
    


# updating an existing login credential
def update(identifier, masterpassword, new_PWD = "", new_text = None, generate_PWD = False, update_text = False, update_PWD = False):
    
    user_profile_location = os.path.abspath("") + "/KWD_User_Profiles/{}".format(UID)

    # get the credentials.txt entries
    cred = open(user_profile_location + "/credential.txt", "r")
    entries = cred.readlines()
    cred.close()
    
    if generate_PWD:
        new_PWD = PG.password_generator()
    
        # generate the salt
        salt = PG.password_generator()
        E2_PWD = password_encryption(new_PWD, masterpassword, salt)
        UID = identifier.split('@')[0]

    # find out which line should be updated
    update_index = None
    for i in range(len(entries)):
        line = entries[i]
        temp_identifier = line.split('\u00b6')[0] 
        if identifier == temp_identifier:
            update_index = i 
            break
    if update_index == None:
        return False
    
    # update that line
    line = entries[update_index]
    line = line.split('\u00b6')

    if update_text:
        line[1] = new_text
    if update_PWD:
        line[4] = salt

    line = "\u00b6".join(line, )
    entries[update_index] = line

    # put everything to credential file
    cred = open(user_profile_location + "/credential.txt", "w")
    for line in entries:
        cred.write(line)
    cred.close()

    if update_PWD:
        # generate the encryption file .enc
        encr = open(user_profile_location + "/{}.enc".format(identifier), "wb")
        encr.write(E2_PWD)
        encr.close()
    return True
# print(update("8637293605@17009268398154283", "890", generate=True))
# requesting the transaction history 
def history(UID):
    user_profile_location = os.path.abspath("") + "/KWD_User_Profiles/{}".format(UID)

    # log file 
    log_file = open(user_profile_location + "/log.txt".format(UID), "a")
    log_file.write("Requested the transaction history of user '{}' on {}\n".format(UID, time.ctime(time.time())))
    log_file.close()

    log_file = open(user_profile_location + "/log.txt".format(UID), "r")
    log = log_file.readlines()
    log_file.close()
    return log
# print(history("8637293605"))
