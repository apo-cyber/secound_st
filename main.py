from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

with open("secret.json") as f:
    secret=json.load(f)

KEY=secret["KEY"]
ENDPOINT=secret["ENDPOINT"]

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    tag_name=[]
    if (len(tags_result_local.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result_local.tags:
            tag_name.append(tag.name)
    return(tag_name)

def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects=detect_objects_results.objects
    return objects

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.markdown('** apo_cyber present **')
st.title('Object Detection App ')

upload_file=st.file_uploader('choose an image...', type=['jpg', 'png'])
if upload_file is not None:
    img=Image.open(upload_file)
    img_path=f'image/{upload_file.name}'
    img.save(img_path)
    objects=detect_objects(img_path)

    draw=ImageDraw.Draw(img)
    for object in objects:
        x=object.rectangle.x
        y=object.rectangle.y
        w=object.rectangle.w
        h=object.rectangle.h
        caption=object.object_property

        font= ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
        text_w, text_h=draw.textsize(caption, font=font)
        
        draw.rectangle([(x,y),(x+w, y+h)], fill=None, outline='green', width=5)
        draw.rectangle([(x,y),(x+text_w, y+text_h)], fill='green')
        draw.text((x,y), caption, fill='white',font=font)  
    
    st.image(img)

    tags_name=get_tags(img_path)
    tags_name=', '.join(tags_name)

    st.markdown('**Recognited content tags**')
    st.markdown(f'>{tags_name}')


# Git init
# Git remote add origin URL
# Git add .
# Git commit -m '1st.version'
# git push origin master
