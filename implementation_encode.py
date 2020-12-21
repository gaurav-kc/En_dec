import hashlib
import os
from file_encode_types import file_enocde_mode
from file_header_types import file_header
from primary_header_types import primary_header
from encrypt_types import blob_encrpytion
from universal import commonFunctions
class enc_def_behaviour(): 
    def __init__(self, flags, args):
        self.flags = flags
        self.args = args
        self.file_enocde_mode = file_enocde_mode(flags, args, self)
        self.file_header = file_header(flags, args, self)
        self.primary_header = primary_header(flags, args, self)
        self.blob_encrpytion = blob_encrpytion(flags, args, self)
        self.universal = commonFunctions(flags, args)
    
    def getPipelineBytes(self):
        pipelineCode = self.args["pipelineCode"]

        pipelineCode = pipelineCode.to_bytes(self.args["_pipeline_code_size"],self.args["_endian"])
        return pipelineCode    

    def encrypt(self,blob):
        # function called when a blob has to be encrypted
        # by default, this is simple byte level encryption where we add key to byte and take % 256 as byte as 0-255 range
        blob = self.blob_encrpytion.encrypt(self.args["encryptMode"], blob)
        return blob
    
    def encodeFile(self, filepath, filename):
        # function takes a filepath and name as args. Here, we can encode a particular file as per format to compress it 
        # or make it robust or for any other purpose
        blob = self.file_enocde_mode.encodeFile(self.args["encodeMode"], filepath, filename)
        return blob

    def getDecryptionKey(self):
        # in this function, by default we have to return the corresponding decryption key to your encryption key
        # this is important as decryption key is included in header while encrypting
        # by default the decryption key is 256 - encrpytion key
        dec_key = self.blob_encrpytion.getDecryptionKey(self.args["encryptMode"])
        return dec_key

    def getMetaInformation(self):
        # this function returns metainformation about the input folder in the form of dictionary. 
        # by default, returns number of files and list of filenames.
        args = self.args
        flags = self.flags
        MetaInformation = {}
        real_pathname = os.path.join(args["current_dir"],args["ip_directory_name"])
        #check input directory name is correct or not 
        isdirectory = os.path.isdir(real_pathname)
        if not isdirectory:
            print(args["ip_directory_name"]," not found")
            exit(-1)
        if flags["is_debug_mode"]:
            print("Looking for files in ",real_pathname)
        filenames = self.getFilenames(real_pathname)    # function call to get only those filenames which we are cosidering
        filecount = len(filenames)
        MetaInformation["filecount"] = filecount
        MetaInformation["filenames"] = filenames
    
        return MetaInformation
        
    def getFilenames(self, path):
        # this function returns a list of only those filenames which have format of our use in the directory at the path 
        tfile_names = os.listdir(path)
        filenames = []
        finalformatlist = self.args["finalformatlist"]
        #analyze these names of files in directory
        for tfile in tfile_names:
            if len(tfile) >= self.args["_filename_size"]:
                print("Filename ",tfile,"too large. Skipping it.")
                continue
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

    def constructHeader(self, MetaInformation):
        # using the metainformation, flags and arguments, this function constructs the primary header.
        # the header is appended after encodeMode
        header = self.primary_header.constructHeader(self.args["primaryHeaderMode"], MetaInformation)
        return header

    def constructFileHeader(self, size, filename):
        # with the argument provided, this function creates file header for a particular file
        fileHeader = self.file_header.constructFileHeader(self.args["fileHeaderMode"], size, filename)
        return fileHeader

    def getFileBlob(self, filepath, filename):
        #encodeFile function can be used to encode the file as per format
        #for example, use an auto encoder to compress an image. And use that compressed representation to store that image
        #similarly, pdfs and other formatted files can be modified to either compress or have some meta info for recovery etc
        b = self.encodeFile(filepath, filename)
        #the bytes should be encrypted. Right now it uses byte level encryption and simply adds key and takes % 256. (as a byte is 0-255)
        #you can implement various encrpytion algorithms. Even on groups of bytes. Key is given 4Bytes in header but can be dec/inc as per req
        b = self.encrypt(b)
        size = int(len(b))
        #append the size 
        fileHeader = self.constructFileHeader(size, filename) 
        fblob = fileHeader + b
        return fblob

    def constructFilesBlob(self, MetaInformation):
        # this function reads each file, encodes it, encrypts it and adds the blobs of all the files and returns it.
        args = self.args
        flags = self.flags
        #now for each file we append byte_count followed by encrypted bytes
        filenames = MetaInformation["filenames"]
        filesblob = bytearray()
        for i in range(0,len(filenames)):
            filepath = os.path.join(args["current_dir"],args["ip_directory_name"],filenames[i])
            fblob = self.getFileBlob(filepath, filenames[i])
            filesblob = filesblob + fblob  #append byte count and that many bytes
        if flags["is_debug_mode"]:
            print("Size of files blob is ", len(filesblob))
        return filesblob

    def chunkBlob(self, blob):
        # now we have all bytes in blob variable.
        # we need to chunk it, break the big blob into pieces
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
        # this function will save each chunk from the list of chunks as a file 
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
        encryptedFilenames = self.universal.getEncryptedFilenames(len(chunk_array))
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

    def getModeBytes(self):
        encodeMode = self.args["encodeMode"]
        encryptMode = self.args["encryptMode"]
        primaryHeaderMode = self.args["primaryHeaderMode"]
        fileHeaderMode = self.args["fileHeaderMode"]

        encodeMode = encodeMode.to_bytes(self.args["_encode_mode_size"],self.args["_endian"])
        encryptMode = encryptMode.to_bytes(self.args["_encrypt_mode_size"],self.args["_endian"])
        primaryHeaderMode = primaryHeaderMode.to_bytes(self.args["_primary_header_mode_size"],self.args["_endian"])
        fileHeaderMode = fileHeaderMode.to_bytes(self.args["_file_header_mode_size"],self.args["_endian"])

        modeBytes = encodeMode + encryptMode + primaryHeaderMode + fileHeaderMode
        return modeBytes
 
    def getPassHash(self,password):
        # this function is called when a password has to be hashed
        # by default we use sha1 to hash the password
        # make sure you use same algo while decrypting
        dig = hashlib.sha1(password.encode())
        return dig.digest()
    