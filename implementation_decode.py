import hashlib
import os
from file_encode_types import file_enocde_mode
from file_header_types import file_header
from primary_header_types import primary_header
from encrypt_types import blob_encrpytion
from universal import commonFunctions
class dec_def_behaviour():   
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
        self.file_enocde_mode = file_enocde_mode(flags, args, self)
        self.file_header = file_header(flags, args, self)
        self.primary_header = primary_header(flags, args, self)
        self.blob_encrpytion = blob_encrpytion(flags, args, self)
        self.universal = commonFunctions(flags, args)

    def decrypt(self,blob,key):
        # this function is called when we have to decrypt a file blob
        # by default, this is simple byte level decryption where we add dec key to byte and take % 256 as byte as 0-255 range
        blob = self.blob_encrpytion.decrypt(self.args["encryptMode"], blob, key)
        return blob
    
    def decodeFile(self, fileblob, filename, fileHeader):
        # this function is called when a fileblob has to be decoded. The filename is to get the format and decode blob accordingly.
        # by default does nothing
        fileblob = self.file_enocde_mode.decodeFile(self.args["encodeMode"], fileblob, filename, fileHeader)
        return fileblob

    def decodeHeader(self,finalBlob, index):
        # given the final blob (the whole blob), we have to decode header and return header contents as a dictionary
        header, index = self.primary_header.decodeHeader(self.args["primaryHeaderMode"], finalBlob, index)
        return header, index
    
    def checkPassword(self, header):
        # we need to check for password. 
        # def_digest is hash for _default_password
        # if it matches with the passowrd in header, it means no password was set
        # but if it doesn't, password was set
        pass_bytes = header["pass_bytes"]
        def_digest = self.getPassHash(self.args["_default_password"])
        if def_digest != pass_bytes:
            #it was a protected file
            count = 3   #number of attempts.
            while count != 0:
                count = count - 1
                print("Enter password ")
                password = input()
                # calc hash of password and compare it with what we had
                ip_bytes = self.getPassHash(password)
                if ip_bytes != pass_bytes:
                    if count == 0:
                        print("Attempts exceeded. Exiting")
                        exit(0)
                    print("Incorrect password.",count," attempts remain")
                    continue
                else:
                    #password was correct
                    return

    def getFileHeader(self, finalBlob, index):
        # from the big blob, get a file header for a file. Read from index pointer. Return a dictionary
        fileHeader, index = self.file_header.getFileHeader(self.args["fileHeaderMode"], finalBlob, index)
        return fileHeader, index

    def getFileInfoList(self, finalBlob, index, header):
        # now we know files count 
        # we know that starting from the index, we have 
        # <file1Header,filebytes> <file2Header,filebytes> .. <filekHeader,filebytes>
        # so we first read tehe header, then the blob. And make a dictionary and return a list of such dictionary
        opfilecount = header["opfilecount"]
        filesInfoList = []
        bytes_list = [] #this will have list of bytearrays
        for _ in range(opfilecount):
            fileHeader, index = self.getFileHeader(finalBlob, index)
            filesize = fileHeader["filesize"]
            temp = bytearray()
            for _ in range(0,filesize): # read that many bytes
                temp.append(finalBlob[index])
                index = index + 1
            fileInfo = {}
            fileInfo["blob"] = temp
            fileInfo["fileHeader"] = fileHeader
            filesInfoList.append(fileInfo)
        if self.flags["is_debug_mode"]:
            print("Number of files recovered is ",len(bytes_list))
        return filesInfoList, index

    def recoverFiles(self, filesInfoList, header):
        # in this function, given a list of dictionaries, and header (for key), decrypt and decode the file and save the file in output folder 
        args = self.args
        # flags = self.flags
        key = header["key"]
        opdir_path = os.path.join(args["current_dir"],args["op_directory_name"])
        # check if destination directory exists
        if not os.path.exists(opdir_path):
            os.mkdir(opdir_path)
        else:
            #if it does, we show a warning 
            print("The destination folder exists. All Files will be safe")
            print("In case, same named files are already there, you will be warned")
            print("continue? y/n")
            choice = input()
            if choice != "y":
                exit(0)
        for i in range(0, len(filesInfoList)):
            fileHeader = filesInfoList[i]["fileHeader"]
            filename = fileHeader["filename"]
            filepath = os.path.join(opdir_path, filename)
            # check if file exists 
            if os.path.exists(filepath):
                print("The file ",filename, " already exists. Overwrite it? y/n")
                choice = input()
                if choice != "y":
                    # if the file need not be overwritten, create a copy_of_<filename> file
                    print("Creating a copy")
                    filename = "Copy_of_" + filename
                    filepath = os.path.join(opdir_path, filename)
            blob = filesInfoList[i]["blob"]
            blob = self.decrypt(blob, key)
            blob = self.decodeFile(blob,filename,fileHeader)
            f = open(filepath, "wb")
            f.write(blob)
            f.close() # this is important ;p
    
    def setArgs(self, index, finalBlob):
        encodeMode = bytearray() 
        for _ in range(0,self.args["_encode_mode_size"]):
            encodeMode.append(finalBlob[index])
            index = index + 1
        encodeMode = int.from_bytes(encodeMode, byteorder=self.args["_endian"])

        encryptMode = bytearray() 
        for _ in range(0,self.args["_encrypt_mode_size"]):
            encryptMode.append(finalBlob[index])
            index = index + 1
        encryptMode = int.from_bytes(encryptMode, byteorder=self.args["_endian"])

        primaryHeaderMode = bytearray() 
        for _ in range(0,self.args["_primary_header_mode_size"]):
            primaryHeaderMode.append(finalBlob[index])
            index = index + 1
        primaryHeaderMode = int.from_bytes(primaryHeaderMode, byteorder=self.args["_endian"])

        fileHeaderMode = bytearray() 
        for _ in range(0,self.args["_file_header_mode_size"]):
            fileHeaderMode.append(finalBlob[index])
            index = index + 1
        fileHeaderMode = int.from_bytes(fileHeaderMode, byteorder=self.args["_endian"])

        self.args["encodeMode"] = encodeMode
        self.args["encryptMode"] = encryptMode
        self.args["primaryHeaderMode"] = primaryHeaderMode
        self.args["fileHeaderMode"] = fileHeaderMode

        return index
    
    def getPassHash(self,password):
        # this function is called when a password has to be hashed
        # by default we use sha1 to hash the password
        # make sure you use same algo while encrpyting
        dig = hashlib.sha1(password.encode())
        return dig.digest()
