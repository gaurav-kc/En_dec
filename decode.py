# find this project at https://github.com/gaurav-kc/Enc_dec

# This is a program to decrypt and recover all the files 
# The program reads the encrypted files and generates original files
# a file is an array of bytes 
# format of the entire blob(unchunked) is like this 
# <pipelineCode> <modes encoded> <primary header> <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
# as of now, there is only one pipeline code 
# as of now, the primary header has file count, decrpytion key and pasword
# as of now, fileheader has filesize, filename
# After the successful execution, a folder will contain all recovered files

# from your pipeline handler file, import the class here.
from implementation_decode import default_decode

# flags and argument handler. 
from flag_and_args import dec_flags_and_args
import sys

# process and set the default args as per flags
faa = dec_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
# those flags and default values will be set for implementation
# as of now just try default one 
default_decode().perform_decode(flags, args)
    
# add another encode mode here 
print("Decryption successful")