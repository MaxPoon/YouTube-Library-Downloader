import time
import requests
import concurrent.futures
from queue import Queue
import math
from pytube import YouTube
from bs4 import BeautifulSoup
from os import listdir
import multiprocessing
cpus = multiprocessing.cpu_count()

def download(url, resolution, path, addOrder, numOfVideos, video_urls, completed):
	try:
		n = url[1]
		url = url[0]
		downloaded = listdir(path)
		resolutions = ['720p', '480p', '360p', '240p', '144p']
		yt = YouTube(url)
		if (yt.filename + '.mp4') in downloaded: return False
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
			if (prefix + yt.filename + '.mp4') in downloaded: return False
			yt.set_filename(prefix + yt.filename)
		video = yt.get('mp4', resolution)
		print("downloading ", yt.filename, resolution)
		video.download(path)
		completed.put(1)
	except:
		print("downloading ", yt.filename, "failed")
		print("retry later")
		video_urls.put((url, n))

#get user input
resolutions = ['720p', '480p', '360p', '240p', '144p']
url = input("YouTube Library URL: ")
resolution = input("Resolution (144, 240, 360, 480, 720): ")
resolution = '480p' if resolution+'p' not in resolutions else resolution+'p'
maxThreads = input("Maximum number of simultaneous downloads: ")
maxThreads = int(maxThreads) if maxThreads.isdigit() else cpus
path = input('Path: ')
addOrder = input("Add order number to the file name (Y/N): ")
addOrder = True if addOrder=='Y' or addOrder=='y' else False
if not maxThreads: maxThreads = 5
if not path: path = './'

#parse the library page and get video urls
html =  requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all('a')
video_urls = Queue()
url_set = set()
count = 1
for tag in tags:
	video_url = tag.get('href', None)
	if video_url and video_url.find('/watch?')==0 and video_url.find('&index=')>0: 
		index = video_url.find('&list=')
		video_url = video_url[:index]
		video_url = 'https://www.youtube.com'+video_url
		if video_url not in url_set:
			video_urls.put((video_url, count))
			url_set.add(video_url)
			count += 1

numOfVideos = video_urls.qsize()
completed = Queue()
pool = concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads)
print("Started downloading ", numOfVideos, " videos")
start_time = time.time()
while completed.qsize()<numOfVideos:
	if video_urls.qsize()>0:
		newURL = video_urls.get()
		pool.submit(download, newURL, resolution, path, addOrder, numOfVideos, video_urls, completed)
print("Download time: ", time.time()-start_time, "seconds")