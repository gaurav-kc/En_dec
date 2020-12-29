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

    def constructFileHeader(self, mode, size, filepath): 
        fileHeader = None
        if mode == 0:
            consFileHeader = default_mode(self.flags, self.args)
            try:
                fileHeader = consFileHeader.constructFileHeader(size, filepath, self.caller)
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

    def constructFileHeader(self, size, filepath, caller):
            # with the argument provided, this function creates file header for a particular file
            fileHeader = bytearray()
            size = size.to_bytes(self.args["_cs_size"],self.args["_endian"])
            fileHeader = fileHeader + size
            filepath = str(filepath)
            filepath = filepath.ljust(self.args["_filepath_size"], ";")
            filepath = bytearray(filepath,'utf-8')
            fileHeader = fileHeader + filepath
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
        filepath = bytearray()
        for _ in range(0,self.args["_filepath_size"]):
            filepath.append(finalBlob[index])
            index = index + 1
        filepath = filepath.decode("utf-8")
        filepath = filepath.split(";")
        filepath = filepath[0]
        fileHeader["filesize"] = filesize
        fileHeader["filepath"] = filepath
        return fileHeader, index