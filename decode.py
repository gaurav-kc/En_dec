from lib_decode import myImplementation
from flag_and_args import dec_flags_and_args
import sys

faa = dec_flags_and_args()
flags, args = faa.getFlagsAndArgs(sys.argv)
lib = myImplementation(flags, args)

chunkcount = lib.identifyChunks()
finalBlob = lib.constructBlob(chunkcount)
header, index = lib.decodeHeader(finalBlob)
lib.checkPassword(header["pass_bytes"])
bytes_list, index = lib.getFileBlobList(finalBlob, index, header["opfilecount"])
actual_names = lib.getActualNames(finalBlob, index)
lib.recoverFiles(bytes_list, actual_names, header["key"])