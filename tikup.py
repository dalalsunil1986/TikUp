from TikTokApi import TikTokApi
import os
import youtube_dl
from internetarchive import upload
from internetarchive import get_item
import argparse

def download(username):
    api = TikTokApi()
    count = 9999
    tiktoks = api.byUsername(username, count=count)
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
    cwd = os.getcwd()
    for tiktok in tiktoks:
        if (os.path.exists(tiktok['id']) == False):
            os.mkdir(tiktok['id'])
        os.chdir(tiktok['id'])
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktok['id']])
        x = os.listdir()
        for i in x:
            if i.endswith('.unknown_video'):
                base = os.path.splitext(i)[0]
                if (os.path.exists(base + '.mp4')):
                    os.remove(base + '.mp4')
                os.rename(i, base + '.mp4')
        os.chdir(cwd)


def upload(username, deletionStatus):
    dirs = os.listdir()
    for tik in dirs:
        if (os.path.isdir(tik) and tik != 'tmp'):
            item = get_item('tiktok-' + username + '-' + tik)
            try:
                item.upload('./' + tik + '/', verbose=True, checksum=True, delete=deletionStatus, metadata=dict(collection='opensource_media', subject='tiktok', creator=username, title='TikTok Video by ' + username, originalurl='https://www.tiktok.com/@' + username + '/video/' + tik, scanner='TikUp 1.0'), retries=9001, retries_sleep=60)
                print ('Uploaded to https://archive.org/details/tiktok-' + username + '-' + tik)
            except:
                print('An error occurred, trying again.')
                item.upload('./' + tik + '/', verbose=True, checksum=True, delete=deletionStatus, metadata=dict(collection='opensource_media', subject='tiktok', creator=username, title='TikTok Video by ' + username, originalurl='https://www.tiktok.com/@' + username + '/video/' + tik, scanner='TikUp 1.0'), retries=9001, retries_sleep=60)
            if (deletionStatus == True):
                os.rmdir(tik)

parser = argparse.ArgumentParser(description='An auto downloader and uploader for Instagram profiles.')
parser.add_argument('user')
parser.add_argument('--no-delete', action='store_false', help="delete files when done")
args = parser.parse_args()
username = args.user
delete = args.no_delete
download(username)
upload(username, delete)
