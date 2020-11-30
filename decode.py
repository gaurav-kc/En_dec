# find this project at https://github.com/gaurav-kc/Enc_dec

# first argument is the input directory name. It should have all the chunks 
# (it is okay if it has other files. The program reads only recognized format files)
# second argument is the output directory name. It will have the files
# third argument is the chunksize. If you mentioned it while encrypting
# fourth argument is key (0-255) only . If mentioned while encrypting

import sys
import os
import json

# default values
directory_name = "encrypted" #1st argument
op_directory_name = "decrypted" #2nd argument
chunksize = 10000 #3rd argument
key = 200 #4th argument 
commonname = "bpsnecjkx"
delimeter = "_"
opformat = "gty"
# allowed_formats = ["jpg","png","jpeg"] # of no use here
endian = 'little'

if len(sys.argv) >= 2:
    directory_name = sys.argv[1]
if len(sys.argv) >= 3:
    op_directory_name = sys.argv[2]
if len(sys.argv) >= 4:
    chunksize = int(sys.argv[3])
if len(sys.argv) >= 5:
    key = int(sys.argv[4])


def decrpyt_byte(by,key):
    #implement encryption logic here
    by = (by + key)%256
    return by

# construct the entire bytearray (combined of all chunks)
# check if given directory exists
dir_path = "./" + directory_name + "/"
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

print(filecount)    # debug purpose only 
if filecount == 0:
    print("No compatible files found")
    exit(0)

# finalres will have the entire bytes 
finalres = bytearray()
for i in range(0,filecount):
    # i here is chunk number
    filename = dir_path + commonname + delimeter + str(i) + "." + opformat
    if not os.path.exists(filename):
        print(filename, " not found")
        exit(0) # bilkul ricks nai lene ka
    file_obj = open(filename,"rb")
    f = file_obj.read()
    b = bytearray(f)
    finalres = finalres + b     # append bytearray of current file to finalres
    file_obj.close() 

print(len(finalres))  # debug only

#entire object I have now
index = 0   # this index will be our pointer to finalres. 
# in case any data is read through finalres, never ever forget to inc index 

opfilecount = bytearray()   # this will have number of files that will be created
for i in range(0,4):    # in our case, first 4 bytes will be interpreted as integer and stores how many files are there
    opfilecount.append(finalres[index])
    index = index + 1
opfilecount = int.from_bytes(opfilecount, byteorder=endian)
print(opfilecount)  # debug only

# now we know files count 
# we know our format is bytecount bytes bytecount bytes ... 
# so we read that many bytes (each such bytes will be one decrypted file)
bytes_list = []
for i in range(opfilecount):
    filesize = bytearray()
    for j in range(0,4):    # 4 bytes to store bytes count 
        filesize.append(finalres[index])
        index = index + 1
    filesize = int.from_bytes(filesize, byteorder=endian)
    temp = bytearray()
    for j in range(0,filesize):
        temp.append(decrpyt_byte(finalres[index],key))
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
print(actual_names) #debug only

# now we have bytearray and filename in 2 lists. We create a file with filename and write the bytearray to it
# In encrypted format, the order of bytes and filenames was same

# check if output directory exists
opdir_path = "./" + op_directory_name + "/"
if not os.path.exists(opdir_path):
    os.mkdir(opdir_path)

for i in range(0,opfilecount):
    rec_filename = opdir_path + actual_names[i]
    # check if file exists 
    if os.path.exists(rec_filename):
        print("The file ",actual_names[i], " already exists. Overwrite it? y/n")
        choice = input()
        if choice != "y":
            continue
    f = open(rec_filename, "wb")
    f.write(bytes_list[i])
    f.close()
print("Done")