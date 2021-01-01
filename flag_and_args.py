# this class is to handle the flags and set the arguments
# with the flags and args as a dictionary, it becomes easy to add flags or arguments and access it anywhere in other files.
# there are 2 classes. enc_flags_and_args and dec_flags_and_args. Respective objects have to be create in respective files 
# create an object and pass the argv and let the class create a dictionary of flags and arguments 
class enc_flags_and_args:
    def getFlagsAndArgs(self,argv,rec_flags=None,rec_args=None):
        # default values 
        ip_directory_name = "testit"   # if not given, expect files in this folder
        op_directory_name = "encrypted"     #if not given, put encrypted files in this folder
        chunksize = 100000   # if not given, consider these many bytes as chunk size
        key = 56    # if not given, consider this value as key for your encryption algorithm
        current_dir = "."
        image_formats = [".jpg",".png",".jpeg",".tiff",".gif"] 
        video_formats = [".mp4",".mov",".mkv",".flv"]
        doc_formats = [".docx",".odt",".xlsx",".ots",".pptx",".odf"]
        prog_formats = [".cpp",".java",".c",",py"]
        finalformatlist = []
        pipelineCode = 0
        encodeMode = 0
        encryptMode = 0
        primaryHeaderMode = 0
        fileHeaderMode = 0
        # flags 
        # currently supported flags. (Input and output directory doesn't need any flag. order doenst matter. Flags and directories can be any order. All are optional)
        # anywhere, first directory name is assumed as input directory name and next as output directory name 
        # by default, input directory is assumed in directory specified in variable directory_name
        # by default, output directory is asssumed in directory specified in variable op_directory_name
        # -cs <chunk_size>  (custom chunk size)
        # -k <key> (custom key)
        # -f  (comma seperated list. Possible elements : images,videos,docs) (consider only those files)
        # -sw (supress warning)
        # -p  (enable password protection)
        # -d  (print debugging statements)
        is_input_directory = False
        is_output_directory = False
        is_chunk_size = False
        is_key = False
        is_format_given = False
        is_pass_protected = False
        is_debug_mode = False
        is_warning_suppressed = False
        is_encodeMode_given = False
        #handling the flags to set/overwrite default values using the command line arguments 
        if argv is not None:
            i = 1
            while i < len(argv):
                if argv[i][0] == "-":
                    flag = argv[i].lstrip("-")
                    # if flag is cs (chunksize)
                    if flag == "cs":
                        is_chunk_size = True    
                        i = i + 1
                        try:
                            chunksize = int(argv[i])
                        except ValueError:
                            print("Chunk size should be an integer")
                            exit(0)
                        except IndexError:
                            print("No chunk size given")
                            exit(0)
                    # if flag is k (key)
                    elif flag == "k":
                        is_key = True
                        i = i + 1
                        try:
                            key = int(argv[i])
                        except ValueError:
                            print("Key should be an integer")
                            exit(0)
                        except IndexError:
                            print("No key given")
                            exit(0)
                    elif flag == "f":
                        is_format_given = True
                        i = i + 1
                        temp = argv[i]
                        temp = temp.split(",")
                        for j in temp:
                            if j == "images":
                                for imgformat in image_formats:
                                    finalformatlist.append(imgformat)
                            elif j == "videos":
                                for vidformat in video_formats:
                                    finalformatlist.append(vidformat)
                            elif j == "docs":
                                for docformat in doc_formats:
                                    finalformatlist.append(docformat)
                            elif j == "prog":
                                for progformat in prog_formats:
                                    finalformatlist.append(progformat)
                            # add another category here 
                            else:
                                print("Unusual paramter",j,"for -f flag found")
                                exit(0)
                        finalformatlist = list(dict.fromkeys(finalformatlist)) # remove duplicates in present
                    elif flag == "sw":
                        is_warning_suppressed = True
                    elif flag == "p":
                        is_pass_protected = True
                    elif flag == "d":
                        is_debug_mode = True
                    # add new flags here 
                    # flags for modes are reamining

                    elif flag == "pipc":
                        i = i + 1
                        try:
                            pipelineCode = int(argv[i])
                        except ValueError:
                            print("Pipeline code should be an integer")
                            exit(0)
                        except IndexError:
                            print("No value for pipeline code")
                            exit(0)

                    elif flag == "enc":
                        i = i + 1
                        try:
                            encodeMode = int(argv[i])
                        except ValueError:
                            print("enc flag expects an integer only as argument")
                            exit(0)
                        except IndexError:
                            print("No value for encode Mode")
                            exit(0)

                    elif flag == "crypt":
                        i = i + 1
                        try:
                            encryptMode = int(argv[i])
                        except ValueError:
                            print("Encryption code should be an integer")
                            exit(0)
                        except IndexError:
                            print("No value for encryption mode")
                            exit(0)
                    
                    elif flag == "phc":
                        i = i + 1
                        try:
                            primaryHeaderMode = int(argv[i])
                        except ValueError:
                            print("Primary header mode should be an integer")
                            exit(0)
                        except IndexError:
                            print("No value for primary header mode")
                            exit(0)
                    
                    elif flag == "fhc":
                        i = i + 1
                        try:
                            fileHeaderMode = int(argv[i])
                        except ValueError:
                            print("File header mode should be an integer")
                            exit(0)
                        except IndexError:
                            print("No value for file header mode")
                            exit(0)

                    else:
                        print("Invalid flag ",flag)
                        exit(0)
                else:
                    if is_input_directory == False:
                        is_input_directory = True
                        ip_directory_name = argv[i]
                    elif is_output_directory == False:
                        is_output_directory = True
                        op_directory_name = argv[i]
                    else:
                        print("Error in this argument",argv[i])
                        exit(0)
                i = i + 1

        flags, args = commonArgs().getCommonFlagsAndArgs()

        flags["is_input_directory"] = is_input_directory
        flags["is_output_directory"] = is_output_directory
        flags["is_chunk_size"] = is_chunk_size
        flags["is_key"] = is_key
        flags["is_format_given"] = is_format_given
        flags["is_pass_protected"] = is_pass_protected
        flags["is_debug_mode"] = is_debug_mode
        flags["is_warning_suppressed"] = is_warning_suppressed
        flags["is_encodeMode_given"] = is_encodeMode_given 
        
        args["ip_directory_name"] = ip_directory_name
        args["op_directory_name"] = op_directory_name
        args["chunksize"] = chunksize
        args["key"] = key
        args["current_dir"] = current_dir
        args["finalformatlist"] = finalformatlist
        args["pipelineCode"] = pipelineCode
        args["encodeMode"] = encodeMode
        args["encryptMode"] = encryptMode
        args["primaryHeaderMode"] = primaryHeaderMode
        args["fileHeaderMode"] = fileHeaderMode
        #anywhere access arguments or flags via this dictionary now

        #overwrite the values if there
        if rec_flags is not None:
            rec_flag_keys = rec_flags.keys()
            for key in rec_flag_keys:
                if key in flags.keys():
                    # maybe put a check before blind assignment 
                    flags[key] = rec_flags[key]
                else:
                    print("Illegal flags key ",key)
        
        if rec_args is not None:
            rec_arg_keys = rec_args.keys()
            for key in rec_arg_keys:
                if key in args.keys():
                    # maybe put a check before blind assignment 
                    args[key] = rec_args[key]
                else:
                    print("Illegal arg key ",key)
        return flags, args
        
            
