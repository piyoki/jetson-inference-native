from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import uuid
import re
from urllib.request import urlopen

app = Flask(__name__)
api = Api(app)


# args parser
inference_args = reqparse.RequestParser()
inference_args.add_argument(
    "url", type=str, help="please put a valid image url", required=True)

# initilize result dictionary
result = {}


# check if the url is invalid
def abort_if_url_invalid(url):

    # check url images
    image_formats = ("image/png", "image/jpeg", "image/gif")
    meta = urlopen(url).info()  # get header of the http request
    if not meta["content-type"] in image_formats:  # check if the content-type is a image
        abort(403, msg="image url is invalid, please try again!")

    # check local images
    #  regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif))$)"
    #  p = re.compile(regex)
    #  if not (re.search(p, url)):
    #      abort(409, msg="image url is invalid, please try again!")


class Inference(Resource):

    # POST
    def post(self):
        # initialize params
        id = uuid.uuid4()
        args = inference_args.parse_args()
        abort_if_url_invalid(args['url'])

        result[id] = args

        # put computing logic here

        return result[id], 200


api.add_resource(Inference, "/inference")

if __name__ == "__main__":
    app.run(debug=True)
