from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pathlib import Path

# flag and default arg manager. and common functions
from flag_and_args import enc_flags_and_args
from flag_and_args import dec_flags_and_args
from universal import commonFunctions

# default pipeline implementations
from implementation_encode import default_encode
from implementation_decode import default_decode

app = Flask(__name__)
api = Api(app)
    
class encode(Resource):
    def get(self):
        return jsonify(status="failure", message="Get request is invalid")

    def post(self):
        params = request.get_json(force=True)
        rec_flags, rec_args, rec_argv = None, None, None
        if "flags" in params.keys():
            rec_flags = params["flags"]
        if "args" in params.keys():
            rec_args = params["args"]   # need to force user to send absolute path or else it won't work
        if "argv" in params.keys():
            rec_argv = params["argv"]
        flags, args = None, None
        if rec_argv is None:
            flags, args = enc_flags_and_args().getFlagsAndArgs(None, rec_flags, rec_args)
        else:
            flags, args = enc_flags_and_args().getFlagsAndArgs(rec_argv)
        if flags is None or args is None:
            print("Some error occured while setting the default args and flags")
        # below code as it is copied from encode.py as the implementation should be same 
        if args["pipelineCode"] == 0: # default mode 
            default_encode().perform_encode(flags, args)
        return jsonify(status="success", message="Encryption successful")


class decode(Resource):
    def get(self):
        return jsonify(status="failure", message="Get request is invalid")
    
    def post(self):
        params = request.get_json(force=True)
        rec_flags, rec_args, rec_argv = None, None, None
        if "flags" in params.keys():
            rec_flags = params["flags"]
        if "args" in params.keys():
            rec_args = params["args"]   # need to force user to send absolute path or else it won't work
        if "argv" in params.keys():
            rec_argv = params["argv"]
        flags, args = None, None
        if rec_argv is None:
            flags, args = dec_flags_and_args().getFlagsAndArgs(None, rec_flags, rec_args)
        else:
            flags, args = dec_flags_and_args().getFlagsAndArgs(rec_argv)
        if flags is None or args is None:
            print("Some error occured while setting the default args and flags")
        # as of now just try default
        default_decode().perform_decode(flags, args)
        return jsonify(status="success", message="Encryption successful")

api.add_resource(encode, '/encode')
api.add_resource(decode, '/decode')

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5001,debug=True)