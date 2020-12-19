# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire (unchunked) is like this 
# a file is an array of bytes 
# <header> <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <semicolon seperated names of all files in same order>
# all these bytes are appended serially 
# feel free to add any further improvements 

# TODO make a gui
# TODO add chunks directly to google drive 
# TODO think upon compression algorithmns for different formats. Use auto encoders or something to compress images 
# TODO have an option for more robust process (say by including some metadata or recovery mechanisms). 
# TODO handle directory inside directory

from lib_encode import myImplementation
# from your python file, import your class here.

from flag_and_args import enc_flags_and_args
import sys

faa = enc_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation
lib = None
if args["encodeMode"] == 0: # default mode 
    lib = myImplementation(flags, args)
# add further modes here
if lib is None:
    print("Invalid encode code")
    exit(0)
# get the count and list of filenames we will process
filecount, filenames = lib.getMetaInformation()
# construct the header for the blob
header = lib.constructHeader(filecount)
# create a blob of all files bytearrays appended
filesblob = lib.constructBlob(filenames)
# encode actual file names to use it while recovery
filenames_enc = lib.constructFilenameBlob(filenames)
# combine header, fileblob and filename encoding blob
try:
    blob = header + filesblob + filenames_enc
except TypeError:
    print("No such files found")
    exit(0)
# chunk the blob into desired sized chunks
chunk_array = lib.chunkBlob(blob)
# save all chunks into files
lib.saveChunks(chunk_array)
print("Encryption successful")