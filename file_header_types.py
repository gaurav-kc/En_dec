# this file is to implemenet various types of file headers as per the value of mode 
# create an object of class file_header and call constructFileHeader or getFileHeader with the mode value 
# Also, while creating the object for class file_header, there params need to be given
# 1. flags -> for code to get access to any flags 
# 2. args -> for code to get access to args 
# 3. self -> (reference to self) which is required to call any function which is present in the caller class
class file_header():
    def __init__(self, flags, args, caller):
        self.flags = flags
        self.args = args
        self.caller = caller

    def constructFileHeader(self, mode, size, filename): 
        fileHeader = None
        if mode == 0:
            consFileHeader = default_mode(self.flags, self.args)
            try:
                fileHeader = consFileHeader.constructFileHeader(size, filename, self.caller)
            except NotImplementedError:
                print("Function to construct file header is not defined")
        if fileHeader is None:
            print("There was some problem while constructing header in mode ",mode)
        return fileHeader
    
    def getFileHeader(self, mode, finalBlob, index):
        fileHeader = None
        retindex = -1
        if mode == 0:
            getfileh = default_mode(self.flags, self.args)
            try:
                fileHeader, retindex = getfileh.getFileHeader(finalBlob, index, self.caller)
            except NotImplementedError:
                print("Function to get file header contents is not defined")
        if fileHeader is None or retindex == -1:
            print("There was some problem while getting file header contents")
        return fileHeader, retindex
    
class default_mode():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args

    def constructFileHeader(self, size, filename, caller):
            # with the argument provided, this function creates file header for a particular file
            fileHeader = bytearray()
            size = size.to_bytes(self.args["_cs_size"],self.args["_endian"])
            fileHeader = fileHeader + size
            filename = filename.ljust(self.args["_filename_size"], ";")
            filename = bytearray(filename,'utf-8')
            fileHeader = fileHeader + filename
            return fileHeader
    
    def getFileHeader(self, finalBlob, index, caller):
        # from the big blob, get a file header for a file. Read from index pointer. Return a dictionary
        fileHeader = {}
        filesize = bytearray()
        for _ in range(0,self.args["_cs_size"]):    # 8 bytes to store bytes count 
            filesize.append(finalBlob[index])
            index = index + 1
        filesize = int.from_bytes(filesize, byteorder=self.args["_endian"])
        # get other file header info here
        filename = bytearray()
        for _ in range(0,self.args["_filename_size"]):
            filename.append(finalBlob[index])
            index = index + 1
        filename = filename.decode("utf-8")
        filename = filename.split(";")
        filename = filename[0]
        fileHeader["filesize"] = filesize
        fileHeader["filename"] = filename
        return fileHeader, index