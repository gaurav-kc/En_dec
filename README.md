En_Dec

The project has 2 main purposes:
1. Convert all the files in the directory into fixed size chunks. (Encode)
2. Recover all the files from the chunks present in that directory. (Decode)

Table of Contents:
1. Introduction
2. Encoding
3. Decoding
4. Flags
5. Installtion and usage
6. Add your implementation

1. Introduction
For any reason like (storing files such that they cannot be opened by anyone else, or chunk bunch of files into fixed sized chunks say 1GB to easily upload and store it on cloud, or any other reasons) you might require to convert some files into fixed sized chunks. The first component of the project (the process of encoding) is dedicated to do this. The encoding and decoding processes work in a pipeline fashion to make it customizable. In short 
//image for files -> encoding -> chunks
//image for chunks -> decoding -> files
The process of encoding is carried out as follows 
//image for process and set flags and arguments -> get meta information -> create a header -> create blob of all files -> encode original file names -> create chunks
and the process of decoding is carried out as follows 
//image for process and set flags and arguments -> identify chunks -> combine them -> get header -> recover all files with their original file names
Additional details in respective section.

2. Encoding 
This component converts files into chunks. But there is added fun to this. 
At first, idea was to simply read the files, combine the binary data and break it into chunks. But what if, we add other stuff in this process? As of now, I have added 2 more stages, encode file and encrypt data. The files can be encoded as per the format into it's compressed representation. Further, those bytes can be encrypted before they are converted into chunks. Best part is, you can add your own encoding and encrypting mechanisms easily without going into other details of the project. 

3. Decoding
This component identifies and converts chunks into original files.
The stages followed while encoding, are performed in a reverse manner while decoding. First, all the data from chunks is combined to form a big blob. Then the header is decoded to get the meta information like number of files, decrpytion key, is it password protected and if yes, hash of the password, and so on. Then, the data is read for every file, decrypted and then decoded to recover the original file from it. 

4. Flags
Flags are useful to specify parameters. 
Flags start with "-". If "-" is not there, it assumes it is the name of directory. 
Be it encoding or decoding, 
First such argument without "-" is considered to be name of input directory (from where files has to be read)
Second such argument without "-" is considered to be name of output directory (name of directory where output is to be stored)

Flag supported in Encode.py
By default, it expects input files in a directory named "testit". Thus, 
python3 encode.py 
will encode all files in "testit" directory. 
You can change it by specifying the name of input directory as argument 
python3 encode.py my_dir
By default, encode.py will put all chunks in a directory named "encrypted". Thus, 
python3 encode.py my_dir 
will encode all files from my_dir and store chunks in "encrypted" directory.
You can change it by specifying the name of output directory as argument 
python3 encode.py my_dir chunks_dir
-cs <chunk_size>  (custom chunk size)
By default, the chunk size is 100000 Bytes (100kB). You can change it using flag -cs
python3 encode.py my_dir chunks_dir -cs 1000000
-k  <key> (custom key)
By default, the project comes with a simple byte level encryption and the key for it is 56. You can change it using flag -k
python3 encode.py my_dir chunks_dir -k 75  
(Note that by default 4 Bytes are allocated in header to store the key. Store key as per your encryption algorithm. The default algo needs key between 0-255)
-f  <comma seperated list. Possible elements : images,videos,docs,prog> (consider only these kind of files to encrypt)
By default, it would try to encode all the files in the directory. To encode specific types of files, you can use flag -f
python3 encode.py my_dir chunks_dir -f images 
encodes only image type of files from input directory
python3 encode.py my_dir chunks_dir -f images,videos
encodes image and video type of files from input directory
(Right now, 4 categories are supported. images, videos, docs, prog. Check the formats for each category in flag_and_args.py)
-p  (enable password protection)
By default, password protection is disabled. To enable it, use flag -p
python3 encode.py my_dir chunks_dir -p
will ask for password before encoding. And will be required while decoding.
-d  (print debugging statements)
While solving errors, debugging statements are useful. But not always. By default it's off. Turn debugging statements on by using flag -d
python3 encode.py my_dir chunks_dir -d
will print debugging statements while executing.
-sw (supress warning)
By default basic warnings are shown. To supress them, use flag -sw

Note that there is no ordering for anything. Just make sure the argument for a flag is right next to it. 
python3 encode.py -cs 1000000 my_dir -k 89 chunks_dir -d -p
will work.

Flag supported in decode.py
-d  (print debugging statements)
(All necessary details are included in the header itself, so that we don't need to remember it)

5. Installtion and usage
Dependencies : 
python3 
python libraries :
hashlib
To run the project:
python3 encode.py <ip directory> <op directory> <flags>
python3 decode.py <ip directory> <op directory>

6. Add your implementation
Fork this repo
