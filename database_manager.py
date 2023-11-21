import os
import time

def check_existance(location):
    # location = os.path.abspath("")
    # checking if the database file exist or not
    list_dir = os.listdir(location)
    if "KWD_Database_Files" not in list_dir:
        os.mkdir(location + "\KWD_Database_Files")
        file = open(location + "\KWD_Database_Files\semaphore.txt","w")
        file.write("unlocked")
        file.close()
    
def fetch(UID):
    '''
    rtype:  [1] Pillcrow symbol represents, UID doesn't exist
            [2] SHA3_256 hash value will be returned
    '''
    # a customary check for the existance of essential files
    location = os.path.abspath("")
    check_existance(location)
    location += "\KWD_Database_Files"
    first_char = UID[0]
    try:
        # .dbf file denote the database file
        file = open(location + "\{}.dbf".format(first_char) , "r")
        while True:
            line = file.readline()
            if not line:
                break
            user_id, hash_value, tele_mob_no = line.rstrip("\n").split("\u00b6")
            if user_id == UID:
                return hash_value, tele_mob_no
        # such UID doesn't exist
        file.close()
        return False, False
    except:
        # such database file is not present
        return False, False

def write(UID, PWD_hash_value, telegram_mobile_no):
    '''
    rtype:  None
    '''
    # a customary check for the existance of essential files
    location = os.path.abspath("")
    check_existance(location)
    location += "\KWD_Database_Files"
    first_char = UID[0]
    
    # check for the semaphores locking mechanism
    while True: 
        semaphore = open(location + "\semaphore.txt", "r")
        status = semaphore.readline()
        if status == "unlocked":
            semaphore.close()
            break
        semaphore.close()
    
        # waits for 1 milliseconds
        time.sleep(0.001)
    
    # we write the UID and PWD hash value
    # locking the database, so that no two write operations happens simulataneously
    semaphore = open(location + "\semaphore.txt", "w")
    semaphore.write("locked")
    semaphore.close()
    try:
        # opening the dbf file in append, if it exists
        file = open(location + "\{}.dbf".format(first_char), "a")
        file.write("{}\u00b6{}\u00b6{}\n".format(UID, PWD_hash_value, telegram_mobile_no))
        file.close()
    except:
        # if the dbf file does not exist
        # then create it
        file = open(location + "\{}.dbf".format(first_char), "w")
        file.write("{}\u00b6{}\n".format(UID, PWD_hash_value))
        file.close()
    
    # unlocking the database
    semaphore = open(location + "\semaphore.txt", "w")
    semaphore.write("unlocked")
    semaphore.close()


