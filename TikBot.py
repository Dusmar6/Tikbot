import PySimpleGUI as sg
import title_generator as tg
import videoConcatenate as vc
import threading
import GetClip as gc
import os
import configparser
import webbrowser
import shutil
import icon as icon
from ScrapeByHashtag import *





logo = icon.logo

def main_window():
    sg.theme('Default1')
    
    menu_def = [
                ['About']
                ] 
    
    
    instruction_tab = [  [sg.T('Welcome to Tikbot!', font = ("Helvetica", 25)), sg.Text('\nYour one-stop shop for compilation making.', font = ("Helvetica", 13))],
                        [sg.Text('-'*200, text_color = 'light grey')],
                        [sg.Text('\nGetting started:', font = ("Helvetica", 12))],
                        [sg.Text('    1. Navigate to'),  sg.Text('https://console.developers.google.com/apis/credentials', key = 'credsite', text_color = 'blue', click_submits = True), sg.Text(' and click "Create Credentials" at the top of the screen.', font = ("Helvetica", 10))],
                        [sg.Text('    2. Create an OAuth client ID. Set the Application type as "other" and name it "Tikbot".', font = ("Helvetica", 10))],
                        [sg.Text('    3. Click on the newly created credentials and then click "Download Json". Place this .json file in the "ID" folder inside the program file.', font = ("Helvetica", 10))],
                         [sg.Text('Tikbot should now be authorized to send videos to your channel. ', font = ("Helvetica", 10))],
                         
                         [sg.Text('\nMaking a compilation:', font = ("Helvetica", 12))],
                         [sg.Text('    1. Create a collection of clips by navigating to the "Create A Collection" tab. Either paste links individually or scrape via hashtag.')],
                        [sg.Text('    2. Once you\'ve created a collection, compile your collection into a single video on the following tab')],
                         [sg.Text('    3. If you wish to upload your compilation directly from Tikbot, populate the necessary boxes, select a compilation, and click "Upload Video"!')],
                        ]

    tab_1_1_layout = [  [sg.Text('Enter the hashtag you would like to scrape posts from')],
                        [sg.InputText(key='hashtag', size=(30,1))],
                        [sg.Text('Enter the amount of posts you would like to scrape')],
                        [sg.InputText(key='scrape_amount', size=(30,1))],
                        [sg.Button('Create Collection', key='scrape_collection'), sg.Text(" "*110)]
                        ] 
    
    tab_1_2_layout = [  [sg.Text('Paste the video source for each Tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                         [sg.Multiline(default_text='', size=(100, 10), key = 'urls')],
                         [sg.Button('Create Collection', key = 'individual'), sg.Text(" "*110)]
                         ]
                     
    tab_1_layout = [    [sg.Text('\nName this collection: ')],
                         [sg.InputText( key='collection', size= (60,1))],
                         [sg.Text('')],
                         [sg.TabGroup([[sg.Tab('Scrape By Hashtag', tab_1_1_layout ), sg.Tab('Add Tiktoks Individually', tab_1_2_layout)]])],   
                         [sg.Text(' ')]
                          
                         ]
    
    tab_2_layout = [    [sg.Text('\nSelect a collection to compile: '), sg.Text(' '*33)],
                         [sg.Listbox(get_collection_names(), size=(45, 15), key = 'to_compile' ), sg.Text('\nCompiled Collections:\n' + get_compilation_names_string(), key = 'compile_names')], 
                         [sg.Text('')],
                         [sg.Button('Compile Collection'), sg.Text(" "*110)] 
                         ]
    
    tab_3_layout = [   
                         [sg.Text('')],
                         [sg.T('Video Title:  '), sg.InputText(  key='title', size= (75,1)), sg.Button('Generate Title')],
                         [sg.T('Description: '), sg.Multiline(default_text='', size=(100, 5), key = 'description')],
                         [sg.T('Tags:          '),sg.Multiline(default_text='', size=(100, 2), key = 'tags')],
                         [ sg.Text('Video Privacy Setting: '), sg.InputOptionMenu(('Public', 'Private', 'Unlisted'), key = 'privacy', size = (20, 1)),sg.Text(' '*4+ 'Category ID:'), sg.InputOptionMenu(['23 Comedy'], key = 'cat', size = (20, 1))],
                         [sg.Text('-'*200, text_color = 'light grey')],
                         [sg.Text('')],
                         [sg.Text('Select a Compilation to upload: '), sg.Listbox(get_compilation_names(), key = 'to_up', size = (35, 3)),  sg.Text(" "*10), sg.Button('Upload Video')],
                          [sg.Text(' '*46), sg.Button('View Compilations'), sg.Text(" "*110)],
                         #[sg.Text('')],
                         [ sg.Text(' '*170)]
                         ]
    
    tab_4_layout = [      [sg.Text('')],
                            [sg.Text('Delete Collection: '+ ' '*3), sg.Listbox(get_collection_names(), key = 'del_coll', size = (35, 3)), sg.Button('Delete', key= 'coll_to_delete'), sg.Text(' '*50), sg.Button('Delete All Collections'),],      
                           [sg.Text('-'*200, text_color = 'light grey')],
                           
                           [sg.Text('Delete Compilation: '), sg.Listbox(get_compilation_names(), key = 'del_comp', size = (35, 3)), sg.Button('Delete', key= 'comp_to_delete'), sg.Text(' '*48), sg.Button('Delete All Compilations'),],      
                           [sg.Text('-'*200, text_color = 'light grey')],
                           
                           [sg.Text('Change your working directory: '+ ' '*60)],      
                           [sg.Text('Your Folder', size=(20, 1), auto_size_text=False, justification='middle'), sg.InputText(get_working_directory(), key = 'dir'), sg.FolderBrowse()], 
                           
                           [sg.Text('-'*200, text_color = 'light grey')],
                           
                           [ sg.Button('Save Settings')]
                           
                           ]
                       

    
    
    layout =   [[sg.Menu(menu_def, )],
                 [sg.TabGroup([[sg.Tab('Instructions', instruction_tab )], [sg.Tab('Create A Collection', tab_1_layout )], [sg.Tab('Compile A Collection', tab_2_layout )],  [sg.Tab('Upload a Compilation to Youtube', tab_3_layout )],  [sg.Tab('Settings', tab_4_layout )]])]   
                       
                       ]          

    window = sg.Window('TikBotMaster ', layout, icon=logo)
    while True:     
        
        event, values = window.read(timeout=10000)

        if event is None:
            break

        if event == "scrape_collection":
            collection_path = os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']).replace(" ", ""))
            if not DupeCheck(collection_path):
                notif('Your collection has begun downloading...')
                os.makedirs(collection_path)
                hashtag = values['hashtag'].strip()
                try:
                    amt = int(values['scrape_amount'].strip())
                    s = ScrapeByHashtag()
                    s.run('memeslol', 'meme', 30)
                except ValueError:
                    notif('Amount of posts to scrape must be a number, try again')




        if event == 'credsite':
            webbrowser.open('https://console.developers.google.com/apis/credentials')
            
        if event == "individual":
            collection_path = os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']).replace(" ", ""))
            if not DupeCheck(collection_path):
                
                notif('Your collection has begun downloading...')
                os.makedirs(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
        if event == "scrape":
            collection_path =  os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']))
            if not DupeCheck(collection_path):
                
                notif('Your collection has begun downloading...')
                os.makedirs(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
        if event == "Compile Collection":
            name = values['to_compile'][0]
            collection_path = os.path.join(get_collections_folderpath(), os.path.normpath(name))
            
            if not CompDupeCheck(name) and len(get_collection_clip_paths(collection_path)) > 1:
                
                notif('Your collection has begun compiling. This may take some time depending on the size of the collection.')
                
                thread = threading.Thread(target = vc.concatenate_clips, args = (get_compilations_folderpath(), name, collection_path, get_temp_folder() ))
                thread.start()
                
        if event == "Generate Title":
            window['title'].update(tg.generate_title())
            
        if event == "View Compilations":
            os.startfile(get_compilations_folderpath())
        
        if event == "Save Settings":
            set_working_directory(os.path.normpath(values['dir']))
            if values['save creds'] == 'Yes':
                set_client_id(values['ID'])
                set_client_secret(values['secret'])
            else:
                set_client_id(' ')
                set_client_secret(' ')
            check()
            
        if event == "coll_to_delete":
            
            collection_name = values['del_coll']
            if collection_name != '' and collection_name != ' ' and collection_name != None:
                if sg.PopupYesNo('Are you sure you want to delete this collection?', icon = logo) == 'Yes':
                    try:
                        shutil.rmtree(os.path.join(get_collections_folderpath(), collection_name[0]))
                    except:
                        print('could not delete collection')
                        
            else:
                notif('None selected.')
                        
        if event == "comp_to_delete":
            comp_name = values['del_comp']
            if comp_name != '' and comp_name != None:
                if sg.PopupYesNo('Are you sure you want to delete this compilation?', icon = logo) == 'Yes':
                    try:
                        os.remove(os.path.join(get_compilations_folderpath(), comp_name[0] +'.mp4'))
                    except:
                        
                        print('could not delete compilation')
            else:
                notif('None selected.')
                        
        if event == "Delete All Collections":
            if sg.PopupYesNo('Are you sure you want to delete all collections? This cannot be undone.', icon = logo) == 'Yes':
                try:
                    shutil.rmtree(get_collections_folderpath())
                except:
                    print('could not delete all collections')
            check()
            
        if event == "Delete All Compilations":
            if sg.PopupYesNo('Are you sure you want to delete all compilations? This cannot be undone.', icon = logo) == 'Yes':
                try:
                    shutil.rmtree(get_compilations_folderpath())
                except:
                    print('could not delete all compilations')
            check()
            
        if event == "Upload Video":
            
            if len(values['to_up']) < 1 :
                notif("Please select a compilation first")
            else:
                
            
                tagsIN = [x.strip() for x in values['tags'].split(',')]
          
                string = 'Are you sure you would like to upload this video to your channel?'
                string += '\nTitle: '+ values['title']
                string += '\nDescription: ' +  values['description'][0:50] + "..."
                string += '\nTags: '+ values['tags'][0:50] + "..."
                string += '\nPrivacy: '+  values['privacy'].lower()
                string += '\nCategory: '+  values['cat']
                string += '\nVideo File: ' + values['to_up'][0]
                
                if sg.PopupYesNo(string, icon = logo) == 'Yes':
                
                    client = ''

                    filepathIN = os.path.join(get_compilations_folderpath(), values['to_up'][0])
                    
                    initialize_upload(client, filepathIN, values['title'], values['description'], tagsIN, 23, values['privacy'].lower())

        
        
        
        window['to_compile'].update(get_collection_names())
        window['compile_names'].update('\nCompiled Collections:\n' + get_compilation_names_string())
        window['del_coll'].update(get_collection_names())
        window['del_comp'].update(get_compilation_names())   
        window['to_up'].update(get_compilation_names()) 
        
        
             
    window.close()
    
    
    
def notif(msg):
    sg.popup( msg, icon = logo)

def pop(msg = 'Something went wrong'):
    sg.popup('Error:', msg)
    
def write_default_config():
    config = configparser.ConfigParser()
    config['config']= {}
    config['config']['working directory'] = os.path.dirname(os.path.realpath(__file__))
    config['config']['client id'] =  ' '
    config['config']['client secret'] = ' '
    
            

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def get_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        idi = config['config']['client id']
    except:
        write_default_config()
        config.read('config.ini')
    return config

def get_working_directory():
    config = get_config()
    return config['config']['working directory']

def set_working_directory(path):
    config = get_config()
    config['config']['working directory']= path
            
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        
def get_client_id():
    config = get_config()
    return config['config']['client id']
    
def get_client_secret():
    config = get_config()
    return config['config']['client secret']

def set_client_id(entry):
    config = get_config()
    config['config']['client id'] = entry
            
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def set_client_secret(entry):
    config = get_config()
    config['config']['client secret'] = entry
            
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
     

def get_temp_folder():
    return os.path.join(get_working_directory(), 'temp')      
        
def get_collections_folderpath():
    return os.path.join(get_working_directory(), 'collections')

def get_compilations_folderpath():
    return os.path.join(get_working_directory(), 'compilations')
        
def get_collection_names():
    names = [f.name for f in os.scandir(get_collections_folderpath()) if f.is_dir() ]
    if len(names) ==0:
        names.append('')
    return names

def get_collection_clip_paths(folderpath):
    onlyfiles = [f for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, f))]
    
    toks = []
    
    for file in onlyfiles:
        if file[-4:] == '.mp4':
            toks.append(os.path.join(folderpath,file))
            
    if len(toks) > 30:
        toks = toks[:30]
        
    return toks
    
def get_compilation_names():
    files = os.listdir(get_compilations_folderpath())
    
    comps=[]
    
    for file in files:
        if file.endswith(".mp4"):
            comps.append(file)
    
    if len(comps) == 0:
        comps.append(' ')

    return comps
    
def get_compilation_names_string():
    comps = get_compilation_names()
    
    string = ''
    for comp in comps:
        string = string + '\n' + comp
    
    
    return string
    
    
def CompDupeCheck(name):
    files = os.listdir(get_compilations_folderpath())
    if name +'.mp4' in files:
        if sg.PopupYesNo('This compilation already exists. Overwrite?', icon = logo) == 'Yes':
            os.remove(os.path.join(get_compilations_folderpath(), name +'.mp4'))
            return False
        else:
            return True
         
        
        #overwrite, delete, return false

def DupeCheck(collection):
    if os.path.exists(collection):
        if sg.PopupYesNo('This collection already exists. Overwrite?', icon = logo) == 'Yes':
            shutil.rmtree(collection)
            return False
        else:
            return True
        
        #overwrite, delete, return false

def check():
    folders = ['collections', 'compilations', 'temp']
    for folder in folders:
        if not os.path.isdir(os.path.join(get_working_directory(), folder)):
            os.mkdir(os.path.join(get_working_directory(), folder))





















#!/usr/bin/python

import httplib2
import random
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10


# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# CLIENT_SECRETS_FILE, name of a file containing the OAuth 2.0 information for
# this application, including client_id and client_secret. You can acquire an
# ID/secret pair from the API Access tab on the Google APIs Console
#   http://code.google.com/apis/console#access
# For more information about using OAuth2 to access Google APIs, please visit:
#   https://developers.google.com/accounts/docs/OAuth2
# For more information about the client_secrets.json file format, please visit:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# Please ensure that you have enabled the YouTube Data API for your project.




# A limited OAuth 2 access scope that allows for uploading files, but not other
# types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console
https://code.google.com/apis/console#access

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""

def secret_client_file():
	for file in os.listdir('./ID'):
		if file.endswith(".json"):
			selected_id = os.path.join("ID",file)
			#print('client_secret_id : ',selected_id)
			return selected_id

def get_authenticated_service(client):
    #client = json.dumps(client)
    #CLIENT_SECRETS_FILE = client
    
    
    CLIENT_SECRETS_FILE = secret_client_file()
    
    print (client)
    print (CLIENT_SECRETS_FILE)
    
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def initialize_upload(client, filepathIN, titleIN, descriptionIN, tagsIN = None, categoryIN = None, privacyIN = None):
    youtube = get_authenticated_service(client)

    body=dict(
      snippet=dict(
        title=titleIN,
        description=descriptionIN,
        tags=tagsIN,
        categoryId=categoryIN
      ),
      status=dict(
        privacyStatus=privacyIN
      )
    )
    
    insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
    body=body,

    media_body=MediaFileUpload(filepathIN, chunksize=-1, resumable=True)
  )


    resumable_upload(insert_request)


def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print ("Uploading file...")
      status, response = insert_request.next_chunk()
      if 'id' in response:
        
        print (response['id'])
        
        if sg.popup_yes_no('Your compilation was succesfully uploaded!\n View the upload now in your browser?', icon = logo) == 'Yes':
            webbrowser.open('https://www.youtube.com/watch?v=' + response['id'])


      else:
        exit("The upload failed with an unexpected response: %s" % response)
    except Exception as e:
      print(e)
      


    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)









            
    
    
    
    
    
    