class dec_flags_and_args:
    def getFlagsAndArgs(self,argv,rec_flags=None,rec_args=None):
        # default values
        ip_directory_name = "encrypted"
        op_directory_name = "decrypted"
        current_dir = "."
        pipelineCode = 0
        encodeMode = 0
        encryptMode = 0
        primaryHeaderMode = 0
        fileHeaderMode = 0
        # presence of default password shows no password was given 

        # user need not remember whatever custom/default chunk value and key was used while encrypting. Hence no flags for that
        # if specified, first directory name will be assumed as input dir name and next as output directory name. Both are optional
        # by default it would assume input from directory name mentioned in variable directory_name
        # by default it would put all recovered files in directory mentioned in variable op_directory_name
        # flags supported
        # -d  (print debugging statements)
        is_input_directory = False
        is_output_directory = False
        is_debug_mode = False
        #handling the flags to set/overwrite default values
        if argv is not None:
            i = 1
            while i < len(argv):
                if argv[i][0] == "-":
                    flag = argv[i].lstrip("-")
                    if flag == "d":
                        is_debug_mode = True
                    # add new flags here 
                    else:
                        print("Invalid flag ",flag)
                        exit(0)
                else:
                    if is_input_directory == False:
                        is_input_directory = True
                        ip_directory_name = argv[i]
                    elif is_output_directory == False:
                        is_output_directory = True
                        op_directory_name = argv[i]
                    else:
                        print("Error in this argument",argv[i])
                        exit(0)
                i = i + 1

        flags, args = commonArgs().getCommonFlagsAndArgs()

        flags["is_input_directory"] = is_input_directory
        flags["is_output_directory"] = is_output_directory
        flags["is_debug_mode"] = is_debug_mode

        args["ip_directory_name"] = ip_directory_name
        args["op_directory_name"] = op_directory_name
        args["current_dir"] = current_dir
        args["pipelineCode"] = pipelineCode
        args["encodeMode"] = encodeMode
        args["encryptMode"] = encryptMode
        args["primaryHeaderMode"] = primaryHeaderMode
        args["fileHeaderMode"] = fileHeaderMode

        #overwrite the values if there
        if rec_flags is not None:
            rec_flag_keys = rec_flags.keys()
            for key in rec_flag_keys:
                if key in flags.keys():
                    # maybe put a check before blind assignment 
                    flags[key] = rec_flags[key]
                else:
                    print("Illegal flags key ",key)
        
        if rec_args is not None:
            rec_arg_keys = rec_args.keys()
            for key in rec_arg_keys:
                if key in args.keys():
                    # maybe put a check before blind assignment 
                    args[key] = rec_args[key]
                else:
                    print("Illegal arg key ",key)

        return flags, args

    
        
