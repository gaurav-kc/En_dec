# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to decrypt and recover all the files 
# The program reads the encrypted files and generates original files
# format of the entire blob(unchunked) is like this 
# a file is an array of bytes 
# <encodeMode> <header> <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
# as of now, header has filecount, key, password
# as of now, fileheader has filesize, filename
# After the successful execution, a folder will contain all recovered files

from blank_template_decode import blankTemplate
# from your python file, import your class here.

from implementation_decode import dec_def_behaviour

from flag_and_args import dec_flags_and_args
import sys

# process and set the default args as per flags
faa = dec_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation
def_imp = dec_def_behaviour(flags, args)
# dec_def_behaviour is called as the starting process remains same
# first, identify all chunks, combine and form a big blob and then get encode mode.
# getting encode mode first is important as further tasks like decoding header, file decoding and decrypting mechanisms depend upon it.

# first identify how many files in the folder we identify as chunks. Get the count 
chunkcount = def_imp.identifyChunks()
# constrct the entire blob, combined all chunks
finalBlob = def_imp.constructBlob(chunkcount)
# extract encodeMode and get index (pointer to the byte where header will start) for blob
encodeMode, index = def_imp.getEncodeCode(finalBlob)

lib = None
if encodeMode == 0: # found that it was encoded with default mode 
    lib = blankTemplate(flags, args)

# add another encode mode here 

if lib is None:
    print("Invalid encode mode detected")
    exit(0)
    
# now the lib object is the object of class corresponding to the encode mode
# decode the header and extract values from header
header, index = lib.decodeHeader(finalBlob, index)
# check if password was there
lib.checkPassword(header)
# get the list of fileInfo objects where each fileinfo object has 2 fields. 1. Fileheader and 2. file blob
filesInfoList, index = lib.getFileBlobList(finalBlob, index, header)
# recover all the files. Now we have list of fileinfo objects. Header is required for key while decrpytion.
# get a file info. Read header, decrypt blob, decode blob, create and save file.
lib.recoverFiles(filesInfoList, header)
# perform some custom action. Pass params as required 
lib.performSomeAction(header)
print("Decryption successful")