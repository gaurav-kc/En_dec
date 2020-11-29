# find this project at https://github.com/gaurav-kc/Enc_dec

# First argument is mandatory. Rest 3 are are optional. But order is important 
# first argument is the input directory name. It should have all the chunks
# second argument is the output directory name. It will have the files
# third argument is the chunksize. If you mentioned it while encrypting
# fourth argument is key (0-255) only . If mentioned while encrypting

import sys
import os
import json

directory_name = "encrypted" #1st argument
op_directory_name = "decrypted" #2nd argument
chunksize = 10000 #3rd argument
key = 200 #4th argument 
commonname = "bpsnecjkx"
delimeter = "_"
opformat = "gty"
# allowed_formats = ["jpg","png","jpeg"]
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

# let us construct the entire object
dir_path = "./" + directory_name + "/"
if not os.path.exists(dir_path):
    print("Directory not found")
    exit(0)

all_files = os.listdir(dir_path)
filecount = 0
for afile in all_files:
    filename = afile.split(".")
    format = filename[-1]
    if format == opformat:
        filecount = filecount + 1

print(filecount)
if filecount == 0:
    print("No compatible files found")
    exit(0)

finalres = bytearray()
for i in range(0,filecount):
    filename = dir_path + commonname + delimeter + str(i) + "." + opformat
    if not os.path.exists(filename):
        print(filename, " not found")
        exit(0)
    f = (open(filename,"rb")).read()
    b = bytearray(f)
    finalres = finalres + b
print(len(finalres))

#entire object I have now
index = 0

opfilecount = bytearray()
for i in range(0,4):
    opfilecount.append(finalres[index])
    index = index + 1
opfilecount = int.from_bytes(opfilecount, byteorder=endian)
print(opfilecount)

bytes_list = []
for i in range(opfilecount):
    filesize = bytearray()
    for j in range(0,4):
        filesize.append(finalres[index])
        index = index + 1
    filesize = int.from_bytes(filesize, byteorder=endian)
    temp = bytearray()
    for j in range(0,filesize):
        temp.append(decrpyt_byte(finalres[index],key))
        index = index + 1
    bytes_list.append(temp)

actual_names = bytearray()
while index < len(finalres):
    actual_names.append(finalres[index])
    index = index + 1
actual_names = actual_names.decode("utf-8") 
actual_names = actual_names.split(";")
actual_names.pop()
print(actual_names)

opdir_path = "./" + op_directory_name + "/"
if not os.path.exists(opdir_path):
    os.mkdir(opdir_path)

for i in range(0,opfilecount):
    rec_filename = opdir_path + actual_names[i]
    f = open(rec_filename, "wb")
    f.write(bytes_list[i])
print("Done")