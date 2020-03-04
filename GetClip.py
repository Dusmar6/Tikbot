import requests
import os

def GetClip(title, urls):
    
    for num in range(len(urls)):
        
        # REST API GET request, stored as a response	
        response = requests.request("GET", urls[num])
        os.mkdir("/" + title)
        # Write contents of GET request, and store it as a .mp4 file
        f = open(title + '/' + 'tok'+str(num)+'.mp4', 'wb')
        
        for chunk in response.iter_content(chunk_size = 255):
            if chunk:
                f.write(chunk)
        f.close()



	
"""

		These links can be found when hovering over a video thumbnail on a hashtag page. These links can be grabbed through
		selenium by iterating through elements and then grabbing the url that appears after hovering over them. Other methods
		have a possibility of working as well.

"""