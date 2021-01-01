# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to encrypt and chunk you files 
# The program reads the files and then encrypts the bytes, and store it in chunks
# format of the entire blob(unchunked) is like this 
# <pipelineCode> <modes encoded> <primary header> <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
# as of now, there is only one pipeline code 
# as of now, the primary header has file count, decrpytion key and pasword
# as of now, fileheader has filesize, filename
# After the successful execution, a folder will contain all chunks

# from the python file, import the pipeline handling class here.
from implementation_encode import default_encode
# deal with the flags and default arguments
from flag_and_args import enc_flags_and_args

import sys

# process and set the default args as per flags
faa = enc_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation

if args["pipelineCode"] == 0: # default mode 
    default_encode().perform_encode(flags, args)
    
# add further pipeline modes here
print("Encryption successful")