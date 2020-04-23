import time
import requests
import subprocess
import threading
import os


def node_server():
    print('server starting')
    p = subprocess.run('node server.js', capture_output=True, text=True, shell=True)
    print('server stopped')
    print(p.returncode)
    if p.returncode == 0:
        print(p.stdout)
    else:
        print(p.stderr)


def terminate_server():
    netstat = subprocess.run('netstat -aon | findstr 8080', capture_output=True, text=True, shell=True)
    port = netstat.stdout.split('  TCP    127.0.0.1:8080         0.0.0.0:0              LISTENING       ')[1].split('\n')[0]
    terminate_bat = "powershell.exe Stop-Process -ID %s -Force" % port
    subprocess.Popen(terminate_bat, shell=True)


def download_videos(response, amt, max_cursor):
    for i in range(len(response.json()['body']['itemListData'])):
        print(response.json()['body']['itemListData'][i]['itemInfos']['video']['urls'][0])

        # If the video about to be downloaded is more than the desired amount, do not download
        if i + int(max_cursor) > amt:
            return -1
        # Write contents of GET request, and store it as a .mp4 file
        f = open('videos/' + tag + '-' + str(i + int(max_cursor)) + '.mp4', 'wb')
        try:
            print('videos/' + tag + '-' + str(i + int(max_cursor)) + '.mp4')
            video_url = requests.get(response.json()['body']['itemListData'][i]['itemInfos']['video']['urls'][0],
                                     headers={'User-Agent': 'Googlebot'})
            for chunk in video_url.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)
            f.close()
        except Exception as e:
            print(e)
            f.close()
            # If the download fails, wait 5 seconds and try again
            time.sleep(5)
            try:
                print('videos/' + tag + '-' + str(i + int(max_cursor)) + '.mp4')
                video_url = requests.get(response.json()['body']['itemListData'][i]['itemInfos']['video']['urls'][0],
                                     headers={'User-Agent': 'Googlebot'})
                for chunk in video_url.iter_content(chunk_size=255):
                    if chunk:
                        f.write(chunk)
                f.close()
            except Exception as e:
                print(e)
                f.close()
                # Video failed to download because the host refused the connection, delete the file so that
                # the video splicer does not have to interact with a 0 Byte .mp4 file
                os.remove(os.getcwd() + '/videos/' + tag + '-' + str(i + int(max_cursor)) + '.mp4')


def get_signature(args, amt):
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

        ### GRAB VIDEO URLS
        ### DOWNLOAD VIDEOS
        session.headers['path'] = "/share/item/list?secUid=&id=23864&type=3&count=30&minCursor=0&maxCursor=0&shareUid=&lang=en&verifyFp=&_signature=%s" % signature
        min_cursor = '0'
        max_cursor = '0'
        while(True):
            response = session.get('https://m.tiktok.com/share/item/list?secUid=&id=' + id + '&type=3&count=30&minCursor=' + min_cursor + '&maxCursor=' + max_cursor + '&shareUid=&lang=en&verifyFp=&_signature=' + signature)
            if download_videos(response, amt, max_cursor) == -1:
                terminate_server()
                return 1
            p = subprocess.run('node browser.js "https://m.tiktok.com/share/item/list?secUid=&id=' + id + '&type=3&count=30&minCursor=' + min_cursor + '&maxCursor=' + max_cursor + '&shareUid=&lang=en&verifyFp=&_signature=%s"' % signature, capture_output=True, text=True, shell=True)
            signature = p.stdout.replace('\n', '')
            max_cursor = str(int(max_cursor) + 30)
            min_cursor = str(int(min_cursor) + 30)
    else:
        print(p.stderr)


tag = 'meme'
amt = 61
t0 = threading.Thread(target=node_server)
t1 = threading.Thread(target=get_signature, args=('node browser.js "https://www.tiktok.com/tag/' + tag + '?lang=en"', amt,))

t0.start()
# Sleep for 5 seconds to give the server time to start up
time.sleep(5)
t1.start()

t0.join()
t1.join()