class commonArgs:
    def getCommonFlagsAndArgs(self):
        #those common for both start with an underscore
        _commonname = "bpsnecjkx"
        _delimeter = "_"
        _opformat = "gty"
        _endian = 'little'
        _default_password = "pmqhfisbrkjcvklzxckliou"
        _filecount_size = 8
        _cs_size = 8
        _dec_key_size = 4
        _pass_size = 20
        _encode_mode_size = 1
        _filepath_size = 256
        _date_time = 32
        _encode_mode_size = 1
        _encrypt_mode_size = 1
        _primary_header_mode_size = 1
        _file_header_mode_size = 1
        _pipeline_code_size = 1

        flags = {}
        args = {}
        args["_commonname"] = _commonname
        args["_delimeter"] = _delimeter
        args["_opformat"] = _opformat
        args["_endian"] = _endian
        args["_default_password"] = _default_password
        args["_filecount_size"] = _filecount_size
        args["_cs_size"] = _cs_size
        args["_dec_key_size"] = _dec_key_size
        args["_pass_size"] = _pass_size
        args["_encode_mode_size"] = _encode_mode_size
        args["_filepath_size"] = _filepath_size
        args["_date_time"] = _date_time
        args["_encode_mode_size"] = _encode_mode_size
        args["_encrypt_mode_size"] = _encrypt_mode_size
        args["_primary_header_mode_size"] = _primary_header_mode_size
        args["_file_header_mode_size"] = _file_header_mode_size
        args["_pipeline_code_size"] = _pipeline_code_size
        return flags, args