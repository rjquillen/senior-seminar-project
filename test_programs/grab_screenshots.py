#
# Author: R.J. Quillen
#
import urllib.request
import time


# This URL may change. It's recieved by right clicking the stream from the 
# web applet and copying the link. 
url = "http://136.227.192.80/cam_pic.php?time=1487356190726&pDelay=40000"
pictures_to_grab = 30

# I've started logging the time it takes to get x amount of images. So 
# far it's been around 15 images per second. I'm working on optimizing this part.
start = time.time() 
for i in range(0, picture_to_grab):
    urllib.request.urlretrieve(url, str(i)+"_test.jpg") # saves the images as the form number_test.jpg
end = time.time()
print("It took " + str((end-start)) + "seconds to retrieve " + picture_to_grab +  " pictures.")
