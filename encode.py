# find this project at https://github.com/gaurav-kc/Enc_dec

# first argument is the input directory name. It should have all the
# files you wish to encrypt.
# second argument is the output directory name. It will have the chunks
# third argument is the chunksize. 
# fourth argument is key (0-255) only 

import sys
import os
import json

#default values 
directory_name = "testit" #1st argument
op_directory_name = "encrypted" #2nd argument
chunksize = 10000 #3rd argument
key = 56 #4th argument 
commonname = "bpsnecjkx"
delimeter = "_"
opformat = "gty"
allowed_formats = ["jpg","png","jpeg"]
endian = 'little'

if len(sys.argv) >= 2:
    directory_name = sys.argv[1]
if len(sys.argv) >= 3:
    op_directory_name = sys.argv[2]
if len(sys.argv) >= 4:
    chunksize = int(sys.argv[3])
if len(sys.argv) >= 5:
    key = int(sys.argv[4])


def encrpyt_byte(by,key):
    #implement encryption logic here
    by = (by + key)%256
    return by

rel_pathname = "./" + directory_name + "/"
#check input directory name is correct or not 
isdirectory = os.path.isdir(rel_pathname)
if not isdirectory:
    print("Directory not found")
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
files_count = files_count.to_bytes(4, endian)   #conv to bytearray
finalres = finalres + files_count #first 4 bytes for file count 

#now for each file we append byte_count followed by encrypted bytes
for tfile in file_names:
    filepath = "./" + directory_name + "/" + tfile
    with open(filepath,"rb") as temp_file:
        f = temp_file.read()
        b = bytearray(f)
        size = int(len(b))
        #encrypt the bytes 
        for i in range(0,len(b)):
            b[i] = encrpyt_byte(b[i],key)
        #append the data
        size = size.to_bytes(4,endian)  #if file size goes beyound 4GB handle here
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

output_direc = "./" + op_directory_name
# check if directory exists
if not os.path.exists(output_direc):
    os.mkdir(output_direc)

# in that dir, put all files
for i in range(0,len(chunk_array)):
    #i will be the chunk number
    chunkname = commonname + delimeter + str(i) + "." + opformat
    chunkname = os.path.join(output_direc,chunkname)
    f = open(chunkname,"wb")
    f.write(chunk_array[i])
    f.close()       # this is important :D