from base64 import urlsafe_b64encode
import hashlib
import json
import logging
try:
    from secrets import SystemRandom
except ImportError:  # pragma: NO COVER
    from random import SystemRandom
from string import ascii_letters, digits

import wsgiref.simple_server
import wsgiref.util
import webbrowser
import google.auth.transport.requests
import google.oauth2.credentials
from six.moves import input

import google_auth_oauthlib.helpers


_LOGGER = logging.getLogger(__name__)


class Flow(object):
    """OAuth 2.0 Authorization Flow

    This class uses a :class:`requests_oauthlib.OAuth2Session` instance at
    :attr:`oauth2session` to perform all of the OAuth 2.0 logic. This class
    just provides convenience methods and sane defaults for doing Google's
    particular flavors of OAuth 2.0.

    Typically you'll construct an instance of this flow using
    :meth:`from_client_secrets_file` and a `client secrets file`_ obtained
    from the `Google API Console`_.

    .. _client secrets file:
        https://developers.google.com/identity/protocols/OAuth2WebServer
        #creatingcred
    .. _Google API Console:
        https://console.developers.google.com/apis/credentials
    """

    def __init__(
            self, oauth2session, client_type, client_config,
            redirect_uri=None, code_verifier=None,
            autogenerate_code_verifier=False):
        """
        Args:
            oauth2session (requests_oauthlib.OAuth2Session):
                The OAuth 2.0 session from ``requests-oauthlib``.
            client_type (str): The client type, either ``web`` or
                ``installed``.
            client_config (Mapping[str, Any]): The client
                configuration in the Google `client secrets`_ format.
            redirect_uri (str): The OAuth 2.0 redirect URI if known at flow
                creation time. Otherwise, it will need to be set using
                :attr:`redirect_uri`.
            code_verifier (str): random string of 43-128 chars used to verify
                the key exchange.using PKCE.
            autogenerate_code_verifier (bool): If true, auto-generate a
                code_verifier.
        .. _client secrets:
            https://developers.google.com/api-client-library/python/guide
            /aaa_client_secrets
        """
        self.client_type = client_type
        """str: The client type, either ``'web'`` or ``'installed'``"""
        self.client_config = client_config[client_type]
        """Mapping[str, Any]: The OAuth 2.0 client configuration."""
        self.oauth2session = oauth2session
        """requests_oauthlib.OAuth2Session: The OAuth 2.0 session."""
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.autogenerate_code_verifier = autogenerate_code_verifier

    @classmethod
    def from_client_config(cls, client_config, scopes, **kwargs):
        """Creates a :class:`requests_oauthlib.OAuth2Session` from client
        configuration loaded from a Google-format client secrets file.

        Args:
            client_config (Mapping[str, Any]): The client
                configuration in the Google `client secrets`_ format.
            scopes (Sequence[str]): The list of scopes to request during the
                flow.
            kwargs: Any additional parameters passed to
                :class:`requests_oauthlib.OAuth2Session`

        Returns:
            Flow: The constructed Flow instance.

        Raises:
            ValueError: If the client configuration is not in the correct
                format.

        .. _client secrets:
            https://developers.google.com/api-client-library/python/guide
            /aaa_client_secrets
        """
        if 'web' in client_config:
            client_type = 'web'
        elif 'installed' in client_config:
            client_type = 'installed'
        else:
            raise ValueError(
                'Client secrets must be for a web or installed app.')

        # these args cannot be passed to requests_oauthlib.OAuth2Session
        code_verifier = kwargs.pop('code_verifier', None)
        autogenerate_code_verifier = kwargs.pop(
            'autogenerate_code_verifier', None)

        session, client_config = (
            google_auth_oauthlib.helpers.session_from_client_config(
                client_config, scopes, **kwargs))

        redirect_uri = kwargs.get('redirect_uri', None)

        return cls(
            session,
            client_type,
            client_config,
            redirect_uri,
            code_verifier,
            autogenerate_code_verifier
        )

    @classmethod
    def from_client_secrets_file(cls, client_secrets_file, scopes, **kwargs):
        """Creates a :class:`Flow` instance from a Google client secrets file.

        Args:
            client_secrets_file (str): The path to the client secrets .json
                file.
            scopes (Sequence[str]): The list of scopes to request during the
                flow.
            kwargs: Any additional parameters passed to
                :class:`requests_oauthlib.OAuth2Session`

        Returns:
            Flow: The constructed Flow instance.
        """
        
        
        with open(client_secrets_file, 'r') as json_file:
            client_config = json.load(json_file)
        
        

        return cls.from_client_config(client_config, scopes=scopes, **kwargs)

    @property
    def redirect_uri(self):
        """The OAuth 2.0 redirect URI. Pass-through to
        ``self.oauth2session.redirect_uri``."""
        return self.oauth2session.redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, value):
        self.oauth2session.redirect_uri = value

    def authorization_url(self, **kwargs):
        """Generates an authorization URL.

        This is the first step in the OAuth 2.0 Authorization Flow. The user's
        browser should be redirected to the returned URL.

        This method calls
        :meth:`requests_oauthlib.OAuth2Session.authorization_url`
        and specifies the client configuration's authorization URI (usually
        Google's authorization server) and specifies that "offline" access is
        desired. This is required in order to obtain a refresh token.

        Args:
            kwargs: Additional arguments passed through to
                :meth:`requests_oauthlib.OAuth2Session.authorization_url`

        Returns:
            Tuple[str, str]: The generated authorization URL and state. The
                user must visit the URL to complete the flow. The state is used
                when completing the flow to verify that the request originated
                from your application. If your application is using a different
                :class:`Flow` instance to obtain the token, you will need to
                specify the ``state`` when constructing the :class:`Flow`.
        """
        kwargs.setdefault('access_type', 'offline')
        if self.autogenerate_code_verifier:
            chars = ascii_letters+digits+'-._~'
            rnd = SystemRandom()
            random_verifier = [rnd.choice(chars) for _ in range(0, 128)]
            self.code_verifier = ''.join(random_verifier)

        if self.code_verifier:
            code_hash = hashlib.sha256()
            code_hash.update(str.encode(self.code_verifier))
            unencoded_challenge = code_hash.digest()
            b64_challenge = urlsafe_b64encode(unencoded_challenge)
            code_challenge = b64_challenge.decode().split('=')[0]
            kwargs.setdefault('code_challenge', code_challenge)
            kwargs.setdefault('code_challenge_method', 'S256')
        url, state = self.oauth2session.authorization_url(
            self.client_config['auth_uri'], **kwargs)

        return url, state

    def fetch_token(self, **kwargs):
        """Completes the Authorization Flow and obtains an access token.

        This is the final step in the OAuth 2.0 Authorization Flow. This is
        called after the user consents.

        This method calls
        :meth:`requests_oauthlib.OAuth2Session.fetch_token`
        and specifies the client configuration's token URI (usually Google's
        token server).

        Args:
            kwargs: Arguments passed through to
                :meth:`requests_oauthlib.OAuth2Session.fetch_token`. At least
                one of ``code`` or ``authorization_response`` must be
                specified.

        Returns:
            Mapping[str, str]: The obtained tokens. Typically, you will not use
                return value of this function and instead and use
                :meth:`credentials` to obtain a
                :class:`~google.auth.credentials.Credentials` instance.
        """
        kwargs.setdefault('client_secret', self.client_config['client_secret'])
        kwargs.setdefault('code_verifier', self.code_verifier)
        return self.oauth2session.fetch_token(
            self.client_config['token_uri'], **kwargs)

    @property
    def credentials(self):
        """Returns credentials from the OAuth 2.0 session.

        :meth:`fetch_token` must be called before accessing this. This method
        constructs a :class:`google.oauth2.credentials.Credentials` class using
        the session's token and the client config.

        Returns:
            google.oauth2.credentials.Credentials: The constructed credentials.

        Raises:
            ValueError: If there is no access token in the session.
        """
        return google_auth_oauthlib.helpers.credentials_from_session(
            self.oauth2session, self.client_config)

    def authorized_session(self):
        """Returns a :class:`requests.Session` authorized with credentials.

        :meth:`fetch_token` must be called before this method. This method
        constructs a :class:`google.auth.transport.requests.AuthorizedSession`
        class using this flow's :attr:`credentials`.

        Returns:
            google.auth.transport.requests.AuthorizedSession: The constructed
                session.
        """
        return google.auth.transport.requests.AuthorizedSession(
            self.credentials)


