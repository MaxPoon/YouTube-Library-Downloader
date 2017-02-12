# YouTube-Library-Downloader
A python(3.x) tool to download all the videos from a YouTube library.

## Description
You may encounter the situation where you need to download all the videos in a YouTube library. This YouTube library downlowder allows you to do it easily.

## Usage
```bash
python pytubelb.py
```
	
## Parameters
URL: The url of the YouTube video library you want to download.

Resolution: The prefered resolution of the video, 480 by default. In the case that the resolution you choose is not available, it will download the video of the highest available resolution.

Maximum number of simultaneous downloads: By default it's the number of CPUs.

path: The path you prefer to save the video. By default it is the current folder.

## Dependencies
* requests
* beautifulsoup4
* pytube
