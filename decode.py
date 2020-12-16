# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to decrypt and recover all the files 
# The program reads the encrypted files and generates original files
# format of the entire (unchunked) is like this 
# a file is an array of bytes 
# <header> <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <all actual filenames encoded>
# After the successful execution, a folder will contain all recovered files
# feel free to add any further improvements 

# TODO add chunks directly to google drive 
# TODO think upon compression algorithmns for different formats. Use auto encoders or something to compress images 
# TODO have an option for more robust process (say by including some metadata or recovery mechanisms). 
# TODO handle directory inside directory

# from your python file, import your class here.
from lib_decode import myImplementation

from flag_and_args import dec_flags_and_args
import sys

faa = dec_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation
lib = myImplementation(flags, args)

# first identify how many files in the folder we identify as chunks. Get the count 
chunkcount = lib.identifyChunks()
# constrct the entire blob, combined all chunks
finalBlob = lib.constructBlob(chunkcount)
# extract header and get index (pointer to the next byte after header) for blob
header, index = lib.decodeHeader(finalBlob)
# check if password was there
lib.checkPassword(header["pass_bytes"])
# get the list of bytearrays where each bytearray is the bytearray of the encrypted encoded file
bytes_list, index = lib.getFileBlobList(finalBlob, index, header["opfilecount"])
# recover the actual names of the files, which we appended at the end of the blob
actual_names = lib.getActualNames(finalBlob, index)
# recover all the files as we now have bytearrays and corresponding filenames. Decrypt, decode and save
lib.recoverFiles(bytes_list, actual_names, header["key"])
print("Decryption successful")