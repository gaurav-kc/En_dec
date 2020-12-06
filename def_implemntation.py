import hashlib
import os

class def_behaviour():
    def __init__(self):
        self._filecount_size = 8
        self._cs_size = 4
        self._dec_key_size = 4
        self._pass_size = 20
        
    def encrypt(self,b,key):
        # by default, this is simple byte level encryption where we add key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b

    def getDecryptionKey(self,key):
        # in this function, by default we have to return the corresponding decryption key to your encryption key
        # this is important as decryption key is included in header while encrypting
        return (256-key)

    def getHeader(self,files_count,chunksize,key,endian,default_password,is_pass_protected):
        header = bytearray()  # this will have the entire header
        files_count = files_count.to_bytes(self._filecount_size, endian)   #conv to bytearray
        cs_bytes = chunksize.to_bytes(self._cs_size,endian)     #conv to bytearray
        dec_key = self.getDecryptionKey(key)
        key_bytes = dec_key.to_bytes(self._dec_key_size,endian) #conv to bytearray

        password = default_password
        # we have to ask for password only when -p flag is specified
        if is_pass_protected == True:
            print("Enter password")
            password = input()
            if len(password) == 0:
                print("No password given. Creating unprotected files..")
            else:
                password = password.strip(" ")
                password = password.strip("\n")

        password = self.getPassHash(password)
        self._pass_size = len(password)
        header = header + files_count + cs_bytes + key_bytes + password
        return header

    def decrypt(self,b,key):
        # by default, this is simple byte level decryption where we add dec key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b

    def decodeHeader(self,finalres,endian):
        # given the block, we have to decode header and return header contents.

        index = 0 
        # we have filecount at beginning
        opfilecount = bytearray() 
        for i in range(0,self._filecount_size):
            opfilecount.append(finalres[index])
            index = index + 1
        opfilecount = int.from_bytes(opfilecount, byteorder=endian)
        # followed by chunkize
        chunk_bytes = bytearray()
        for i in range(0,self._cs_size):
            chunk_bytes.append(finalres[index])
            index = index + 1
        chunksize = int.from_bytes(chunk_bytes, byteorder=endian)
        # followed by key (decrpytion key)
        key_bytes = bytearray()
        for i in range(0,self._dec_key_size):
            key_bytes.append(finalres[index])
            index = index + 1
        key = int.from_bytes(key_bytes, byteorder=endian)
        # followed by password hash value
        pass_bytes = bytearray()
        for i in range(0,self._pass_size):
            pass_bytes.append(finalres[index])
            index = index + 1
        return opfilecount, chunksize, key, pass_bytes, index
    
    def getPassHash(self,password):
        # by default we use sha1 to hash the password
        dig = hashlib.sha1(password.encode())
        return dig.digest()

    def encodeBytes(self,b,format):
        # no as such format specific modification by default
        return b
    
    def decodeBytes(self,b,format):
        # no as such format specific modification by default
        return b

    def enc_filenames(self,rel_pathname,allowed_formats):
        # task is to return list of filenames, list of respective formats, encoded string of all original filenames
        tfile_names = os.listdir(rel_pathname)
        file_names = []
        formats = []
        filenames_enc = str()
        #analyze these names of files in directory
        for tfile in tfile_names:
            temp = tfile.split(".")
            #only one dot is allowed in filename
            if len(temp) != 2:
                print("Incorrect format ",tfile, " skipping it.")
                continue
            #check for delimeter
            temp1 = tfile.split(";")
            if len(temp1) != 1:
                print("; found in ",tfile," which is not allowed")
                continue
            format = temp[1]
            #check if file has format in our list
            if format not in allowed_formats:
                print("Excluding file ",tfile)
                continue
            file_names.append(tfile)
            formats.append(format)
            filenames_enc = filenames_enc + tfile + ";"

        # this was added to restore the original filenames 
        # it is of type filename1;filename2; .. filenamek;
        filenames_enc = bytearray(filenames_enc,'utf-8')
        return file_names, formats, filenames_enc

