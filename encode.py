# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire blob(unchunked) is like this 
# a file is an array of bytes 
# <encodeMode> <header> <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
# as of now, header has filecount, key, password
# as of now, fileheader has filesize, filename
# After the successful execution, a folder will contain all chunks

from blank_template_encode import blankTemplate
from lib_encode import myImplementation
# from your python file, import your class here.

from flag_and_args import enc_flags_and_args
import sys

# process and set the default args as per flags
faa = enc_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation

lib = None
if args["encodeMode"] == 0: # default mode 
    lib = blankTemplate(flags, args)
# add further modes here
if args["encodeMode"] == 1: # sample mode
    lib = myImplementation(flags, args)
    
if lib is None:
    print("Invalid encode code")
    exit(0)

# get the metainformation like count of files, filenames, from the input folder
MetaInformation = lib.getMetaInformation()
# get bytearray formed encode mode to append
encodeMode = lib.getEncodeMode()
# construct the header for the blob. The header will be appended after encodeMode
header = lib.constructHeader(MetaInformation, encodeMode)
# create a blob of all files bytearrays appended
filesblob = lib.constructBlob(MetaInformation)
# combine header and fileblob
try:
    blob = header + filesblob
except TypeError:
    print("No such files found") # in case filesblob turns out to be empty.
    exit(0)
# chunk the blob into desired sized chunks. Break the big blob into pieces
chunk_array = lib.chunkBlob(blob)
# save all chunks into files
lib.saveChunks(chunk_array)
# perform any custom action. Pass params as required 
lib.performSomeAction()
print("Encryption successful")