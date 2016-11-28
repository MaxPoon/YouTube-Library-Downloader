# YouTube-Library-Downloader
A python tool to download all the videos from a YouTube library.

## Description
You may encounter the situation where you need to download all the videos in a YouTube library. This YouTube library downlowder allows you to do it easily.

## Usage
	python pytubelb
	
## Parameters
URL: The url of the YouTube video library you want to download.

Resolution: The resolution of the video you prefer, 480 by default. In the case that the resolution you choose is not available, it will download the video of the highest available resolution.

Maximum number of simultaneous downloads: 5 by default

path: The path you prefer to save the video. By default it is the current folder.

## Dependencies
* requests
* beautifulsoup4
* pytube