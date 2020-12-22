# this file is to handle various encryption schemes based upon the mode 
# in the pipeline, create an object of class blob_encrpytion and call encrypt and decrypt functions with mode
# as per the value of mode, appropriate encryption and decryption class will be called
# Also, while creating the object for class blob_encrpytion, there params need to be given
# 1. flags -> for code to get access to any flags 
# 2. args -> for code to get access to args 
# 3. self -> (reference to self) which is required to call any function which is present in the caller class

class blob_encrpytion:
    def __init__(self, flags, args, caller):
        self.flags = flags
        self.args = args
        self.caller = caller
    
    def encrypt(self, mode, blob):
        encblob = None
        if mode == 0:
            enmode = default_mode(self.flags, self.args)
            encblob = enmode.encrypt(blob, self.caller)
        # add new modes here
        if encblob is None:
            print("Some error occured while encrypting with mode ",mode)
            exit(0)
        return encblob

    def decrypt(self, mode, blob, key):
        decblob = None
        if mode == 0:
            decmode = default_mode(self.flags, self.args)
            decblob = decmode.decrypt(blob, key, self.caller)
        # add new modes here
        if decblob is None:
            print("Some error occured while decrypting with mode ",mode)
            exit(0)
        return decblob
    
    def getDecryptionKey(self, mode):
        dec_key = None
        if mode == 0:
            getdec = default_mode(self.flags, self.args)
            dec_key = getdec.getDecryptionKey(self.caller)
        if dec_key is None:
            print("Some error occured while getting description key in mode ",mode)
        return dec_key

    
class default_mode():
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
    
    def encrypt(self,blob, caller):
        # function called when a blob has to be encrypted
        # by default, this is simple byte level encryption where we add key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(blob)):
            blob[i] = (blob[i] + self.args["key"])%256
        return blob

    def decrypt(self,blob,key, caller):
        # this function is called when we have to decrypt a file blob
        # by default, this is simple byte level decryption where we add dec key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(blob)):
            blob[i] = (blob[i] + key)%256
        return blob
    
    def getDecryptionKey(self, caller):
        # in this function, by default we have to return the corresponding decryption key to your encryption key
        # this is important as decryption key is included in header while encrypting
        # by default the decryption key is 256 - encrpytion key
        key = self.args["key"]
        if key<0 or key>256:
            print("Key has to be between 0 to 256")
            exit(0)
        dec_key = 256 - key
        return dec_key