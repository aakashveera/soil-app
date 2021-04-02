from flask import Flask, request
import json
import base64
import werkzeug

import os
import cv2
import random
import numpy as np
import torch
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet

def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    
seed_everything(42)

use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")

model = torch.load("model.pth",map_location='cpu')
model.to(device)
model.eval()

transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(224),       
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

labels = ['Alluvial_Soil','Black_Soil','Clay_Soil','Red_Soil']

app = Flask(__name__)
app.secret_key = "abc" 

@app.route('/', methods = ['GET'])
def home():
    if request.method == 'GET':
        data = "hello world"
        return data

@app.route('/soil_predict', methods = ['POST'])
def file_upload():
	if request.method== 'POST':
		files_get=request.files['image']
		filename = werkzeug.utils.secure_filename(files_get.filename)
		files_get.save(filename)

		img = transform(cv2.imread(filename)).unsqueeze_(0).to(device)

		with torch.no_grad():
			label = model(img).data.numpy().argmax()

		print(label)

		os.remove(filename)

		response_string = {"soil": labels[label]}
		return json.dumps(response_string, indent=4)

app.run(host ='0.0.0.0',debug=True)