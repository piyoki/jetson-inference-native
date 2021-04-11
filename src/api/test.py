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

response = requests.post(BASE + "inference", {"url": "https://baidu.com"})

print(response.json())
