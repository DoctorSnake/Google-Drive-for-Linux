from Google.Drive.auth import Auth
import pprint
from apiclient.http import MediaFileUpload
from apiclient.errors import HttpError

class Uploader:
    def __init__(self):        
        self.service = Auth()
        self.drive_service = self.service.startService()

    def uploadFile(self, file): 
        # Insert a file
        media_body = MediaFileUpload(file["title"], mimetype=file["mimeType"], resumable=True)
        request = self.drive_service.files().insert(body=file, media_body=media_body).execute()
        pprint.pprint(request)
        """
        response = None
        progress = 0
        while response is None:               
            try:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print "Uploaded %d%%." % progress
                print "%s Upload Complete" % file["title"]
            except HttpError, e:
                if e.resp.status in [404]:
                    # Start the upload all over again.
                    return 404
                elif e.resp.status in [500, 502, 503, 504]:
                    # Call next_chunk() again, but use an exponential backoff for repeated errors.
                    request.next_chunk()
                else:
                    # Do not retry. Log the error and fail.
                    return 400
        """
        return 200
            
                
    def uploadFiles(self, files):
        while files is not []:
            file = files.pop()
            status = self.uploadFile(file)
            if status in [200, 400]:
                pass
            elif status is 404:
               files.append(file)
            
            
        
                
        
            
            
