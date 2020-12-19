from implementation_decode import dec_def_behaviour
# create a class that inherits the class dec_def_behaviour
class myImplementation(dec_def_behaviour):
    def __init__(self, flags, args):
        # set the flags and args for parent class
        super().initialize(flags, args)
        
    # this function is to perform all the actions specific to this class after the process is over
    def performSomeAction(self, header):
        self.printEncodeDateTime(header)
    """
    In encode part, we added date time to the header.
    Now we need to handle that while decoding
    observe the function decodeHeader
    Now override the function and let's append to it's implementation
    """
    def decodeHeader(self,finalBlob, index):
        header, index = super().decodeHeader(finalBlob, index)
        # now, from this index, _date_time bytes I have to read to get the date time 
        datetime = bytearray()
        for _ in range(0, self.args["_date_time"]):
            datetime.append(finalBlob[index])
            index = index + 1
        # now, its a bytearray. Decode it to string 
        datetime = datetime.decode("utf-8")
        datetime = datetime.split("&")
        datetime = datetime[0]
        # add this to the header
        header["datetime"] = datetime
        # and send this modified header to main
        return header, index

    # try printing the date time 
    def printEncodeDateTime(self, header):
        print("These files were encoded at ",header["datetime"])