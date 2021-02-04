import os
import exifread
import glob
import numpy as np
from PIL import Image
import cv2

l=glob.glob("/home/roland/2tb/iii/**/*.jpg",recursive=True)
zufall=np.random.randint(len(l))


#a=os.popen('curl  "https://nominatim.openstreetmap.org/reverse?format=json&lat=43.205291666666678&lon=2.3628583333333335"').read()
#lat_r= exifdata[14].split()
#lat=int(lat_r[3].split(',')[0].split('[')[-1])+float(lat_r[4].split(',')[0])/60+float(lat_r[5].split('/')[0])/3600/10000



def read_exif(file_name):
	
	f = open(file_name, 'rb')

	tags = exifread.process_file(f)

	exifdata=[]
	for tag in tags.keys():
		if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
			print ("Key: %s, value %s" % (tag, tags[tag]))
			exifdata.append("%s, value %s" % (tag, tags[tag]))
	return exifdata

def conv(tag):
	lat_r= tag.split()

	lat=int(lat_r[3].split(',')[0].split('[')[-1])+float(lat_r[4].split(',')[0])/60+float(lat_r[5].split('/')[0])/3600/10000
	return lat

def ori(tag):
	factor=1
	lat_r= tag.split()
	we=lat_r[3].split()[-1]
	print(we)
	if we=='W' or we=='S':
		factor=-1
	print(factor)	
		
	return factor

def ort(lat,latori,lon,lonori):
	we1,we2=ori(latori),ori(lonori)
	a=os.popen('curl  "https://nominatim.openstreetmap.org/reverse?format=json&lat=%s&lon=%s"' % (str(lat*we1),str(lon*we2))).read()
	#print('curl  "https://nominatim.openstreetmap.org/reverse?format=json&lat=%s&lon=%s"' % (str(lat*we1),str(lon*we2)))
	return(a)


a=read_exif(l[zufall])

o=ort(conv(a[14]),a[13],conv(a[16]),a[15])

#print(o.split(',')[22])
print(o)

#im = Image.open(l[zufall])
#im.show()
img = cv2.imread(l[zufall])
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
