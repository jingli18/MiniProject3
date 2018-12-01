import io
import os
from urllib import request
import tweepy
import json
import PIL
from subprocess import Popen, PIPE
from PIL import Image, ImageDraw, ImageFont
import pymongo
#from google.cloud import vision
#from google.cloud.vision import types

Video_client = pymongo.MongoClient()
try:
    mydb = Video_client["Searchdata"]
    print("Database 'Searchdata' created!")
except:
    print("Database 'Searchdata' already exists.")
try:
    mycol = mydb["Users"]
    print("Collection 'Users' created!")
except:
    print("Collection 'Users' already exists.")

try:   
    keypat = os.getcwd()
    keypath1 = keypat + '/img'
    keypath2 = keypat + '/img2'
    keypath3 = keypat + '/tagimg'
    os.makedirs(keypath1)
    os.makedirs(keypath2)
    os.makedirs(keypath3)
    print("Folders Created Successfully!")
except:
    print("Folders already exists.")

search = {}

#get keys from txt
keypath = os.getcwd()
keypath = keypath + '/keys.txt'
info = open(keypath)
ky = info.readlines()
keyinfo = []
for line in ky:
	keyinfo.append(line.replace('\n', ''))
#write keys to tweepy
consumer_key = keyinfo[0]
consumer_secret = keyinfo[1]
access_key = keyinfo[2]
access_secret = keyinfo[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print (api)

#get img
imgpath = os.getcwd()
imgpath1= imgpath + "/img/" 
imgpath2= imgpath + "/img2/"

urllist=[]
#media_files = set()
keyword=input("Please input keyword: ")
search['keyword'] = str(keyword)
users = []
for tweet in tweepy.Cursor(api.search, q=keyword).items(15):
    print('Tweet by: @'+tweet.user.screen_name)
    users.append(tweet.user.screen_name)
    public_tweets=api.user_timeline(tweet.user.screen_name)
    for status in public_tweets:
        for media in status.entities.get('media',[]):
            urllist.append(media.get("media_url"))
search['Users'] = str(users)
search['ImgURL'] = str(urllist)
for m in range(len(urllist)):
	print(urllist[m])
	jpg_link = urllist[m]  
	request.urlretrieve(jpg_link, imgpath1+'%s.jpg' %m)
	
	imgfile=str(m)+'.jpg'
	downpath = os.path.join(imgpath1,imgfile)
	img= Image.open(downpath)
	img = img.resize((1500,1000), Image.ANTIALIAS)
	savepath = os.path.join(imgpath2,imgfile)
	img.save(savepath)
	print(savepath)

tagpaths = os.getcwd()
tagpath = tagpaths + '/tagimg/'
imgpath = os.getcwd()
imgpath2= imgpath + "/img2/"



#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=tagpaths + '/PNG vision-003b735f10a8.json'
#client = vision.ImageAnnotatorClient()
#for n in range(20):
#	imgfile=str(n)+'.jpg'
#	pathimg=os.path.join(imgpath2,imgfile)
## The name of the image file to annotate
#	file_name = os.path.join(
# 	os.path.dirname(__file__),
#   	pathimg)
#
## Loads the image into memory
#	with io.open(file_name, 'rb') as image_file:
#		content = image_file.read()
#		image = types.Image(content=content)
#
## Performs label detection on the image file
#	response = client.label_detection(image=image)
#	labels = response.label_annotations
#
#	print('Labels:')
#	for label in labels:
#		print(label.description)
#
#
#
#	image = Image.open(pathimg)
#	draw = ImageDraw.Draw(image)
#	ttFont = ImageFont.truetype(tagpaths+'/Important.ttf', size=55)
#	fillcolor = "#3498DB"
#	width, height= image.size
#	i = 0
#	for label in labels:
#		draw.text((width-1490, height-990+i), label.description, fill=fillcolor, font=ttFont)
#		
#		i=i+60
#	savepath = os.path.join(tagpath,imgfile)
#	image.save(savepath)
#		
#	n=n+1
#search['Labels'] = str(labels)
#
#os.chdir(tagpath)
#p = os.popen('ffmpeg -r 1 -i %d.jpg -vcodec libx264 -y -an video.mp4')
##os.popen('ffmpeg -r 1 -i %d.jpg -vcodec libx264 -y -an video.mp4')
#print ("Done")
## print(p.read())

mycol.insert_one(search)
for x in mycol.find():
    print(x)