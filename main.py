# import wmi
#
# # Initializing the wmi constructor
# f = wmi.WMI()
#
# # Printing the header for the later columns
# print("pid   Process name")
#
# # Iterating through all the running processes
# for process in f.Win32_Process():
#     # Displaying the P_ID and P_Name of the process
#     print(f"{process.ProcessId} {process.Name}")

import zlib
d={'24788': 'audiodg.exe'}
checksum=0
for item in d.items():
    c1 = 1
    for t in item:
        c1 = zlib.adler32(bytes(repr(t),'utf-8'), c1)
    checksum=checksum ^ c1

print(checksum)
# jhjh={'key3':'value4', 'key1':'value1'}
# checksum=0
# for item in d.items():
#     c1 = 1
#     for t in item:
#         c1 = zlib.adler32(bytes(repr(t),'utf-8'), c1)
#     checksum=checksum ^ c1
#
# print(checksum)


# from cryptography.fernet import Fernet
#
# # we will be encryting the below string.
# message = "hello geeks"
#
# # generate a key for encryptio and decryption
# # You can use fernet to generate
# # the key or use random key generator
# # here I'm using fernet to generate key
#
# key = Fernet.generate_key()
#
# # Instance the Fernet class with the key
#
# fernet = Fernet(key)
#
# # then use the Fernet class instance
# # to encrypt the string string must must
# # be encoded to byte string before encryption
# encMessage = fernet.encrypt(message.encode())
#
# print("original string: ", message)
# print("encrypted string: ", encMessage)
#
# # decrypt the encrypted string with the
# # Fernet instance of the key,
# # that was used for encrypting the string
# # encoded byte string is returned by decrypt method,
# # so decode it to string with decode methods
# decMessage = fernet.decrypt(encMessage).decode()
#
# print("decrypted string: ", decMessage)

# import csv
# with open("serviceList.csv", 'r') as file:
#     reader = csv.reader(file)
#     for line in reader:
#         print(line[0] + "," + line[1])

# f = open("status_log.txt", "r")
# lines = f.readlines()
# for line in lines:
#     print(line)
#     # print(line.strip())
#     # print(line.strip().split(' - '))
#     print(line.split()[0])
#     # print(type( line.strip()))

# dict_wed = {'24788': 'audiodg.exe'}





