# this file is to handle various implementations of primary header
# create an object of class primary_header and call constructHeader and decodeHeader with mode value 
# Also, while creating the object for class primary_header, there params need to be given
# 1. flags -> for code to get access to any flags 
# 2. args -> for code to get access to args 
# 3. self -> (reference to self) which is required to call any function which is present in the caller class

from datetime import datetime

class primary_header():
    def __init__(self, flags, args, caller):
        self.flags = flags
        self.args = args
        self.caller = caller
    
    def constructHeader(self, mode, MetaInformation):
        header = None
        if mode == 0:
            consheader = default_mode(self.flags, self.args)
            try:
                header = consheader.constructHeader(MetaInformation, self.caller)
            except NotImplementedError:
                print("Function to construct header need to be defined")
        if header is None:
            print("There was some problem while constructing header in mode ",mode)
        return header
    
    def decodeHeader(self,mode, finalBlob, index):
        header = None
        retindex = -1
        if mode == 0:
            decheader = default_mode(self.flags, self.args)
            try:
                header, retindex = decheader.decodeHeader(finalBlob, index, self.caller)
            except NotImplementedError:
                print("Function to decode header need to be defined")
        if header is None or retindex == -1:
            print("There was some problem while decoding header in mode ",mode)
        return header, retindex
    
class default_mode():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
    
    def constructHeader(self, MetaInformation, caller):
        # using the metainformation, flags and arguments, this function constructs the primary header.
        # the header is appended after encodeMode
        filecount = MetaInformation["filecount"]
        curr_timestamp = int(datetime.now().timestamp()) # stores the encoding timestamp
        args = self.args
        flags = self.flags

        if filecount == 0:
            print("Nothing to encrpyt")
            exit(0)
        if flags["is_debug_mode"]:
            print("File count is ",filecount)
        
        header = bytearray()  # this will have the entire header
        files_count = filecount.to_bytes(args["_filecount_size"], args["_endian"])   # conv to bytearray
        timestamp_bytes = curr_timestamp.to_bytes(8, args["_endian"]) # conv to bytearray
        dec_key = caller.getDecryptionKey()
        key_bytes = dec_key.to_bytes(args["_dec_key_size"],args["_endian"]) # conv to bytearray
        password = args["_default_password"]
        # we have to ask for password only when -p flag is specified
        if flags["is_pass_protected"] == True:
            print("Enter password")
            password = input()
            if len(password) == 0:
                print("No password given. Creating unprotected files..")
            else:
                password = password.strip(" ")
                password = password.strip("\n")
        password = caller.getPassHash(password)
        
        header = files_count + timestamp_bytes + key_bytes + password
        # append header to the encodemode
        return header
    
    def decodeHeader(self,finalBlob, index, caller):
        # given the final blob (the whole blob), we have to decode header and return header contents as a dictionary
        args = self.args
        # we have filecount at beginning
        opfilecount = bytearray() 
        for _ in range(0,args["_filecount_size"]):
            opfilecount.append(finalBlob[index])
            index += 1
        opfilecount = int.from_bytes(opfilecount, byteorder=args["_endian"])
        # followed by encoding timestamp
        enc_timestamp = bytearray()
        for _ in range(8):
            enc_timestamp.append(finalBlob[index])
            index += 1
        enc_timestamp = int.from_bytes(enc_timestamp, byteorder=args["_endian"])        
        enc_datetime = str(datetime.fromtimestamp(enc_timestamp))
        # followed by key (decrpytion key)
        key_bytes = bytearray()
        for _ in range(0,args["_dec_key_size"]):
            key_bytes.append(finalBlob[index])
            index += 1
        key = int.from_bytes(key_bytes, byteorder=args["_endian"])
        # followed by password hash value
        pass_bytes = bytearray()
        for _ in range(0,args["_pass_size"]):
            pass_bytes.append(finalBlob[index])
            index = index + 1
        header = {}
        header["opfilecount"] = opfilecount
        header["enc_datetime"] = enc_datetime
        header["key"] = key
        header["pass_bytes"] = pass_bytes
        return header, index