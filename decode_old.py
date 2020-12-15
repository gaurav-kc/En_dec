# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to decrypt and recover all the files 
# The program reads the encrypted files and generates original files
# format of the entire (unchunked) is like this 
# a file is an array of bytes 
# <header> <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <semicolon seperated names of all files in same order>
# After the successful execution, a folder will contain all recovered files
# feel free to add any further improvements 

# TODO add chunks directly to google drive 
# TODO think upon compression algorithmns for different formats. Use auto encoders or something to compress images 
# TODO have an option for more robust process (say by including some metadata or recovery mechanisms). 
# TODO handle directory inside directory

import sys
import os
import json
import hashlib

# from your python file, import your class here.
from refer import myImplementation
# create an object of your implementation here and assign to lib
lib = myImplementation()

# default values
directory_name = "encrypted"
op_directory_name = "decrypted"
# chunksize = 10000 # from header only
# key = 200 # from header only
commonname = "bpsnecjkx" # TODO can be made an argument
delimeter = "_"
opformat = "gty"
# allowed_formats = ["jpg","png","jpeg"] # of no use here
endian = 'little'
current_dir = "./"
default_password = "pmqhfisbrkjcvklzxckliou" # should be same as while encoding
# presence of def password shows no password was given 

# flags 
# user need not remember whatever custom/default chunk value and key used while encrypting. Hence no flags for that
# if specified, first directory name will be assumed as input dir name and next as output directory name. Both are optional
# by default it would assume input from directory name mentioned in variable directory_name
# by default it would put all recovered files in directory mentioned in variable op_directory_name
# flags supported yet
# -d  (print debugging statements)
is_input_directory = False
is_output_directory = False
is_debug_mode = False
#handling the flags to set/overwrite default values
i = 1
while i < len(sys.argv):
    if sys.argv[i][0] == "-":
        flag = sys.argv[i].lstrip("-")
        if flag == "d":
            is_debug_mode = True
        # add new flags here 
        else:
            print("Invalid flag ",flag)
            exit(0)
    else:
        if is_input_directory == False:
            is_input_directory = True
            directory_name = sys.argv[i]
        elif is_output_directory == False:
            is_output_directory = True
            op_directory_name = sys.argv[i]
        else:
            print("Error in this argument",sys.argv[i])
            exit(0)
    i = i + 1


# we first construct the entire bytearray (combined of all chunks) and then start decoding it
if is_debug_mode:
    print("Decrypting ... ")
# check if given directory exists
dir_path = os.path.join(current_dir,directory_name)
if not os.path.exists(dir_path):
    print("Directory not found")
    exit(0)
if is_debug_mode:
    print("Looking for files in ",dir_path)
# this step is to avoid all other files apart from what we recognize as chunk
# we only take count of such files and assume the files are from 0 to filecount-1 (maybe not the best way)
all_files = os.listdir(dir_path)
filecount = 0
for afile in all_files:
    filename = afile.split(".")
    if len(filename) != 2:
        continue
    format = filename[-1]
    if format == opformat:
        filecount = filecount + 1

# print(filecount)    # debug purpose only 
if filecount == 0:
    print("No compatible files found")
    exit(0)
# TODO Put an extra check if filenames are from 0 to n-1 or not
if is_debug_mode:
    print("Number of chunks found is ",filecount)
# finalres will have the entire bytes 
finalres = bytearray()
for i in range(0,filecount):
    # i here is chunk number
    filename = commonname + delimeter + str(i) + "." + opformat
    filename = os.path.join(dir_path,filename)
    if not os.path.exists(filename):
        print(filename, " not found")
        exit(0) # bilkul ricks nai lene ka
    file_obj = open(filename,"rb")
    f = file_obj.read()
    b = bytearray(f)
    finalres = finalres + b     # append bytearray of current file to finalres
    file_obj.close() 
if is_debug_mode:
    print("Size of entire blob is ",len(finalres))
# print(len(finalres))  # debug only

# now we have the entire object. All chunks combined. Now we start decoding
# first decode the header. The header had filecount, chunksize, key and password.
# the index is kind of file pointer. Header size is not fixed yet, hence function should
# return an index which tells where header ends
opfilecount, chunksize, key, pass_bytes, index = lib.decodeHeader(finalres,endian)
if is_debug_mode:
    print("Header size is ",index)
# we need to check for password. 
# def_digest is hash for default password
# if it matches with the passowrd in header, it means no password was set
# but if it doesn't, password was set
def_digest = lib.getPassHash(default_password)

if def_digest != pass_bytes:
    #it was a protected file
    count = 3   #number of attempts.
    while count != 0:
        count = count - 1
        print("Enter password ")
        password = input()
        # calc hash of password and compare it with what we had
        ip_bytes = lib.getPassHash(password)
        if ip_bytes != pass_bytes:
            if count == 0:
                print("Attempts exceeded. Exiting")
                exit(0)
            print("Incorrect password.",count," attempts remain")
            continue
        else:
            #password was correct
            break

# print(opfilecount)  # debug only

# now we know files count 
# we know that starting from the index, we have 
# <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <semicolon seperated names of all files in same order>
# so we read that many bytes (each such bytes will be one decrypted file) and store then in an array and store that bytearray in an array
bytes_list = [] #this will have list of bytearrays
for i in range(opfilecount):
    filesize = bytearray()
    for j in range(0,8):    # 8 bytes to store bytes count 
        filesize.append(finalres[index])
        index = index + 1
    filesize = int.from_bytes(filesize, byteorder=endian)
    temp = bytearray()
    for j in range(0,filesize): # read that many bytes
        temp.append(finalres[index])
        index = index + 1
    bytes_list.append(temp) # read filesize bytes into seperate bytearray and add it to the list
if is_debug_mode:
    print("Number of files recovered is ",len(bytes_list))
# after storing all file bytes, we had encoded and appended semi-colon seperated list of original filenames
# we recover it now
actual_names = bytearray()  
while index < len(finalres):
    actual_names.append(finalres[index])
    index = index + 1
actual_names = actual_names.decode("utf-8") #decode that bytearray into string
actual_names = actual_names.split(";")
actual_names.pop() # last element will be empty as format was filename1;filename2; .. filenamek;
if is_debug_mode:
    print("Names for",len(actual_names),"files were found")

opdir_path = os.path.join(current_dir,op_directory_name)
# check if destination directory exists
if not os.path.exists(opdir_path):
    os.mkdir(opdir_path)
else:
    #if it does, we show a warning 
    print("The destination folder exists. All Files will be safe")
    print("In case, same named files are already there, you will be warned")
    print("continue? y/n")
    choice = input()
    if choice != "y":
        exit(0)
for i in range(0,opfilecount):
    rec_filename = os.path.join(opdir_path,actual_names[i])
    # check if file exists 
    if os.path.exists(rec_filename):
        print("The file ",actual_names[i], " already exists. Overwrite it? y/n")
        choice = input()
        if choice != "y":
            continue
    temp = actual_names[i].split(".")
    if len(temp) != 2:
        print("Some error occured in ",actual_names[i])
        continue
    # we get the format 
    # if we did some format specific encoding, we have to decode it. For eg use auto encoder to decode image and reconstruct original one
    format = temp[1]
    # first we decrypt the bytes considering how we encrypt them
    b = lib.decrypt(bytes_list[i],key)
    # now we decode bytes as per format and get bytearray
    b = lib.decodeBytes(b,format)
    # create a file with that bytearray
    f = open(rec_filename, "wb")
    f.write(b)
    f.close() # this is important ;p
if is_debug_mode:
    print("Encryption successful")