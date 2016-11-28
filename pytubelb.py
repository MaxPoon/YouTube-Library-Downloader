import requests
import threading
from pytube import YouTube
from bs4 import BeautifulSoup

def download(url, resolution, path):
	try:
		resolutions = ['720p', '480p', '360p', '240p', '144p']
		yt = YouTube(url)
		if len(yt.filter('mp4', resolution=resolution)) == 0:
			resolutions.remove(resolution)
			for r in resolutions:
				if len(yt.filter('mp4', resolution=r)) != 0:
					resolution = r
					break
		video = yt.get('mp4', resolution)
		print("downloading ", yt.filename)
		video.download(path)
	except:
		download(url, resolution, path)

#get user input
resolutions = ['720p', '480p', '360p', '240p', '144p']
url = input("YouTube Library URL: ")
resolution = input("Resolution (144, 240, 360, 480, 720): ")
resolution = '480p' if resolution+'p' not in resolutions else resolution+'p'
maxThreads = input("Maximum number of simultaneous downloads: ")
maxThreads = int(maxThreads) if maxThreads.isdigit() else 5
path = input('Path: ')
if not maxThreads: maxThreads = 5
if not path: path = './'

#parse the library page and get video urls
html =  requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all('a')
video_urls = set()
for tag in tags:
	video_url = tag.get('href', None)
	if video_url and video_url.find('/watch?')==0: 
		index = video_url.find('&list=')
		video_url = video_url[:index]
		video_urls.add('https://www.youtube.com'+video_url)
video_urls = list(video_urls)

while len(video_urls):
	if threading.active_count() >= maxThreads+1: continue
	newURL = video_urls.pop(0)
	newDownload = threading.Thread(target = download, args = (newURL, resolution, path))
	newDownload.start()