# this file is to implement functios which are common. irrespective of mode or any customizations. 
from pathlib import Path
class commonFunctions():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
    
    def getEncryptedFilenames(self, chunkcount):
        args = self.args
        chunk_names = []
        for i in range(0, chunkcount):
            chunkname = args["_commonname"] + args["_delimeter"] + str(i) + "." + args["_opformat"]
            chunk_names.append(chunkname)
        return chunk_names 
    
    def getFirstFileName(self):
        chunk_names = self.getEncryptedFilenames(1)
        return chunk_names[0]

    def readPipelineCode(self):
        # start point for our program
        dir_path = Path(self.args["current_dir"]).joinpath(self.args["ip_directory_name"])
        filename = self.getFirstFileName()
        filepath = dir_path.joinpath(filename)
        if not filepath.exists():
            print(filename, " not found")
            exit(0) # bilkul ricks nai lene ka
        file_obj = open(filepath,"rb")
        f = file_obj.read()
        fblob = bytearray(f)
        file_obj.close() 
        index = 0

        pipeLineCode = bytearray() 
        for _ in range(0,self.args["_encode_mode_size"]):
            pipeLineCode.append(fblob[index])
            index = index + 1
        pipeLineCode = int.from_bytes(pipeLineCode, byteorder=self.args["_endian"])

        return fblob, pipeLineCode, index