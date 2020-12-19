from implementation_encode import enc_def_behaviour
# create the class that inherits the class enc_def_behaviour
from datetime import datetime
class myImplementation(enc_def_behaviour):
    # and define init function and set the parent class's flags and args
    def __init__(self, flags, args):
        super().initialize(flags, args)

    # this function is to perform all the actions specific to this class after the process is over
    def performSomeAction(self):
        pass
    """
    now here, override the function you want
    say you wish to add date of encoding to the primary header
    we need to change constructheader function here in encoding logic
    observe the function constructHeader. 
    So i override that function. I take the header, and add date and then send it to the main
    """
    def constructHeader(self, MetaInformation, encodeMode):
        header = super().constructHeader(MetaInformation, encodeMode)
        # now we have the default header. We need to set the size for the date time. say 32 bytes
        # to the file flag_and_args.py, in class commonArs, add an argument _date_time as 32.
        # this is necessary so that, while decoding, the decode.py should know how many bytes to read to get date and time 
        # now get the current date and time 
        current = datetime.now()
        date_time_string = current.strftime("%d/%m/%Y %H:%M:%S")
        # convert the string so that we can append to byte array. But first we need to pad it. Let's pad with &
        date_time_string = date_time_string.ljust(self.args["_date_time"], "&")
        date_time_string = bytearray(date_time_string, 'utf-8')
        header = header + date_time_string
        # now in the main, return this header. Now, handle it while decoding header
        return header