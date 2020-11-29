# find recent code at https://github.com/gaurav-kc/Enc_dec

# first argument is the input directory name. It should have all the
# images you wish to encrypt. For now chunk size will be 200MB

# second argument is the output directory name. It will have the chunks 

import sys
import os

# if len(sys.argv) != 3:
#     print("Arguments not correct. Expecting 1 arg")
#     exit(-1)

directory_name = "testit" #1st argument
op_directory_name = "encrypted" #2nd argument
key = 56 #can be taken as argument
chunksize = 10000 #can be taken as argument 
def encrpyt_byte(by,key):
    #implement encryption logic here
    by = (by + key)%256
    return by

rel_pathname = "./" + directory_name + "/"
#check directory name is correct or not 
isdirectory = os.path.isdir(rel_pathname)
if not isdirectory:
    print("Directory not found")
    exit(-1)

#check all files and formats
allowed_formats = ["jpg","png","jpeg"]

tfile_names = os.listdir(rel_pathname)
file_names = []
#analyze these names 
for tfile in tfile_names:
    temp = tfile.split(".")
    if len(temp) != 2:
        print("Incorrect format ",tfile)
        continue
    filename = temp[0]
    format = temp[1]
    if format not in allowed_formats:
        print("Excluding file ",tfile)
        continue
    file_names.append(tfile)
print(file_names)
    
files_count = len(file_names)
if files_count == 0:
    print("Nothing to encrpyt")
    exit(0)

finalres = bytearray()
little = 'little'
files_count = files_count.to_bytes(4, little)   #conv to bytearray
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
        size = size.to_bytes(4,little)
        finalres = finalres + size + b

#now we have all bytes in finalres variable.
#we need to chunk it

chunk_array = []
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
#give crazy file names 
output_direc = "./" + op_directory_name
os.mkdir(output_direc)
delimeter = "_"
opformat = "gty"
for i in range(0,len(chunk_array)):
    #i will be the chunk number
    chunkname = "bpsnecjkx" + delimeter + str(i) + "." + opformat
    chunkname = os.path.join(output_direc,chunkname)
    f = open(chunkname,"wb")
    f.write(chunk_array[i])
        
