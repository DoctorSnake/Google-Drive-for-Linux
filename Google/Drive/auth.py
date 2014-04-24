import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import sys
import logging

class Auth:
    # Copy your credentials from the console
    client_secrets = ""
    
    # Check https://developers.google.com/drive/scopes for all available scopes
    oauth_scopes = ''
    
    # Redirect URI for installed apps
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    def __init__(self):    
        # define credentials
        encoding = sys.getfilesystemencoding()
        self.client_secrets = os.path.dirname(unicode(__file__, encoding))+"/profile/client_secret.json"
        
        #add scopes to oauth
        self.oauth_scopes = [
                    'https://www.googleapis.com/auth/drive',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/drive.install'
                    ]
        
        # Run through the OAuth flow and retrieve credentials
        self.flow = flow_from_clientsecrets(self.client_secrets, ' '.join(self.oauth_scopes))
        self.flow.redirect_uri = Auth.redirect_uri
    
    def get_authorization(self):    
        authorize_url = self.flow.step1_get_authorize_url()        
        print 'Go to the following link in your browser: ' + authorize_url        
        authorization_code = raw_input('Enter verification code: ').strip()
        return authorization_code
        
    
    def authorize(self, authorization_code):
        try:
            credentials = self.flow.step2_exchange(authorization_code)
            return credentials
        except FlowExchangeError, error:
            logging.error('An error occurred: %s', error)
        
    def get_user_info(credentials):
        """Send a request to the UserInfo API to retrieve the user's information.

        Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                     request.
        Returns:
        User information as a dict.
        """
        user_info_service = build(
          serviceName='oauth2', version='v2',
          http=credentials.authorize(httplib2.Http()))
        user_info = None
        try:
            user_info = user_info_service.userinfo().get().execute()
        except errors.HttpError, e:
            logging.error('An error occurred: %s', e)
        if user_info and user_info.get('id'):
            return user_info
        else:
            logging.error('No user')
    
        
        
    def startService(self):
        authorization_code = self.get_authorization()
        credentials = self.authorize(authorization_code)
        #user_info = get_user_info(credentials)
        # Create an httplib2.Http object and authorize it with our credentials
        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)
        return build('drive', 'v2', http=self.http)
        
        

