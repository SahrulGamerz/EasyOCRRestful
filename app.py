from flask import Flask, request, abort
from PIL import Image
from waitress import serve
import urllib
import numpy as np
import cv2
import easyocr
import re
import base64
import io
import os

if 'PORT' in os.environ:
    print("Port specified, using given port")
    PORT = os.environ['PORT']
else:
    print("Port not specified, using default port")
    PORT = 2000

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
base64_regex = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")

app = Flask(__name__)

def url_to_image(url):
    """
    download the image, convert it to a NumPy array, and then read it into OpenCV format
    :param url: url to the image
    :return: image in format of Opencv
    """

    if (url_regex.match(url) is not None):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
    elif (base64_regex.search(re.sub('^data:image/.+;base64,', '', url)) is not None):
        base64_decoded = base64.b64decode(re.sub('^data:image/.+;base64,', '', url))
        base64_image = Image.open(io.BytesIO(base64_decoded))
        imgByteArr = io.BytesIO()
        base64_image.save(imgByteArr, format=base64_image.format)
        image = np.asarray(bytearray(imgByteArr.getvalue()), dtype="uint8")
    else:
        print("Non url/base64")
        return
    
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def data_process(data):
    """
    read params from the received data
    :param data: in json format
    :return: params for image processing
    """
    image = data["image"]
    lang = data["lang"]

    return url_to_image(image), lang

def recognition(image, lang):
    """
    :param image:
    :return:
    """
    results = []
    reader = easyocr.Reader([lang], gpu=False)
    texts = reader.readtext(image)
    for (bbox, text, prob) in texts:
        output = {
            "coordinate": [list(map(float, coordinate)) for coordinate in bbox],
            "text": text,
            "score": prob
        }
        results.append(output)

    return results

@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    """
    received request from client and process the image
    :return: dict of width and points
    """
    data = request.get_json(force=True, silent=False)
    image, lang = data_process(data)
    
    if(image is None):
        return abort(400)

    results = recognition(image, lang)
    return {
        "results": results
    }

@app.route('/health', methods=['GET', 'POST'])
def health():
    return {
        'code': 200,
        'message': 'Server is up'
    }

if __name__ == "__main__":
    print("Serving web on port", PORT)
    serve(app, host='0.0.0.0', port=PORT)
    serve(app, host='::0', port=PORT)
    #app.run(host='0.0.0.0', port=PORT, debug=True)