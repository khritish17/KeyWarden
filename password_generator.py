import time
import secrets
import math 

character_pool = [  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                     'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
                    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 
                    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                    ['!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '+', '=',
                     '{', '}', '[', ']', '<', '>', '?'] ]

def generate_cryptographic_random_number(start, end):
    # Ensure that the range is valid
    if not (isinstance(start, int) and isinstance(end, int) and start <= end):
        raise ValueError("Invalid range")

    # Calculate the range size
    range_size = end - start + 1

    # Calculate the number of bytes needed to represent the range
    num_bytes = (range_size.bit_length() + 7) // 8

    # Generate a random number using secrets
    random_number = int.from_bytes(secrets.token_bytes(num_bytes), 'big') % range_size

    # Map the random number to the specified range
    mapped_number = start + random_number

    return mapped_number

def password_generator():
    # setting the length for the password: length varies from 16 - 19
    length = 16 + int(time.gmtime().tm_sec % 4)
    
    secure_password = ""
    char_category = 0
    for i in range(length):
        char_category = generate_cryptographic_random_number(0, 3)
        char_index_limit = 0
        if char_category == 0:
            # lower case letters
            char_index_limit = len(character_pool[0]) - 1
            
        elif char_category == 1:
            # lower case letters
            char_index_limit = len(character_pool[1]) - 1

        elif char_category == 2:
            # numbers / single digit integers
            char_index_limit = len(character_pool[2]) - 1
        elif char_category == 3:
            # special characters
            char_index_limit = len(character_pool[3]) - 1 
            
        random_index = generate_cryptographic_random_number(0, char_index_limit)
        secure_password += character_pool[char_category][random_index]

    return secure_password

def entropy(PWD):
    length = len(PWD)
    characters =[0, 0, 0, 0] # 0: lower case, 1: upper case, 2: numbers, 3: special characters
    for char in PWD:
        if char in character_pool[0]:
            characters[0] = 1
        elif char in character_pool[1]:
            characters[1] = 1
        elif char in character_pool[2]:
            characters[2] = 1
        elif char in character_pool[3]:
            characters[3] = 1
    count = 0
    if characters[0] == 1:
        count += len(character_pool[0])
    if characters[1] == 1:
        count += len(character_pool[1])
    if characters[2] == 1:
        count += len(character_pool[2])
    if characters[3] == 1:
        count += len(character_pool[3])
    entropy = math.log2(count) * length
    return int(entropy)

# pwd = password_generator()
# print("{} = {}".format(pwd, entropy(pwd)))
