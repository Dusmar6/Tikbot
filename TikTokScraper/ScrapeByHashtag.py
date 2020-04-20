import time
import requests
import subprocess
import threading

def node_server():
    print('server starting')
    p = subprocess.run('node server.js', capture_output=True, text=True, shell=True)
    print('server stopped')
    print(p.returncode)
    if p.returncode == 0:
        print(p.stdout)
    else:
        print(p.stderr)


def get_signature(args):
    hashtag = args.split('tag/')[1].replace('?lang=en"', '')
    print(args.split('tag/')[1].replace('?lang=en"', ''))
    p = subprocess.run(args, capture_output=True, text=True, shell=True)
    print('p working')
    print(p.returncode)
    if p.returncode == 0:
        signature = p.stdout.replace('\n', '')
        referer = "https://www.tiktok.com/tag/" + hashtag + "?lang=en"

        session = requests.session()

        session.headers = {
            "authority": "m.tiktok.com",
            "method": "GET",
            "scheme": "https",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://www.tiktok.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": referer,
            "user-agent": "Naverbot",
            'path': "node/share/discover?noUser=1&userCount=30&verifyFp=&_signature=%s" % signature
        }

        ### UPDATE PATH HEADER
        ### MAKE GET REQUEST
        ### UPDATE SIGNATURE
        response = session.get('https://m.tiktok.com/node/share/discover?noUser=1&userCount=30&verifyFp=&_signature=' + signature)
        print(response.json())

        p = subprocess.run('node browser.js "https://m.tiktok.com/node/share/discover?noUser=1&userCount=30&verifyFp=&_signature=%s"' % signature, capture_output=True, text=True, shell=True)
        signature = p.stdout.replace('\n', '')
        # print(signature)

        ### UPDATE PATH HEADER
        ### MAKE GET REQUEST
        ### UPDATE SIGNATURE
        session.headers['path'] = "/api/challenge/detail/?challengeName=meme&language=en&verifyFp=&_signature=%s" % signature
        response = session.get('https://m.tiktok.com/api/challenge/detail/?challengeName=' + hashtag + '&language=en&verifyFp=&_signature=' + signature)
        # print('id:', response.json()['challengeInfo']['challenge']['id'])
        # Grabs ID for next GET request
        id = response.json()['challengeInfo']['challenge']['id']
        print(response.text)
        p = subprocess.run('node browser.js "https://m.tiktok.com/api/challenge/detail/?challengeName=' + hashtag + '&language=en&verifyFp=&_signature=%s"' % signature, capture_output=True, text=True, shell=True)
        signature = p.stdout.replace('\n', '')


        session.cookies.set('_ga', 'GA1.2.1212173610.1579663971', domain='.tiktok.com', path='/')
        session.cookies.set('_gat_gtag_UA_144727112_1', '1', domain='.tiktok.com', path='/')
        session.cookies.set('_gid', 'GA1.2.1867164184.1586475006', domain='.tiktok.com', path='/')
        session.cookies.set('odin_tt', 'b6c6373cda2488cae916a12bedab02986a0ebcf2a37eac31d874d43ffbf8aa00f7163ee8f2cd17140246e3404c8e35c01e7c4279a625b44e9653171cfba56815', domain='.tiktok.com', path='/')

        session.headers['path'] = "/share/item/list?secUid=&id=23864&type=3&count=30&minCursor=0&maxCursor=0&shareUid=&lang=en&verifyFp=&_signature=%s" % signature
        response = session.get('https://m.tiktok.com/share/item/list?secUid=&id=' + id + '&type=3&count=30&minCursor=0&maxCursor=0&shareUid=&lang=en&verifyFp=&_signature=' + signature)
        # print(response.json()['body']['itemListData'][0]['itemInfos']['video']['urls'][0])

        # TODO: Allow for the option of more than 30 videos to be downloaded at once *implement scrolling*
        # TODO: Allow for the user to select how many videos they want to download, more or less than 30
        # TODO: https://m.tiktok.com/share/item/list?secUid=&id=23864&type=3&count=30&minCursor=0&maxCursor=30&shareUid=&lang=en&verifyFp=&_signature=FSacsAAgEBZg1xfupJqbFxUmnaAAEu8

        for i in range(len(response.json()['body']['itemListData'])):
            print(response.json()['body']['itemListData'][i]['itemInfos']['video']['urls'][0])

            # Write contents of GET request, and store it as a .mp4 file
            f = open('videos/' + tag + '-' + str(i) + '.mp4', 'wb')
            video_url = requests.request("GET", response.json()['body']['itemListData'][i]['itemInfos']['video']['urls'][0])
            for chunk in video_url.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)
            f.close()
    else:
        print(p.stderr)




tag = 'meme'
t0 = threading.Thread(target=node_server)
t1 = threading.Thread(target=get_signature, args=('node browser.js "https://www.tiktok.com/tag/' + tag + '?lang=en"',))

t0.start()
# Sleep for 5 seconds to give the server time to start up
time.sleep(5)
t1.start()

t0.join()
t1.join()
