import requests

class GetClip:
	
	"""

		These links can be found when hovering over a video thumbnail on a hashtag page. These links can be grabbed through
		selenium by iterating through elements and then grabbing the url that appears after hovering over them. Other methods
		have a possibility of working as well.

	"""
    url = "https://v19.muscdn.com/0dfa950e45846a3145c8c92af6b2a8a5/5e420c56/video/tos/maliva/tos-maliva-v-0068/e58c12ab959e400d93338800aace5a4f/?a=1233&br=1686&bt=843&cr=0&cs=0&dr=0&ds=3&er=&l=202002102007040101102422090303AAFD&lr=tiktok_m&qs=0&rc=MzduOTw0eTRscTMzaDczM0ApOzY7ZzQ0Ozs2NzU6O2VkNWdxYzI0NnIvaDZfLS0zMTZzczAvLmNhXi5gL2E0MjE2NGE6Yw%3D%3D"
    # url = "https://v19.muscdn.com/e1e064bb6329b2ee6422007ff5ca0583/5e420c5b/video/tos/maliva/tos-maliva-v-0068/9a99776396964a92a5d0f35c456ad4ba/?a=1233&br=3284&bt=1642&cr=0&cs=0&dr=0&ds=3&er=&l=202002102007040101102422090303AAFD&lr=tiktok_m&qs=0&rc=M3ZvcjxuZztmcTMzNDczM0ApZGVmN2k5N2Q1N2g3aWdmM2doNm9pczZyamVfLS0tMTZzczZeNmExYTJfNV40Yi1hLy06Yw%3D%3D"

    # REST API GET request, stored as a response	
    response = requests.request("GET", url)

    # Write contents of GET request, and store it as a .mp4 file
    f = open('testvid.mp4', 'wb')
    for chunk in response.iter_content(chunk_size = 255):
        if chunk:
            f.write(chunk)
    f.close()