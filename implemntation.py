import hashlib
import os
class template():
    def __init__(self, default_imp):
        self.default = default_imp

    def encrypt(self,b,key):
        return self.default.encrypt(b,key)

    def getDecryptionKey(self,key):
        return self.default.getDecryptionKeykey(key)

    def getHeader(self,files_count,chunksize,key,endian,default_password,is_pass_protected):
        return self.default.getHeader(files_count,chunksize,key,endian,default_password,is_pass_protected)

    def decrypt(self,b,key):
        return self.default.decrypt(b,key)

    def decodeHeader(self,finalres,endian):
        return self.default.decodeHeader(finalres,endian)
    
    def getPassHash(self,password):
        return self.default.getPassHash(password)

    def encodeBytes(self,b,format):
        return self.default.encodeBytes(b,format)
    
    def decodeBytes(self,b,format):
        return self.default.decodeBytes(b,format)
    
    def enc_filenames(self,rel_pathname,allowed_formats):
        return self.default.enc_filenames(rel_pathname, allowed_formats)

class def_behaviour():
    def encrypt(self,b,key):
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b

    def getDecryptionKey(self,key):
        return (256-key)

    def getHeader(self,files_count,chunksize,key,endian,default_password,is_pass_protected):
        header = bytearray()  # this will have the entire bytearray
        files_count = files_count.to_bytes(8, endian)   #conv to bytearray
        cs_bytes = chunksize.to_bytes(4,endian)
        dec_key = self.getDecryptionKey(key)
        key_bytes = dec_key.to_bytes(4,endian)

        password = default_password
        if is_pass_protected == True:
            print("Enter password")
            password = input()
            if len(password) == 0:
                print("No password given. Creating unprotected files..")
            else:
                password = password.strip(" ")
                password = password.strip("\n")

        password = self.getPassHash(password)

        header = header + files_count + cs_bytes + key_bytes + password
        return header

    def decrypt(self,b,key):
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b

    def decodeHeader(self,finalres,endian):
        index = 0 
        opfilecount = bytearray() 
        for i in range(0,8):
            opfilecount.append(finalres[index])
            index = index + 1
        opfilecount = int.from_bytes(opfilecount, byteorder=endian)
        chunk_bytes = bytearray()
        for i in range(0,4):
            chunk_bytes.append(finalres[index])
            index = index + 1
        chunksize = int.from_bytes(chunk_bytes, byteorder=endian)
        key_bytes = bytearray()
        for i in range(0,4):
            key_bytes.append(finalres[index])
            index = index + 1
        key = int.from_bytes(key_bytes, byteorder=endian)
        pass_bytes = bytearray()
        for i in range(0,20):
            pass_bytes.append(finalres[index])
            index = index + 1
        return opfilecount, chunksize, key, pass_bytes, index
    
    def getPassHash(self,password):
        dig = hashlib.sha1(password.encode())
        return dig.digest()

    def encodeBytes(self,b,format):
        return b
    
    def decodeBytes(self,b,format):
        return b

    def enc_filenames(self,rel_pathname,allowed_formats):
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
            filename = temp[0]
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

class myImplementation(template):
    def encrypt(self,b,key):
        return super().encrypt(b,key)

    def getDecryptionKey(self,key):
        return super().getDecryptionKey(key)

    def getHeader(self,files_count,chunksize,key,endian,default_password,is_pass_protected):
        return super().getHeader(files_count,chunksize,key,endian,default_password,is_pass_protected)

    def decrypt(self,b,key):
        return super().decrypt(b,key)

    def decodeHeader(self,finalres,endian):
        return super().decodeHeader(finalres,endian)
    
    def getPassHash(self,password):
        return super().getPassHash(password)

    def encodeBytes(self,b,format):
        return super().encodeBytes(b,format)
    
    def decodeBytes(self,b,format):
        return super().decodeBytes(b,format)
    
    def enc_filenames(self,rel_pathname,allowed_formats):
        return super().enc_filenames(rel_pathname,allowed_formats)