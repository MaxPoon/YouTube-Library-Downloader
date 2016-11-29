import requests
import threading
import math
from pytube import YouTube
from bs4 import BeautifulSoup
from os import listdir

def download(url, resolution, path, addOrder, n, numOfVideos):
	try:
		downloaded = listdir(path)
		resolutions = ['720p', '480p', '360p', '240p', '144p']
		yt = YouTube(url)
		if yt.filename + '.mp4' in downloaded: return
		if len(yt.filter('mp4', resolution=resolution)) == 0:
			resolutions.remove(resolution)
			for r in resolutions:
				if len(yt.filter('mp4', resolution=r)) != 0:
					resolution = r
					break
		if addOrder:
			length = int(math.log(numOfVideos,10)) + 1
			prefix = str(n)
			prefix = "0"*(length - len(str(n))) + prefix +'. '
			yt.set_filename(prefix + yt.filename)
			if prefix + yt.filename + '.mp4' in downloaded: return
		video = yt.get('mp4', resolution)
		print("downloading ", yt.filename, resolution)
		video.download(path)
	except:
		print("downloading ", yt.filename, "failed")

#get user input
resolutions = ['720p', '480p', '360p', '240p', '144p']
url = input("YouTube Library URL: ")
resolution = input("Resolution (144, 240, 360, 480, 720): ")
resolution = '480p' if resolution+'p' not in resolutions else resolution+'p'
maxThreads = input("Maximum number of simultaneous downloads: ")
maxThreads = int(maxThreads) if maxThreads.isdigit() else 5
path = input('Path: ')
addOrder = input("Add order number to the file name (Y/N): ")
addOrder = True if addOrder=='Y' or addOrder=='y' else False
if not maxThreads: maxThreads = 5
if not path: path = './'

#parse the library page and get video urls
html =  requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all('a')
video_urls = []
for tag in tags:
	video_url = tag.get('href', None)
	if video_url and video_url.find('/watch?')==0 and video_url.find('&index=')>0: 
		index = video_url.find('&list=')
		video_url = video_url[:index]
		video_url = 'https://www.youtube.com'+video_url
		if video_url not in video_urls:
			video_urls.append(video_url)

count = 1
numOfVideos = len(video_urls)
print("Started downloading ", numOfVideos, " videos")
while len(video_urls):
	if threading.active_count() >= maxThreads+1: continue
	newURL = video_urls.pop(0)
	newDownload = threading.Thread(target = download, args = (newURL, resolution, path,addOrder, count, numOfVideos))
	newDownload.start()
	count += 1