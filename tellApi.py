from urllib import request as rq
from io import BytesIO
import os, sys, warnings
from views import database,ini_ip
import json
from PIL import Image
from werkzeug.utils import secure_filename
from imageai.Prediction.Custom import CustomImagePrediction

if not sys.warnoptions:
    warnings.simplefilter("ignore")
from flask import Flask, request, send_file, render_template


execution_path = os.getcwd()

UPLOAD_FOLDER = 'UPLOAD_FOLDER'

def detect():
    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("model200.h5")
    prediction.setJsonPath("class1.json")
    prediction.loadModel(num_objects=12)
    predictions, probabilities = prediction.predictImage("UPLOAD_FOLDER/photo.jpg", result_count=1)

    for eachPrediction, eachProbability in zip(predictions, probabilities):
        item = eachPrediction

    return item




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/",methods=['GET'])
def home():
	global IPaddress
	if request.method == 'GET':
		return render_template('base.html',title='Home',ip=IPaddress)

@app.route("/ip",methods=['POST'])
def ip_1():
	if request.method == 'POST':
		ip = request.data
		ip = ip.decode("utf-8")
		global IPaddress
		IPaddress= ip
		ip = ini_ip(ip)
		print("ip is :",ip)
		data = {'ip': ip}
		data = json.dumps(data)
		return data


@app.route('/detect', methods = ['GET', 'POST'])
def upload_file():
	global IPaddress
	IP = IPaddress
	formats = {
		'image/jpeg': 'JPEG',
		'image/png': 'PNG',
		'image/gif': 'GIF',
		'image/jpg': 'JPG'
	}
	URL = "http://" +IP+"/photo.jpg"
	response = rq.urlopen(URL)
	image_type = response.info().get('Content-Type')
	try:
		format = formats[image_type]
	except KeyError:
		raise ValueError('Not a supported image format')

	file = BytesIO(response.read())
	img = Image.open(file)

	# ...

	filename = secure_filename(URL.rpartition('/')[-1])
	img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), format=format)
	short_code = detect()
	response = database(short_code)
	return response


if __name__ == '__main__':
	IPaddress = ""
	app.run(debug=True)
