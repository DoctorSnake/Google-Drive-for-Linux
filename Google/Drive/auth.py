import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

class Auth:
    # Copy your credentials from the console
    client_id = ""
    client_secret = ""
    
    # Check https://developers.google.com/drive/scopes for all available scopes
    oauth_scope = 'https://www.googleapis.com/auth/drive'
    
    # Redirect URI for installed apps
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    def __init__(self):    
        # define credentials
        self.client_id = "874010315843-7a1vim2u25s7c4sl6erjivup6iup3j3q.apps.googleusercontent.com"
        self.client_secret = "Z8iMm_6NDzmtSyiJ0HEsjyAI"
        
        # Run through the OAuth flow and retrieve credentials
        self.flow = OAuth2WebServerFlow(self.client_id, self.client_secret, Auth.oauth_scope, Auth.redirect_uri)
        
    def authorize(self):
        authorize_url = self.flow.step1_get_authorize_url()        
        print 'Go to the following link in your browser: ' + authorize_url
        
        code = raw_input('Enter verification code: ').strip()
        credentials = self.flow.step2_exchange(code)
        
        # Create an httplib2.Http object and authorize it with our credentials
        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)
        
    def startService(self):
        self.authorize()
        return build('drive', 'v2', http=self.http)
        
        

