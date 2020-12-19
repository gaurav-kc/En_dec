from implementation_encode import enc_def_behaviour
# create the class that inherits the class enc_def_behaviour
class blankTemplate(enc_def_behaviour):
    # and define init function and set the parent class's flags and args
    def __init__(self, flags, args):
        super().initialize(flags, args)

    # this function is to perform all the actions specific to this class after the process is over
    def performSomeAction(self):
        pass