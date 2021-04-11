from PIL import Image
import requests
import io
from urllib.request import urlopen

BASE = "http://127.0.0.1:5000/"

#  image_formats = ("image/png", "image/jpeg", "image/gif")
#  url = "https://baidu.com"
#  site = urlopen(url)
#  meta = site.info()  # get header of the http request
#  if meta["content-type"] in image_formats:  # check if the content-type is a image
#      print("it is an image")

#  response = requests.get(url)
#  image_bytes = io.BytesIO(response.content)
#  img = Image.open(image_bytes)
#  img.show()

response = requests.post(
    BASE + "inference", {"network": "resnet-18", "url": "https://i.guim.co.uk/img/media/bd3bd1958ba8528446be026a806892f217204f04/0_173_5184_3110/master/5184.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=a251698ed3806300769ed9bcfec854c0"})

print(response.json())
