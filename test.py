from Google.Drive.media_query import Uploader

a = {'title':'ok.txt', 'description':'try1', 'mimeType':'text/plain'}
b = {'title':'k.txt', 'description':'try2', 'mimeType':'text/plain'}
ls = [a,b]
u = Uploader();
u.uploadFiles(ls)
