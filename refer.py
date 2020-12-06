from def_implemntation import def_behaviour
# this is for reference.
# copy paste this to create your implementation. Change classname. 
# if you want any function to behave by default, leave it as it is.
# if you wish to add to what a function does, catch paramters in local variables returned by super().<fn_name> and modify and return
# if you wish to completly change implementation of a function, remove the return line. See what that function returns and write function like that

class myImplementation(def_behaviour):
    def encrypt(self,b,key):
        # you can modify how the bytes are encrypted 
        return super().encrypt(b,key)

    def getDecryptionKey(self,key):
        # when you implement your own encryption algo, return a decrytion key accoording to it. Note that key size is set to 4 bytes
        return super().getDecryptionKey(key)

    def getHeader(self,files_count,chunksize,key,endian,default_password,is_pass_protected):
        # given all those params, construct your own header.
        return super().getHeader(files_count,chunksize,key,endian,default_password,is_pass_protected)

    def decrypt(self,b,key):
        # mention custon decryption mechanism
        return super().decrypt(b,key)

    def decodeHeader(self,finalres,endian):
        # if you made a custom header, write logic to decode it 
        return super().decodeHeader(finalres,endian)
    
    def getPassHash(self,password):
        # use any other password hashing mechanism here
        return super().getPassHash(password)

    def encodeBytes(self,b,format):
        # do any file format specific encoding here (to compress or anything)
        return super().encodeBytes(b,format)
    
    def decodeBytes(self,b,format):
        # given encoded bytes for a file and format, decode it as per how it was encoded
        return super().decodeBytes(b,format)
    
    def enc_filenames(self,rel_pathname,allowed_formats):
        # create your own mechanism to encode all original filenames here
        return super().enc_filenames(rel_pathname,allowed_formats)