class InstalledAppFlow(Flow):
    """Authorization flow helper for installed applications.

    This :class:`Flow` subclass makes it easier to perform the
    `Installed Application Authorization Flow`_. This flow is useful for
    local development or applications that are installed on a desktop operating
    system.

    This flow has two strategies: The console strategy provided by
    :meth:`run_console` and the local server strategy provided by
    :meth:`run_local_server`.

    Example::

        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['profile', 'email'])

        flow.run_local_server()

        session = flow.authorized_session()

        profile_info = session.get(
            'https://www.googleapis.com/userinfo/v2/me').json()

        print(profile_info)
        # {'name': '...',  'email': '...', ...}


    Note that these aren't the only two ways to accomplish the installed
    application flow, they are just the most common ways. You can use the
    :class:`Flow` class to perform the same flow with different methods of
    presenting the authorization URL to the user or obtaining the authorization
    response, such as using an embedded web view.

    .. _Installed Application Authorization Flow:
        https://developers.google.com/api-client-library/python/auth
        /installed-app
    """
    _OOB_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    _DEFAULT_AUTH_PROMPT_MESSAGE = (
        'Please visit this URL to authorize this application: {url}')
    """str: The message to display when prompting the user for
    authorization."""
    _DEFAULT_AUTH_CODE_MESSAGE = (
        'Enter the authorization code: ')
    """str: The message to display when prompting the user for the
    authorization code. Used only by the console strategy."""

    _DEFAULT_WEB_SUCCESS_MESSAGE = (
        'The authentication flow has completed. You may close this window.')

    def run_console(
            self,
            authorization_prompt_message=_DEFAULT_AUTH_PROMPT_MESSAGE,
            authorization_code_message=_DEFAULT_AUTH_CODE_MESSAGE,
            **kwargs):
        """Run the flow using the console strategy.

        The console strategy instructs the user to open the authorization URL
        in their browser. Once the authorization is complete the authorization
        server will give the user a code. The user then must copy & paste this
        code into the application. The code is then exchanged for a token.

        Args:
            authorization_prompt_message (str): The message to display to tell
                the user to navigate to the authorization URL.
            authorization_code_message (str): The message to display when
                prompting the user for the authorization code.
            kwargs: Additional keyword arguments passed through to
                :meth:`authorization_url`.

        Returns:
            google.oauth2.credentials.Credentials: The OAuth 2.0 credentials
                for the user.
        """
        kwargs.setdefault('prompt', 'consent')

        self.redirect_uri = self._OOB_REDIRECT_URI

        auth_url, _ = self.authorization_url(**kwargs)
        
        
        '''
        print(authorization_prompt_message.format(url=auth_url))

        code = input(authorization_code_message)
        '''
        
        webbrowser.open(auth_url, new = 1)
        
        code = sg.popup_get_text('A seperate browser window should have opened.\nPlease authorize the app and paste the authorization code below.', icon = logo)
        
        sg.popup('Please wait while Tikbot attempts to upload your compilation...', icon = logo, non_blocking=True, auto_close=True,
    auto_close_duration=3)
        
        self.fetch_token(code=code)

        return self.credentials

    def run_local_server(
            self, host='localhost', port=8080,
            authorization_prompt_message=_DEFAULT_AUTH_PROMPT_MESSAGE,
            success_message=_DEFAULT_WEB_SUCCESS_MESSAGE,
            open_browser=True,
            **kwargs):
        """Run the flow using the server strategy.

        The server strategy instructs the user to open the authorization URL in
        their browser and will attempt to automatically open the URL for them.
        It will start a local web server to listen for the authorization
        response. Once authorization is complete the authorization server will
        redirect the user's browser to the local web server. The web server
        will get the authorization code from the response and shutdown. The
        code is then exchanged for a token.

        Args:
            host (str): The hostname for the local redirect server. This will
                be served over http, not https.
            port (int): The port for the local redirect server.
            authorization_prompt_message (str): The message to display to tell
                the user to navigate to the authorization URL.
            success_message (str): The message to display in the web browser
                the authorization flow is complete.
            open_browser (bool): Whether or not to open the authorization URL
                in the user's browser.
            kwargs: Additional keyword arguments passed through to
                :meth:`authorization_url`.

        Returns:
            google.oauth2.credentials.Credentials: The OAuth 2.0 credentials
                for the user.
        """
        wsgi_app = _RedirectWSGIApp(success_message)
        local_server = wsgiref.simple_server.make_server(
            host, port, wsgi_app, handler_class=_WSGIRequestHandler)

        self.redirect_uri = 'http://{}:{}/'.format(
            host, local_server.server_port)
        auth_url, _ = self.authorization_url(**kwargs)

        if open_browser:
            webbrowser.open(auth_url, new=1, autoraise=True)

        print(authorization_prompt_message.format(url=auth_url))

        local_server.handle_request()

        # Note: using https here because oauthlib is very picky that
        # OAuth 2.0 should only occur over https.
        authorization_response = wsgi_app.last_request_uri.replace(
            'http', 'https')
        self.fetch_token(authorization_response=authorization_response)

        return self.credentials


class _WSGIRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    """Custom WSGIRequestHandler.

    Uses a named logger instead of printing to stderr.
    """
    def log_message(self, format, *args):
        # pylint: disable=redefined-builtin
        # (format is the argument name defined in the superclass.)
        _LOGGER.info(format, *args)


class _RedirectWSGIApp(object):
    """WSGI app to handle the authorization redirect.

    Stores the request URI and displays the given success message.
    """

    def __init__(self, success_message):
        """
        Args:
            success_message (str): The message to display in the web browser
                the authorization flow is complete.
        """
        self.last_request_uri = None
        self._success_message = success_message

    def __call__(self, environ, start_response):
        """WSGI Callable.

        Args:
            environ (Mapping[str, Any]): The WSGI environment.
            start_response (Callable[str, list]): The WSGI start_response
                callable.

        Returns:
            Iterable[bytes]: The response body.
        """
        start_response('200 OK', [('Content-type', 'text/plain')])
        self.last_request_uri = wsgiref.util.request_uri(environ)
        return [self._success_message.encode('utf-8')]    
    
    
    
    
    
    
def main():
    check()
    main_window()
    
    
    
main()

# [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],
