from implementation_decode import dec_def_behaviour
# create a class that inherits the class dec_def_behaviour
class blankTemplate(dec_def_behaviour):
    def __init__(self, flags, args):
        # set the flags and args for parent class
        super().initialize(flags, args)
        
    # this function is to perform all the actions specific to this class after the process is over
    def performSomeAction(self, header):
        pass
