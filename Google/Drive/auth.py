import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import sys
import logging
import pickle

class Auth:
    # Copy your credentials from the console
    client_secrets = ""
    
    # Check https://developers.google.com/drive/scopes for all available scopes
    oauth_scopes = ''
    
    # Redirect URI for installed apps
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    #path 
    path = ""
    
    #initial flow object
    flow = ''
    
    def __init__(self):            
        #current file location
        encoding = sys.getfilesystemencoding()
        self.path = os.path.dirname(unicode(__file__, encoding))
        
        # define credentials
        self.client_secrets = self.path+"/profile/client_secret.json"
        
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
        authorization_code = self.get_authcode()
        if authorization_code is None:
            print 'Go to the following link in your browser: ' + authorize_url
            authorization_code = raw_input('Enter verification code: ').strip()    
            self.store_authcode(authorization_code)    
        return authorization_code
        
    
    def authorize(self, authorization_code):
        try:
            credentials = self.get_stored_credentials()
            if credentials is None:
                credentials = self.flow.step2_exchange(authorization_code)
            return credentials
        except FlowExchangeError, error:
            logging.error('An error occurred: %s', error)
        
    def get_user_info(self, credentials):
        """Send a request to the UserInfo API to retrieve the user's information.

        Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                     request.
        Returns:
        User information as a dict.
        """
        user_info_service = build(
          serviceName='oauth2', version='v2',
          http = credentials.authorize(httplib2.Http())
      )
        user_info = None
        try:
            user_info = user_info_service.userinfo().get().execute()
        except errors.HttpError, e:
            logging.error('An error occurred: %s', e)
        if user_info and user_info.get('id'):
            return user_info
        else:
            logging.error('No user')
            
    def store_authcode(self, code):
        file = open(self.path+"/profile/authcode.ser", "wb")
        file.write(code)
        file.close()
        
    def get_authcode(self):
        try:
            file = open(self.path+"/profile/authcode.ser", "rb")
            data = file.readline()
            return data
        except:
            return None
    
    def store_credentials(self, user_id, credentials):    
        try:
            #open the file to store the serialed data
            file = open(self.path+"/profile/acessdrive.ser", "wb")
            #serialize the credentials and the user id
            data = {"user_id":user_id, "credentials":credentials}
            pickle.dump(data, file)
            file.close()
        except pickle.PicklingError, err:
            logging.error("credential object cannot be dumped, %s", e)
    
    def get_stored_credentials(self):
        try:
            #open the file to store the serialed data
            file = open(self.path+"/profile/acessdrive.ser", "rb")
            #get serialized data
            data = pickle.load(file)
            return data["credentials"]
        except:
            return None 
            
            
    def get_authorization_url(self, email_address):
        """Retrieve the authorization URL.

        Args:
        email_address: User's e-mail address.
        state: State for the authorization URL.
        Returns:
        Authorization URL to redirect the user to.
        """
        flow = self.flow
        flow.params['access_type'] = 'offline'
        flow.params['approval_prompt'] = 'force'
        flow.params['user_id'] = email_address
        #flow.params['state'] = state
        return flow.step1_get_authorize_url()
    
    
    def get_credentials(self, authorization_code):    
        email = ""
        try:
            credentials = self.authorize(authorization_code)
            print credentials
            #get user information
            user_info = self.get_user_info(credentials)
            email = user_info.get('email')
            user_id = user_info.get('id')        
            print email       
            
            if credentials.refresh_token is not None:
                self.store_credentials(user_id, credentials)
                return credentials
            else:
                credentials = self.get_stored_credentials()
                if credentials and credentials.refresh_token is not None:
                    return credentials
        except:
            logging.error('An error occurred during code exchange.')
            # Drive apps should try to retrieve the user and credentials for the current
            # session.
            # If none is available, redirect the user to the authorization URL.
            authorization_url = self.get_authorization_url(email)
            credentials = self.get_stored_credentials()
            return credentials
    
    def startService(self):
        authorization_code = self.get_authorization()
        credentials = self.get_credentials(authorization_code)
                
        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build('drive', 'v2', http=http)
        
        

