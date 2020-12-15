import hashlib
import os

class enc_def_behaviour(): 
    def initialize(self, flags, args):
        self.flags = flags
        self.args = args

    def encrypt(self,b):
        # by default, this is simple byte level encryption where we add key to byte and take % 256 as byte as 0-255 range
        for i in range(0,len(b)):
            b[i] = (b[i] + self.args["key"])%256
        return b

    def getDecryptionKey(self):
        # in this function, by default we have to return the corresponding decryption key to your encryption key
        # this is important as decryption key is included in header while encrypting
        dec_key = 256 - self.args["key"]
        return dec_key
    
    def getPassHash(self,password):
        # by default we use sha1 to hash the password
        dig = hashlib.sha1(password.encode())
        return dig.digest()

    def getMetaInformation(self):
        #return number of files and list of filenames which will be processed
        args = self.args
        flags = self.flags
        real_pathname = os.path.join(args["current_dir"],args["ip_directory_name"])
        #check input directory name is correct or not 
        isdirectory = os.path.isdir(real_pathname)
        if not isdirectory:
            print(args["ip_directory_name"]," not found")
            exit(-1)
        if flags["is_debug_mode"]:
            print("Looking for files in ",real_pathname)
        filenames = self.getFilenames(real_pathname)
        filecount = len(filenames)
        return filecount, filenames
        
    def getFilenames(self, path):
        #return list of file names in a folder (expects a path)
        tfile_names = os.listdir(path)
        filenames = []
        finalformatlist = self.args["finalformatlist"]
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
            if len(finalformatlist) > 0:
                if format not in finalformatlist:
                    if not self.flags["is_warning_suppressed"]:
                        print("Excluding file ",tfile)
                    continue
            filenames.append(tfile)
        return filenames

    def constructHeader(self, filecount):
        args = self.args
        flags = self.flags

        if filecount == 0:
            print("Nothing to encrpyt")
            return 
        if flags["is_debug_mode"]:
            print("File count is ",filecount)
        
        header = bytearray()  # this will have the entire header
        files_count = filecount.to_bytes(args["_filecount_size"], args["_endian"])   #conv to bytearray
        chunksize = args["chunksize"]
        cs_bytes = chunksize.to_bytes(args["_cs_size"],args["_endian"])     #conv to bytearray
        dec_key = self.getDecryptionKey()
        key_bytes = dec_key.to_bytes(args["_dec_key_size"],args["_endian"]) #conv to bytearray

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

        password = self.getPassHash(password)
        header = header + files_count + cs_bytes + key_bytes + password
        return header

    def constructBlob(self, filenames):
        args = self.args
        flags = self.flags
        #now for each file we append byte_count followed by encrypted bytes
        filesblob = bytearray()
        for i in range(0,len(filenames)):
            filepath = os.path.join(args["current_dir"],args["ip_directory_name"],filenames[i])
            #encodeFile function can be used to encode the file as per format
            #for example, use an auto encoder to compress an image. And use that compressed representation to store that image
            #similarly, pdfs and other formatted files can be modified to either compress or have some meta info for recovery etc
            b = self.encodeFile(filepath, filenames[i])
            size = int(len(b))
            #the bytes should be encrypted. Right now it uses byte level encryption and simply adds key and takes % 256. (as a byte is 0-255)
            #you can implement various encrpytion algorithms. Even on groups of bytes. Key is given 4Bytes in header but can be dec/inc as per req
            b = self.encrypt(b)
            #append the size 
            size = size.to_bytes(args["_cs_size"],args["_endian"])  
            filesblob = filesblob + size + b  #append byte count and that many bytes
        if flags["is_debug_mode"]:
            print("Size of files blob is ", len(filesblob))
        return filesblob
    
    def encodeFile(self, filepath, filename):
        with open(filepath,"rb") as temp_file:
            f = temp_file.read()
            b = bytearray(f)
            return b

    def constructFilenameBlob(self, filenames):
        filenames_enc = str()
        for tfile in filenames:
            filenames_enc = filenames_enc + tfile + ";"
        # this will be added to restore the original filenames 
        # it is of type filename1;filename2; .. filenamek;
        filenames_enc = bytearray(filenames_enc,'utf-8')
        return filenames_enc

    def chunkBlob(self, blob):
        # now we have all bytes in blob variable.
        # we need to chunk it
        # a warning is given as small chunk size can create millions of chunks
        args = self.args
        flags = self.flags
        chunkcount = int(len(blob)/args["chunksize"]) + 1 
        if not flags["is_warning_suppressed"]:
            print(chunkcount, " chunks will form. Are you sure you want to continue? y/n")
            choice = input()
            if choice != "y":
                exit(0)

        chunk_array = []    # this will be array of bytearrays where each bytearray is a chunk of size chunksize (except last)
        i = 0
        while i < len(blob):
            chunk = bytearray()
            j = 0
            while (j < args["chunksize"]) and (i<len(blob)):
                chunk.append(blob[i])
                i = i+1
                j = j+1
            chunk_array.append(chunk)
        if flags["is_debug_mode"]:
            print("Number of chunks created = ",len(chunk_array))
        return chunk_array
    
    def saveChunks(self, chunk_array):
        args = self.args
        flags = self.flags
        output_direc = os.path.join(args["current_dir"],args["op_directory_name"])
        # check if the output directory exists
        if not os.path.exists(output_direc):
            os.mkdir(output_direc)
        else:
            #if it does, we show a warning 
            print("The destination folder exists. All Files will be safe")
            print("In case, same named files are already there, operation will be aborted")
            print("continue? y/n")
            choice = input()
            if choice != "y":
                exit(0)
        encryptedFilenames = self.getEncryptedFilenames(len(chunk_array))
        if flags["is_debug_mode"]:
            print(len(encryptedFilenames), " chunks will be created")
        for chunkNumber in range(0,len(chunk_array)):
            chunkname = os.path.join(output_direc,encryptedFilenames[chunkNumber])
            if os.path.exists(chunkname) == True:
                # The file already exists. Even if we overwrite, the but we are not able to overwrite all chunks,
                # while decrypting it will be error
                # best is to roll back. We could have halted but then incomplete chunks will exist 
                print("Existing file ",chunkname," found. Rolling back changes")
                self.abrupt_abortion(chunkNumber, encryptedFilenames)
                exit(0)
            f = open(chunkname,"wb")
            f.write(chunk_array[chunkNumber])
            f.close()       # this is important :D   

    def getEncryptedFilenames(self, chunkcount):
        args = self.args
        chunk_names = []
        for i in range(0, chunkcount):
            chunkname = args["_commonname"] + args["_delimeter"] + str(i) + "." + args["_opformat"]
            chunk_names.append(chunkname)
        return chunk_names
    
    def abrupt_abortion(self, chunkNumber, encryptedFilenames):
        # a function to roll back changes used in the loop later
        # say in the destination directory, we find an existing chunk
        # then we have to roll back changes 
        output_direc = os.path.join(self.args["current_dir"],self.args["op_directory_name"])
        for i in range(0,chunkNumber):
            chunkname = os.path.join(output_direc,encryptedFilenames[i])
            try:
                os.remove(chunkname)
            except FileNotFoundError:
                print("Did not find ",chunkname)