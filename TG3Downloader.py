###
### Olympus TG3 Photo Download Over WiFi
###		To download photos from Olympus TG3 over WiFi
###	
### Rev 1.1 R.Y.Liang, 2015/9/11
###		Add progress indication during file transferring
###
### Rev 1.0 R.Y.Liang, 2014/8/15
###		Initial Version
###

###
### Constant definition, user defined
###
# define your local storage path here
LOCAL_STORAGE_PATH = 'D:\My Documents\My Pictures'

###
### Constant definition, system constant
###
INITIAL_URL = r'http://192.168.0.10'

###
### Modules definition
###
import urllib.request
import os
from datetime import datetime
import socket
import sys

socket.setdefaulttimeout(600)

def textDownloadProgress(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("%2d%%" % percent)
    sys.stdout.write("\b\b\b")
    sys.stdout.flush()

def retrievePictureInformationFromURL(url):
	index_obj = urllib.request.urlopen(url)
	index_text = index_obj.read().decode("utf-8")
	index_lines = index_text.split('\n')
	result = []
	for rawtext in index_lines:
		if (rawtext[0:7] == 'wlansd['):
			rawcontenttext = rawtext.split('=')
			contenttext = rawcontenttext[1].replace('"','')
			contenttext = contenttext.replace(';','')
			contenttext = contenttext.replace('\r','')
			contentinformation = contenttext.split(',')
			result.append(contentinformation)
	return result
	
def downloadToLocal(pathlist):
	for item in pathlist:
		sys.stdout.write (item[0] + ' >>> ')
		urllib.request.urlretrieve (item[0], item[1], reporthook=textDownloadProgress)
		print ('')

print (r'**********************************')
print (r'Olympus TG3 Download Over WiFi 1.1')
print (r'     Author : R.Y.Liang, 2015/9/11')
print (r'**********************************')
print (r'Olympus TG3 Web Address : ' + INITIAL_URL)
print (r'Local Storage Path      : ' + LOCAL_STORAGE_PATH)

root_folder = retrievePictureInformationFromURL(INITIAL_URL)
subfolders = []
for subfolder in root_folder:
	if (int(subfolder[2]) == 0):
		subfolders.append(subfolder[0] + r'/' + subfolder[1])

preparedToDownload = []
totalSizeByte = 0
for subfolder in subfolders:
	picts = retrievePictureInformationFromURL (INITIAL_URL + subfolder)
	for pict in picts:
		remote_fullpath = INITIAL_URL + pict[0] + r'/' + pict[1]
		local_fullpath  = LOCAL_STORAGE_PATH + pict[0] + r'/' + pict[1]
		
		if not(os.path.isfile(local_fullpath)):
			preparedToDownload.append([remote_fullpath, local_fullpath])
			totalSizeByte += int(pict[2])
			
totalSizeMB = totalSizeByte / 1024 / 1024
timeStart = datetime.now()
downloadToLocal(preparedToDownload)
timeEnd = datetime.now()
timeDiff = timeEnd - timeStart
if (totalSizeMB == 0):
	print('The photo has already synced')
else:
    print('Transferd Size : {:.4}'.format(totalSizeMB) + ' MB')
    print('Time Elapsed : ' + str(timeDiff.seconds) + ' seconds')
    print('Transfer Rate : {:.4}'.format(totalSizeMB / int(timeDiff.seconds)) + ' MB/sec')

