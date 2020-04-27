import requests
import os.path

def GetClip(path, urls):
    
    for num in range(len(urls)):
        
        filepath = os.path.join(path, 'tok'+str(num)+'.mp4')
        # REST API GET request, stored as a response	
        response = requests.request("GET", urls[num])
        # Write contents of GET request, and store it as a .mp4 file
        f = open(filepath, 'wb')
        
        for chunk in response.iter_content(chunk_size = 255):
            if chunk:
                f.write(chunk)
        f.close()
        
        
        
        
        
    
