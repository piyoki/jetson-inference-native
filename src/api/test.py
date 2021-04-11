import requests
from urllib.request import urlopen

BASE = "http://127.0.0.1:5000/"

#  image_formats = ("image/png", "image/jpeg", "image/gif")
#  url = "https://baidu.com"
#  site = urlopen(url)
#  meta = site.info()  # get header of the http request
#  if meta["content-type"] in image_formats:  # check if the content-type is a image
#      print("it is an image")

response = requests.post(BASE + "inference", {"url": "https://baidu.com"})

print(response.json())
