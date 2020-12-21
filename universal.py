import os
class commonFunctions():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
    
    def getPipelineBytes(self):
        pipelineCode = self.args["pipelineCode"]

        pipelineCode = pipelineCode.to_bytes(self.args["_pipeline_code_size"],self.args["_endian"])
        return pipelineCode
    
    def identifyChunks(self):
        # this function is to get the count of chunks in input folder.
        args = self.args
        flags = self.flags
        dir_path = os.path.join(args["current_dir"],args["ip_directory_name"])
        if not os.path.exists(dir_path):
            print("Directory not found")
            exit(0)
        if flags["is_debug_mode"]:
            print("Looking for files in ",dir_path)
        # this step is to count the chunks and avoid all other files apart from what we recognize as chunk
        all_files = os.listdir(dir_path)
        chunkcount = 0
        for afile in all_files:
            if self.isChunk(afile): # function call to identify a filename as chunk
                chunkcount = chunkcount + 1
        if chunkcount == 0:
            print("No compatible files found")
            exit(0)
        if flags["is_debug_mode"]:
            print("Number of chunks found is ",chunkcount)
        return chunkcount
    
    def isChunk(self, filename):
        # checks if a filename is identified as chunk or not 
        # by defaults assumes, if the format is as per _opformat in args , then it is chunk
        filename = filename.split(".")
        if len(filename) != 2:
            return False
        format = filename[-1]
        if format == self.args["_opformat"]:
            return True
        return False
    
    def constructBlob(self, chunkcount):
        # a function that reads all the chunks and combines all the blobs into a big blob
        args = self.args
        flags = self.flags
        # to get the chunk names
        encryptedFilenames = self.getEncryptedFilenames(chunkcount)
        dir_path = os.path.join(args["current_dir"],args["ip_directory_name"])
        finalBlob = bytearray()
        for i in range(0, chunkcount):
            filename = os.path.join(dir_path, encryptedFilenames[i])
            if not os.path.exists(filename):
                print(filename, " not found")
                exit(0) # bilkul ricks nai lene ka
            file_obj = open(filename,"rb")
            f = file_obj.read()
            b = bytearray(f)
            finalBlob = finalBlob + b     # append bytearray of current file to finalBlob
            file_obj.close() 
        if flags["is_debug_mode"]:
            print("Size of entire blob is ",len(finalBlob))
        return finalBlob
    
    def getEncryptedFilenames(self, chunkcount):
        # start point for our program
        args = self.args
        chunk_names = []
        for i in range(0, chunkcount):
            chunkname = args["_commonname"] + args["_delimeter"] + str(i) + "." + args["_opformat"]
            chunk_names.append(chunkname)
        return chunk_names 
    
    def readPipelineCode(self, finalBlob):
        index = 0

        pipeLineCode = bytearray() 
        for _ in range(0,self.args["_encode_mode_size"]):
            pipeLineCode.append(finalBlob[index])
            index = index + 1
        pipeLineCode = int.from_bytes(pipeLineCode, byteorder=self.args["_endian"])

        return pipeLineCode, index
