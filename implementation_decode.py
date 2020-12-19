import hashlib
import os

class dec_def_behaviour():   
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args

    def initialize(self, flags, args):
        self.flags = flags
        self.args = args

    def decrypt(self,b,key):
        # this function is called when we have to decrypt a file blob
        # by default, this is simple byte level decryption where we add dec key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b
    
    def decodeFile(self, fileblob, filename, fileHeader):
        # this function is called when a fileblob has to be decoded. The filename is to get the format and decode blob accordingly.
        # by default does nothing
        return fileblob

    def decodeHeader(self,finalBlob, index):
        # given the final blob (the whole blob), we have to decode header and return header contents as a dictionary
        args = self.args
        # we have filecount at beginning
        opfilecount = bytearray() 
        for _ in range(0,args["_filecount_size"]):
            opfilecount.append(finalBlob[index])
            index = index + 1
        opfilecount = int.from_bytes(opfilecount, byteorder=args["_endian"])
        # followed by key (decrpytion key)
        key_bytes = bytearray()
        for _ in range(0,args["_dec_key_size"]):
            key_bytes.append(finalBlob[index])
            index = index + 1
        key = int.from_bytes(key_bytes, byteorder=args["_endian"])
        # followed by password hash value
        pass_bytes = bytearray()
        for _ in range(0,args["_pass_size"]):
            pass_bytes.append(finalBlob[index])
            index = index + 1
        header = {}
        header["opfilecount"] = opfilecount
        header["key"] = key
        header["pass_bytes"] = pass_bytes
        return header, index

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

    def getFileBlobList(self, finalBlob, index, header):
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

    def getEncodeCode(self, finalBlob):
        # when the full blob is made, the first _encode_mode_size rep the encode mode, i.e in which mode they were encoded
        index = 0
        encodeMode = bytearray()
        for _ in range(0,self.args["_encode_mode_size"]):
            encodeMode.append(finalBlob[index])
            index = index + 1
        encodeMode = int.from_bytes(encodeMode, byteorder=self.args["_endian"])
        return encodeMode, index
    
    # these functions (below this line) should be present in both and must be exactly same
    def getPassHash(self,password):
        # this function is called when a password has to be hashed
        # by default we use sha1 to hash the password
        dig = hashlib.sha1(password.encode())
        return dig.digest()
    
    def getEncryptedFilenames(self, chunkcount):
        # here is the file naming logic. By default, list of filenames for chunks is a function of chunkcount.
        # if you implement your own logic (say you don't want filenames to appear serially due to <filename>_0 , override this function, but make sure that 
        # the function does not use randomization. For eg, getEncryptedFilenames(5), should always return same list of names. This is required as we need the
        # same list when we have to identify the chunks)
        args = self.args
        chunk_names = []
        for i in range(0, chunkcount):
            chunkname = args["_commonname"] + args["_delimeter"] + str(i) + "." + args["_opformat"]
            chunk_names.append(chunkname)
        return chunk_names