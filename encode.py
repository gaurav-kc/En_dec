# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire blob(unchunked) is like this 
# a file is an array of bytes 
# <encodeMode> <header> <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
# as of now, header has filecount, key, password
# as of now, fileheader has filesize, filename
# After the successful execution, a folder will contain all chunks

from universal import commonFunctions
# from your python file, import your class here.
from implementation_encode import enc_def_behaviour
from flag_and_args import enc_flags_and_args
import sys

# process and set the default args as per flags
faa = enc_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation
cmf = commonFunctions(flags, args)
lib = None

if args["pipelineCode"] == 0: # default mode 
    lib = enc_def_behaviour(flags, args)
    # get the metainformation like count of files, filenames, from the input folder
    MetaInformation = lib.getMetaInformation()
    # get the pipeline code in the byte format 
    pipelineC = lib.getPipelineBytes()
    # get the modes encoded in bytes 
    modeCode = lib.getModeBytes()
    # construct the header for the blob. The header will be appended after encodeMode
    header = lib.constructHeader(MetaInformation)
    header = pipelineC + modeCode + header
    # create a blob of all files bytearrays appended
    filesblob = lib.constructFilesBlob(MetaInformation)
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
    # add further modes here

if lib is None:
    print("Invalid encode code")
    exit(0)
print("Encryption successful")