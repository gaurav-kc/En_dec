from lib_encode import myImplementation
from flag_and_args import enc_flags_and_args
import sys

faa = enc_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
lib = myImplementation(flags, args)

filecount, filenames = lib.getMetaInformation()
header = lib.constructHeader(filecount)
filesblob = lib.constructBlob(filenames)
filenames_enc = lib.constructFilenameBlob(filenames)
blob = header + filesblob + filenames_enc
chunk_array = lib.chunkBlob(blob)
lib.saveChunks(chunk_array)