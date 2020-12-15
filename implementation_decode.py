import hashlib
import os

class dec_def_behaviour():   
    def initialize(self, flags, args):
        self.flags = flags
        self.args = args

    def decrypt(self,b,key):
        # by default, this is simple byte level decryption where we add dec key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(b)):
            b[i] = (b[i] + key)%256
        return b

    def decodeHeader(self,finalBlob):
        # given the block, we have to decode header and return header contents.
        index = 0 
        args = self.args
        # we have filecount at beginning
        opfilecount = bytearray() 
        for _ in range(0,args["_filecount_size"]):
            opfilecount.append(finalBlob[index])
            index = index + 1
        opfilecount = int.from_bytes(opfilecount, byteorder=args["_endian"])
        # followed by chunkize
        chunk_bytes = bytearray()
        for _ in range(0,args["_cs_size"]):
            chunk_bytes.append(finalBlob[index])
            index = index + 1
        chunksize = int.from_bytes(chunk_bytes, byteorder=args["_endian"])
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
        header["chunksize"] = chunksize
        header["key"] = key
        header["pass_bytes"] = pass_bytes
        
        return header, index
    
    def getPassHash(self,password):
        # by default we use sha1 to hash the password
        dig = hashlib.sha1(password.encode())
        return dig.digest()

    def decodeFile(self, fileblob, filename):
        return fileblob

    def identifyChunks(self):
        # check if given directory exists
        args = self.args
        flags = self.flags
        dir_path = os.path.join(args["current_dir"],args["ip_directory_name"])
        if not os.path.exists(dir_path):
            print("Directory not found")
            exit(0)
        if flags["is_debug_mode"]:
            print("Looking for files in ",dir_path)
        # this step is to avoid all other files apart from what we recognize as chunk
        # we only take count of such files and assume the files are from 0 to filecount-1 (maybe not the best way)
        all_files = os.listdir(dir_path)
        chunkcount = 0
        for afile in all_files:
            if self.isChunk(afile):
                chunkcount = chunkcount + 1
        if chunkcount == 0:
            print("No compatible files found")
            exit(0)
        if flags["is_debug_mode"]:
            print("Number of chunks found is ",chunkcount)
        return chunkcount

    def isChunk(self, filename):
        filename = filename.split(".")
        if len(filename) != 2:
            return False
        format = filename[-1]
        if format == self.args["_opformat"]:
            return True
        return False
    
    def constructBlob(self, chunkcount):
        # finalBlob will have the entire bytes 
        args = self.args
        flags = self.flags
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
        finalBlob = finalBlob + b     # append bytearray of current file to finalres
        file_obj.close() 
        if flags["is_debug_mode"]:
            print("Size of entire blob is ",len(finalBlob))
        return finalBlob
    
    def checkPassword(self, pass_bytes):
        # we need to check for password. 
        # def_digest is hash for default password
        # if it matches with the passowrd in header, it means no password was set
        # but if it doesn't, password was set
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

    def getFileBlobList(self, finalBlob, index, opfilecount):
        # now we know files count 
        # we know that starting from the index, we have 
        # <file1info,filebytes> <file2size,filebytes> .. <fileksize,filebytes> <semicolon seperated names of all files in same order>
        # so we read that many bytes (each such bytes will be one decrypted file) and store then in an array and store that bytearray in an array
        bytes_list = [] #this will have list of bytearrays
        for i in range(opfilecount):
            filesize = bytearray()
            for j in range(0,self.args["_cs_size"]):    # 8 bytes to store bytes count 
                filesize.append(finalBlob[index])
                index = index + 1
            filesize = int.from_bytes(filesize, byteorder=self.args["_endian"])
            temp = bytearray()
            for j in range(0,filesize): # read that many bytes
                temp.append(finalBlob[index])
                index = index + 1
            bytes_list.append(temp) # read filesize bytes into seperate bytearray and add it to the list
        if self.flags["is_debug_mode"]:
            print("Number of files recovered is ",len(bytes_list))
        return bytes_list, index

    def getActualNames(self, finalBlob, index):
        # after storing all file bytes, we had encoded and appended semi-colon seperated list of original filenames
        # we recover it now
        actual_names = bytearray()  
        while index < len(finalBlob):
            actual_names.append(finalBlob[index])
            index = index + 1
        actual_names = actual_names.decode("utf-8") #decode that bytearray into string
        actual_names = actual_names.split(";")
        actual_names.pop() # last element will be empty as format was filename1;filename2; .. filenamek;
        if self.flags["is_debug_mode"]:
            print("Names for",len(actual_names),"files were found")
        return actual_names

    def recoverFiles(self, bytes_list, actual_names, key):
        args = self.args
        flags = self.flags
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
        for i in range(0, len(bytes_list)):
            filepath = os.path.join(opdir_path, actual_names[i])
            # check if file exists 
            if os.path.exists(filepath):
                print("The file ",actual_names[i], " already exists. Overwrite it? y/n")
                choice = input()
                if choice != "y":
                    print("Creating a copy")
                    filename = "Copy_of_" + actual_names[i]
                    filepath = os.path.join(opdir_path, filename)
            b = self.decrypt(bytes_list[i], key)
            b = self.decodeFile(b,actual_names[i])
            f = open(filepath, "wb")
            f.write(b)
            f.close() # this is important ;p
    def getEncryptedFilenames(self, chunkcount):
        args = self.args
        chunk_names = []
        for i in range(0, chunkcount):
            chunkname = args["_commonname"] + args["_delimeter"] + str(i) + "." + args["_opformat"]
            chunk_names.append(chunkname)
        return chunk_names