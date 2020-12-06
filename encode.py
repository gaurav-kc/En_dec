# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire (unchunked) is like this 
# a file is an array of bytes 
# <header> <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <semicolon seperated names of all files in same order>
# all these bytes are appended serially 
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
directory_name = "testit"   # if not given, expect files in this folder
op_directory_name = "encrypted"     #if not given, put encrypted files in this folder
chunksize = 10000   # if not given, consider these many bytes as chunk size
key = 56    # if not given, consider this value as key for your encryption algorithm
commonname = "bpsnecjkx"    # common name for all chunked encrypted files
delimeter = "_" # delimeter between common name and file number
opformat = "gty"    # format for chunks. 
allowed_formats = ["jpg","png","jpeg"]  # encrpyt only these format files 
endian = 'little'   # in encode and decode, both should have same endian to write bytes
current_dir = "./"
default_password = "pmqhfisbrkjcvklzxckliou" # this is to detect whether password was provided or not

# flags 
# currently supported flags. (Input and output directory doesn't need any flag. order doenst matter. Flags and directories can be any order. All are optional)
# anywhere, first directory name is assumed as input directory name and next as output directory name 
# by default, input directory is assumed in directory specified in variable directory_name
# by default, output directory is asssumed in directory specified in variable op_directory_name
# -cs <chunk_size>  (custom chunk size)
# -k <key> (custom key)
# -p  (enable password protection)
# -d  (print debugging statements)
is_input_directory = False
is_output_directory = False
is_chunk_size = False
is_key = False
is_pass_protected = False
is_debug_mode = False
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
        elif flag == "p":
            is_pass_protected = True
        elif flag == "d":
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
if is_debug_mode:
    print("Encrypting ... ")
rel_pathname = os.path.join(current_dir,directory_name)
#check input directory name is correct or not 
isdirectory = os.path.isdir(rel_pathname)
if not isdirectory:
    print(directory_name," not found")
    exit(-1)
if is_debug_mode:
    print("Looking for files in ",rel_pathname)
# get list of file_names, respective format, and filenames_enc is a compact representation
# to store original filenames (to restore original filenames when we decrypt)
# the filenames_enc is appended at the end. By default uses semicolon seperated filenames 
file_names, formats, filenames_enc = lib.enc_filenames(rel_pathname,allowed_formats)

#to avoid null cases. Check if there is atleast one file to encrypt
files_count = len(file_names)
if files_count == 0:
    print("Nothing to encrpyt")
    exit(0)
if is_debug_mode:
    print("File count is ",files_count)
#getHeader will construct the header and return bytearray format of it
#header has number_of_files, chunksize, key, password_hash
finalres = lib.getHeader(files_count,chunksize,key,endian,default_password,is_pass_protected)
if is_debug_mode:
    print("Length of header is ",len(finalres))
#now for each file we append byte_count followed by encrypted bytes
for i in range(0,len(file_names)):
    filepath = os.path.join(current_dir,directory_name,file_names[i])
    with open(filepath,"rb") as temp_file:
        f = temp_file.read()
        b = bytearray(f)
        size = int(len(b))
        #encodeBytes right now does nothing
        #this function can be used to encode the file as per format
        #for example, use an auto encoder to compress an image. And use that compressed representation to store that image
        #similarly, pdfs and other formatted files can be modified to either compress or have some meta info for recovery etc
        b = lib.encodeBytes(b,formats[i])
        #the bytes should be encrypted. Right now it uses byte level encryption and simply adds key and takes % 256. (as a byte is 0-255)
        #you can implement various encrpytion algorithms. Even on groups of bytes. Key is given 4Bytes in header but can be dec/inc as per req
        b = lib.encrypt(b,key)
        #append the size 
        size = size.to_bytes(8,endian)  
        finalres = finalres + size + b  #append byte count and that many bytes

#now in finalres, we have this 
# <header> <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes>
# now at the end, we append the list of original file names 
finalres = finalres + filenames_enc
if is_debug_mode:
    print("Length of entire blob is ",len(finalres))
# now we have all bytes in finalres variable.
# we need to chunk it
# a warning is given as wrong chunk size can create millions of chunks
chunkcount = int(len(finalres)/chunksize) + 1 
print(chunkcount, " chunks will form. Are you sure you want to continue? y/n")
choice = input()
if choice != "y":
    exit(0)

chunk_array = []    # this will be array of bytearrays where each bytearray is a chunk of size chunksize (except last)
i = 0
while i < len(finalres):
    chunk = bytearray()
    j = 0
    while (j < chunksize) and (i<len(finalres)):
        chunk.append(finalres[i])
        i = i+1
        j = j+1
    chunk_array.append(chunk)
if is_debug_mode:
    print("Number of chunks created = ",len(chunk_array))
#now we have an array of bytearrays 

output_direc = os.path.join(current_dir,op_directory_name)
# check if the output directory exists
if not os.path.exists(output_direc):
    os.mkdir(output_direc)
else:
    #if it does, we show a warning 
    print("The destination folder exists. All Files will be safe")
    print("In case, same named files are already there, operation will be aborted")
    print("continue? y/n")
    choice = input()
    if choice != "y":
        exit(0)
# a function to roll back changes used in the loop later
# say in the destination directory, we find an existing chunk
# then we have to roll back changes 
def abrupt_abortion(commonname,delimeter,i,opformat,output_direc):
    for i in range(0,i):
        chunkname = commonname + delimeter + str(i) + "." + opformat
        chunkname = os.path.join(output_direc,chunkname)
        try:
            os.remove(chunkname)
        except FileNotFoundError:
            print("Did not find ",chunkname)

# in the target directory, we create all the chunk files 
for i in range(0,len(chunk_array)):
    #i will be the chunk number
    chunkname = commonname + delimeter + str(i) + "." + opformat
    chunkname = os.path.join(output_direc,chunkname)
    if os.path.exists(chunkname) == True:
        # The file already exists. Even if we overwrite, the but we are not able to overwrite all chunks,
        # while decrypting it will be error
        # best is to roll back. We could have halted but then incomplete chunks will exist 
        print("Existing file ",chunkname," found. Rolling back changes")
        abrupt_abortion(commonname,delimeter,i,opformat,output_direc)
        exit(0)
    f = open(chunkname,"wb")
    f.write(chunk_array[i])
    f.close()       # this is important :D
if is_debug_mode:
    print("Encryption successful")