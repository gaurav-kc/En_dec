# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to decrypt and recover all the files 
# The program reads the encrypted files and generates original files
# format of the entire (unchunked) is like this 
# <file_count,4B> <file_1_size,4B><file_1_bytes> <file_2_size,4B><file_2_bytes> ... <file_n_size,4B><file_n_bytes> <encoded string of semi-colon sepereated original filenames>
# After the successful execution, a folder will contain all recovered files
# feel free to add any further improvements 

# scope for improvements 
# TODO header contain chunksize and key 
# TODO modularize the code. Write in functions
# TODO allocate 8 Bytes instead of 4. 4 bytes puts limitation on file size (4GB) and on filecount (4*10^9)
# TODO flagged arguments (so that args dont have to be in order)
# TODO improve parent directory handling. Explicitly mentioning "./" is never good
# TODO add chunks directly to google drive 
# TODO think upon compression algorithmns for different formats. 
# TODO have an option for more robust process (say by including some metadata or recovery mechanisms)

import sys
import os
import json
import hashlib
from implemntation import template,def_behaviour,myImplementation
# default values
directory_name = "encrypted"
op_directory_name = "decrypted"
# chunksize = 10000
# key = 200 # we get cs and key from header now 
commonname = "bpsnecjkx"
delimeter = "_"
opformat = "gty"
# allowed_formats = ["jpg","png","jpeg"] # of no use here
endian = 'little'
current_dir = "./"
default_password = "pmqhfisbrkjcvklzxckliou"

# flags 
is_input_directory = False
is_output_directory = False
is_chunk_size = False
is_key = False

#handling the flags to set/overwrite default values
i = 1
while i < len(sys.argv):
    if sys.argv[i][0] == "-":
        flag = sys.argv[i].lstrip("-")
        # if flag is cs (chunksize)
        if flag == "cs":
            is_chunk_size = True    
            i = i + 1
            try:
                chunksize = int(sys.argv[i])
            except ValueError as e:
                print("Chunk size should be an integer")
                exit(0)
            except IndexError as ie:
                print("No chunk size given")
                exit(0)
        # if flag is k (key)
        elif flag == "k":
            is_key = True
            i = i + 1
            try:
                key = int(sys.argv[i])
            except ValueError as e:
                print("Key should be an integer")
                exit(0)
            except IndexError as ie:
                print("No key given")
                exit(0)
            if key<0 or key>256:
                print("Key has to be between 0 to 256")
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

db = def_behaviour()
setdb = template(db)
lib = myImplementation(setdb)

# construct the entire bytearray (combined of all chunks)
# check if given directory exists
dir_path = os.path.join(current_dir,directory_name)
if not os.path.exists(dir_path):
    print("Directory not found")
    exit(0)

# this step is to avoid all other files apart from what we recognize as chunk
# we only take count of such files and assume the files are from 0 to filecount-1
all_files = os.listdir(dir_path)
filecount = 0
for afile in all_files:
    filename = afile.split(".")
    format = filename[-1]
    if format == opformat:
        filecount = filecount + 1

# print(filecount)    # debug purpose only 
if filecount == 0:
    print("No compatible files found")
    exit(0)

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

# print(len(finalres))  # debug only

#entire object I have now
# this index will be our pointer to finalres. 
# in case any data is read through finalres, never ever forget to inc index 
opfilecount, chunksize, key, pass_bytes, index = lib.decodeHeader(finalres,endian)
def_digest = lib.getPassHash(default_password)

if def_digest != pass_bytes:
    #it was a protected file
    count = 3
    while count != 0:
        count = count - 1
        print("Enter password ")
        password = input()
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
# we know our format is bytecount bytes bytecount bytes ... 
# so we read that many bytes (each such bytes will be one decrypted file)
bytes_list = []
for i in range(opfilecount):
    filesize = bytearray()
    for j in range(0,8):    # 4 bytes to store bytes count 
        filesize.append(finalres[index])
        index = index + 1
    filesize = int.from_bytes(filesize, byteorder=endian)
    temp = bytearray()
    for j in range(0,filesize):
        temp.append(finalres[index])
        index = index + 1
    bytes_list.append(temp) # read filesize bytes into seperate bytearray and add it to the list

# after storing all bytes, we had encoded and appended semi-colon seperated list of original filenames
# we recover it now
actual_names = bytearray()  
while index < len(finalres):
    actual_names.append(finalres[index])
    index = index + 1
actual_names = actual_names.decode("utf-8") #decode that bytearray into string
actual_names = actual_names.split(";")
actual_names.pop() # last element will be empty as format was filename1;filename2; .. filenamek;


opdir_path = os.path.join(current_dir,op_directory_name)
if not os.path.exists(opdir_path):
    os.mkdir(opdir_path)

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
    format = temp[1]
    b = lib.decodeBytes(bytes_list[i],format)
    b = lib.decrypt(b,key)
    f = open(rec_filename, "wb")
    f.write(b)
    f.close()
print("Decryption done")