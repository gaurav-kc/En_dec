# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire (unchunked) is like this 
# <file_count,4B> <file_1_size,4B><file_1_bytes> <file_2_size,4B><file_2_bytes> ... <file_n_size,4B><file_n_bytes> <encoded string of semi-colon sepereated original filenames>
# all these bytes are appended serially 
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

# default values 
directory_name = "testit"
op_directory_name = "encrypted" 
chunksize = 10000
key = 56 
commonname = "bpsnecjkx"
delimeter = "_"
opformat = "gty"
allowed_formats = ["jpg","png","jpeg"]
endian = 'little'
current_dir = "./"
default_password = "pmqhfisbrkjcvklzxckliou"

# flags 
is_input_directory = False
is_output_directory = False
is_chunk_size = False
is_key = False
is_pass_protected = False
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
        elif flag == "p":
            is_pass_protected = True
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


def encrpyt_bytes(b,key):
    #implement encryption logic here
    for i in range(0,len(b)):
        b[i] = (b[i] + key)%256
    return b

def getDecKey(key):
    return (256-key)

rel_pathname = os.path.join(current_dir,directory_name)
#check input directory name is correct or not 
isdirectory = os.path.isdir(rel_pathname)
if not isdirectory:
    print(directory_name," not found")
    exit(-1)

#check all files and formats
tfile_names = os.listdir(rel_pathname)
file_names = [] #this will have all filenames which will be actually encrypted
filenames_enc = str()
#analyze these names of files in directory
for tfile in tfile_names:
    temp = tfile.split(".")
    #only one dot is allowed in filename
    if len(temp) != 2:
        print("Incorrect format ",tfile, " skipping it.")
        continue
    #check for delimeter
    temp1 = tfile.split(";")
    if len(temp1) != 1:
        print("; found in ",tfile," which is not allowed")
        continue
    filename = temp[0]
    format = temp[1]
    #check if file has format in our list
    if format not in allowed_formats:
        print("Excluding file ",tfile)
        continue
    file_names.append(tfile)
    filenames_enc = filenames_enc + tfile + ";"

# this was added to restore the original filenames 
# it is of type filename1;filename2; .. filenamek;
filenames_enc = bytearray(filenames_enc,'utf-8')

files_count = len(file_names)
if files_count == 0:
    print("Nothing to encrpyt")
    exit(0)

finalres = bytearray()  # this will have the entire bytearray
files_count = files_count.to_bytes(8, endian)   #conv to bytearray
cs_bytes = chunksize.to_bytes(4,endian)
dec_key = getDecKey(key)
key_bytes = dec_key.to_bytes(4,endian)

password = default_password
if is_pass_protected == True:
    print("Enter password")
    password = input()
    if len(password) == 0:
        print("No password given. Creating unprotected files..")
    else:
        password = password.strip(" ")
        password = password.strip("\n")

password = hashlib.sha1(password.encode())
password = password.digest()
print(len(password))
finalres = finalres + files_count + cs_bytes + key_bytes + password
print("Header is ",len(finalres))
#now for each file we append byte_count followed by encrypted bytes
for tfile in file_names:
    filepath = os.path.join(current_dir,directory_name,tfile)
    with open(filepath,"rb") as temp_file:
        f = temp_file.read()
        b = bytearray(f)
        size = int(len(b))
        #encrypt the bytes 
        b = encrpyt_bytes(b,key)
        #append the data
        size = size.to_bytes(8,endian)  #if file size goes beyound 4GB handle here
        finalres = finalres + size + b  #append byte count and that many bytes

# we convert the list and append at the end to restore the original names 
finalres = finalres + filenames_enc
print("finalres is ",len(finalres)) #this is for debugging

# now we have all bytes in finalres variable.
# we need to chunk it
# a warning is given as wrong chunk size can create millions of chunks
chunkcount = int(len(finalres)/chunksize) + 1 
print(chunkcount, " chunks will form. Are you sure you want to continue? y/n")
choice = input()
if choice != "y":
    exit(0)

chunk_array = []    # this will be array of bytearrays where each bytearray is a chunk
i = 0
while i < len(finalres):
    chunk = bytearray()
    j = 0
    while (j < chunksize) and (i<len(finalres)):
        chunk.append(finalres[i])
        i = i+1
        j = j+1
    chunk_array.append(chunk)

#now we have byte chunks

output_direc = os.path.join(current_dir,op_directory_name)
# check if directory exists
if not os.path.exists(output_direc):
    os.mkdir(output_direc)
else:
    print("The destination folder exists. All Files will be safe")
    print("In case, same named files are already there, operation will be aborted")
    print("continue? y/n")
    choice = input()
    if choice != "y":
        exit(0)

def abrupt_abortion(commonname,delimeter,i,opformat,output_direc):
    for i in range(0,i):
        chunkname = commonname + delimeter + str(i) + "." + opformat
        chunkname = os.path.join(output_direc,chunkname)
        try:
            os.remove(chunkname)
        except FileNotFoundError:
            print("Did not find ",chunkname)

# in that dir, put all files
for i in range(0,len(chunk_array)):
    #i will be the chunk number
    chunkname = commonname + delimeter + str(i) + "." + opformat
    chunkname = os.path.join(output_direc,chunkname)
    if os.path.exists(chunkname) == True:
        print("Existing file ",chunkname," found. Rolling back changes")
        abrupt_abortion(commonname,delimeter,i,opformat,output_direc)
        exit(0)
    f = open(chunkname,"wb")
    f.write(chunk_array[i])
    f.close()       # this is important :D
