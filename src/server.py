from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import uuid
import re
from urllib.request import urlopen
import os
import sys
from inference import run_inference


app = Flask(__name__)
api = Api(app)


# args parser
inference_args = reqparse.RequestParser()
inference_args.add_argument(
    "network", type=str, help="please put a valid image url")
inference_args.add_argument(
    "url", type=str, help="please put a valid image url", required=True)

# initilize result dictionary
result_dict = {}


def abort_if_url_invalid(url):

    # check url images
    image_formats = ("image/png", "image/jpeg", "image/gif")
    meta = urlopen(url).info()  # get header of the http request
    if not meta["content-type"] in image_formats:  # check if the content-type is a image
        abort(403, msg="image url is invalid, please try again!")


class Inference(Resource):

    # POST
    def post(self):
        # initialize params
        id = uuid.uuid4()
        args = inference_args.parse_args()
        abort_if_url_invalid(args['url'])

        result_dict[id] = args

        # perform the inference task
        result = run_inference(args['network'], args['url'])

        return {"result": {
                "id": str(id),
                "network": "{:s}".format(args['network']),
                "recognized_object": "{:s}".format(result['recognized_object']),
                "class_number": "{:d}".format(result['class_number']),
                "confidence": "{:f}%" .format(result['confidence'])
                }}, 200


api.add_resource(Inference, "/inference")

if __name__ == "__main__":
    app.run(debug=True)
