from TikTokApi import TikTokApi
import os
import youtube_dl
from internetarchive import upload
from internetarchive import get_item
import argparse

def downloadTikTok(username, tiktok, cwd):
    ydl_opts = {
        'writeinfojson': True,
        'writedescription': True,
        'write_all_thumbnails': True,
        'writeannotations': True,
        'allsubtitles': True,
        'ignoreerrors': True,
        'fixup': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        }
    try:
        tiktokID = tiktok['id']
    except:
        tiktokID = tiktok['itemInfos']['id']
    if (os.path.exists(tiktokID) == False):
        os.mkdir(tiktokID)
    os.chdir(tiktokID)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID])
    x = os.listdir()
    for i in x:
        if i.endswith('.unknown_video'):
            base = os.path.splitext(i)[0]
            if (os.path.exists(base + '.mp4')):
                os.remove(base + '.mp4')
            os.rename(i, base + '.mp4')
    os.chdir(cwd)

def downloadUser(username):
    api = TikTokApi()
    count = 9999
    tiktoks = api.byUsername(username, count=count)
    cwd = os.getcwd()
    for tiktok in tiktoks:
        downloadTikTok(username, tiktok, cwd)


def uploadUser(username, deletionStatus):
    dirs = os.listdir()
    for tiktok in dirs:
        uploadTikTok(username, tiktok, deletionStatus)

def uploadTikTok(username, tiktok, deletionStatus):
    if (os.path.isdir(tiktok) and tiktok != 'tmp'):
        item = get_item('tiktok-' + tiktok)
        try:
            item.upload('./' + tiktok + '/', verbose=True, checksum=True, delete=deletionStatus, metadata=dict(collection='opensource_media', subject='tiktok', creator=username, title='TikTok Video by ' + username, originalurl='https://www.tiktok.com/@' + username + '/video/' + tiktok, scanner='TikUp 1.0'), retries=9001, retries_sleep=60)        
        except:
            print('An error occurred, trying again.')
            item.upload('./' + tiktok + '/', verbose=True, checksum=True, delete=deletionStatus, metadata=dict(collection='opensource_media', subject='tiktok', creator=username, title='TikTok Video by ' + username, originalurl='https://www.tiktok.com/@' + username + '/video/' + tiktok, scanner='TikUp 1.0'), retries=9001, retries_sleep=60)
        if (deletionStatus == True):
            os.rmdir(tiktok)
        print ()
        print ('Uploaded to https://archive.org/details/tiktok-' + username + '-' + tiktok)
        print ()

def downloadHashtag(hashtag, deletionStatus):
    api = TikTokApi()
    count = 9999
    tiktoks = api.byHashtag(hashtag, count=count)
    usernames = []
    cwd = os.getcwd()
    for tiktok in tiktoks:
        username = tiktok['authorInfos']['uniqueId']
        downloadTikTok(username, tiktok, cwd)
        usernames.append(username + ':' + tiktok['itemInfos']['id'])
    return usernames


parser = argparse.ArgumentParser(description='An auto downloader and uploader for Instagram profiles.')
parser.add_argument('user')
parser.add_argument('--no-delete', action='store_false', help="don't delete files when done")
parser.add_argument('--hashtag', action='store_true', help="download hashtag instead of username")
args = parser.parse_args()
username = args.user
delete = args.no_delete
if (args.hashtag == True):
    names = downloadHashtag(username, delete)
    print (names)
    for name in names:
        splitName = name.split(':')
        uploadTikTok(splitName[0], splitName[1], delete)
else:
    downloadUser(username)
    uploadUser(username, delete)
