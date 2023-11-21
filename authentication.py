# crypotgraphic hash functions library
import hashlib as HL
import database_manager as dbm
def crypt_hashing(value):
    # perform the cryptographic SHA3_512
    # hash_object
    sha3 = HL.sha3_512()
    encoded_value = value.encode()
    sha3.update(encoded_value)
    return sha3.hexdigest()

def login(UID, PWD):
    # UID is the userName
    # PWD is the password

    # Fetch the stored SHA3_512 hash value from the database
    fetched_hash_value, telegram_mobile_no = dbm.fetch(UID)
    if fetched_hash_value == False:
        return False
    
    # compute the SHA3_512 hash value of the password obtained
    computed_hash_value = crypt_hashing(PWD)

    # comparision
    if computed_hash_value == fetched_hash_value:
        # write the code for 2FA or OTP verification
        return True
    return False

def signup(UID, PWD, telegram_mobile_no):
    '''
        rtype: True or False
        True: If successfull signup done
        False: 
    '''
    computed_hash_value, _ = dbm.fetch(UID)
    if computed_hash_value == False:
        pwd_hash_value = crypt_hashing(PWD)
        dbm.write(UID, pwd_hash_value, telegram_mobile_no)
        return True
    else:
        return False
