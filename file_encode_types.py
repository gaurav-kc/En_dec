class file_enocde_mode:
    def __init__(self, flags, args, caller):
        self.flags = flags
        self.args = args
        self.caller = caller
    
    def encodeFile(self, mode, filepath, filename):
        blob = None
        if mode == 0:
            enmode = default_mode(self.flags, self.args)
            blob = enmode.encodeFile(filepath, filename, self.caller)
        # add new modes here
        if blob is None:
            print("Some error occured while encoding with mode ",mode)
            exit(0)
        return blob

    def decodeFile(self, mode, fileblob, filename, fileHeader):
        retfileblob = None
        if mode == 0:
            decmode = default_mode(self.flags, self.args)
            retfileblob = decmode.decodeFile(fileblob, filename, fileHeader, self.caller)
        # add new modes here
        if fileblob is None:
            print("Some error occured while decoding in mode ",mode)
            exit(0)
        return retfileblob

class default_mode():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args

    def encodeFile(self, filepath, filename, caller):
        # function takes a filepath and name as args. Here, we can encode a particular file as per format to compress it 
        # or make it robust or for any other purpose
        with open(filepath,"rb") as temp_file:
            f = temp_file.read()
            blob = bytearray(f)
            # by default does nothing
            return blob
    
    def decodeFile(self, fileblob, filename, fileHeader, caller):
        # this function is called when a fileblob has to be decoded. The filename is to get the format and decode blob accordingly.
        # by default does nothing
        return fileblob