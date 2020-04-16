import PySimpleGUI as sg
import title_generator as tg
import videoConcatenate as vc
import threading
import GetClip as gc
import sys
import os
import configparser
import time         
import shutil
import icon

logo = icon.logo

def main_window():
    sg.theme('Default1')
    
    menu_def = [
                ['Help', ['Creating a Collection', 'Compiling a Collection', 'Uploading a Collection'  ]],
                ['About']
                ] 
    
    
 
    tab_1_1_layout = [  [sg.T('Coming Soon.')]
                        ] 
    
    tab_1_2_layout = [  [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
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
                         [sg.Listbox(get_collection_names(), size=(45, 15), key = 'to_compile' ), sg.Text('\nCompiled Collections:\n' + get_compilation_names(), key = 'compile_names')], 
                         [sg.Text('')],
                         [sg.Button('Compile Collection'), sg.Text(" "*110)] 
                         ]
    
    tab_3_layout = [    [sg.Text('\nSelect a collection to compile: ')],
                         
                         [sg.Button('Create Collection'), sg.Text(" "*110)] 
                         ]
    
    tab_4_layout = [      [sg.Text('\nChange your working directory: '+ ' '*60)],      
                           [sg.Text('Your Folder', size=(20, 1), auto_size_text=False, justification='middle'), sg.InputText(get_working_directory(), key = 'dir'), sg.FolderBrowse()], 
                           [sg.Button('Save')],
                           [sg.Text('-'*200, text_color = 'light grey')],
                           
                           [sg.Text('Delete Collection: '), sg.InputCombo(get_collection_names()), sg.Button('Delete'), sg.Text(' '*20), sg.Button('Delete All Collections'),],      
                           [sg.Text('-'*200, text_color = 'light grey')],
                           
                           [sg.Text('Delete Compilation: '), sg.InputCombo(get_collection_names()), sg.Button('Delete'), sg.Text(' '*20), sg.Button('Delete All Compilations'),],      
                           [sg.Text('-'*200, text_color = 'light grey')]
                           
                           ]
                       

    
    
    layout =   [[sg.Menu(menu_def, )],
                 [sg.TabGroup([[sg.Tab('Create A Collection', tab_1_layout )], [sg.Tab('Compile A Collection', tab_2_layout )],  [sg.Tab('Upload a Compilation to Youtube', tab_3_layout )],  [sg.Tab('Settings', tab_4_layout )]])]   
                       
                       ]          

    window = sg.Window('TikBot ', layout, icon = logo )
    while True:     
        
        event, values = window.read(timeout = 5000)

        if event == None: 
            break
        
        if event == "individual":
            collection_path =  os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']))
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
            name                = values['to_compile'][0]
            collection_path     = os.path.join(get_collections_folderpath(), os.path.normpath(name))
            
            if not CompDupeCheck(name) and len(get_collection_clip_paths(collection_path)) > 1:
                
                notif('Your collection has begun compiling. This may take some time depending on the size of the collection.')
                '''
                vc.concatenate_clips(get_compilations_folderpath(), name, collection_path)
                '''
                thread = threading.Thread(target = vc.concatenate_clips, args = (get_compilations_folderpath(), name, collection_path, get_temp_folder() ))
                thread.start()
                
        
        if event == "Save":
            set_working_directory(os.path.normpath(values['dir']))
            
        
        print('\nrefresh')
        window['to_compile'].update(get_collection_names())
        window['compile_names'].update('\nCompiled Collections:\n' + get_compilation_names())        
             
    window.close()
    
'''

def Intro():
    sg.theme('SystemDefaultForReal')
    layout = [  [sg.Text('Welcome to TikBot!', size = (15,1))],
                [sg.Text('-'*130, text_color = 'light grey')],
                [sg.Text('Set your working directory: '+ ' '*60)],      
                     [sg.Text('Your Folder', size=(20, 1), auto_size_text=False, justification='middle'), sg.InputText(get_working_directory(), key = 'dir'), sg.FolderBrowse()], 
                [sg.Button('Next'), sg.Button('Cancel')] ]
    window = sg.Window('TikBot ', layout, icon = logo)    
    while True:   
        event, values = window.read()
            
        if event == 'Next':
            set_working_directory(os.path.normpath(values['dir']))
            window.close() 
            PageTwo()
            

   
        if event in (None, 'Cancel'): 
            window.close()
            sys.exit()
            
            
            
def PageTwo():
    sg.theme('SystemDefaultForReal')
    
    tab1_layout = [    [sg.T('This is inside tab 1')]] 
    
    tab2_layout = [ [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(100, 10), key = 'urls')]]
                     
    
    layout = [       [sg.Text('Name this collection: ')],
                     [sg.InputText( key='collection', size= (60,1))],

                     
                     [sg.TabGroup([[sg.Tab('Scrape By Hashtag', tab1_layout ), sg.Tab('Add Tiktoks Individually', tab2_layout)]])],    
                     
                       [sg.Button('Create Collection'), sg.Button('Back'), sg.Text(" "*110), sg.Button('Compile Collection', tooltip = 'Edit a collection into a single video')] 
                       ]
                     
                     

    window = sg.Window('TikBot ', layout, icon = logo )
    while True:     
        
        event, values = window.read()

        if event == None: 
            break
        
        if event == "Create Collection":
            
            collection_path =  os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']))
            
            if not DupeCheck(collection_path):
                
                notif('Your collection has begun downloading...')
                os.makedirs(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
        if event == "Back":
            window.close()
            Intro()
            
        if event == "Compile Collection":
            window.close()
            PageThree()
                
             
    window.close()
    
    
def PageThree():
    sg.theme('SystemDefaultForReal')
    
    tab1_layout = [    [sg.T('This is inside tab 1')]] 
    
    tab2_layout = [ [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(100, 10), key = 'urls')]]
                     
    
    layout = [       [sg.Text('Name this collection: ')],
                     [sg.InputText( key='collection', size= (60,1))],

                     
                     [sg.TabGroup([[sg.Tab('Scrape By Hashtag', tab1_layout ), sg.Tab('Add Tiktoks Individually', tab2_layout)]])],    
                       [sg.Button('Create Collection'), sg.Button('Back'), sg.Text(" "*110), sg.Button('Compile Collection', tooltip = 'Edit a collection into a single video')] 
                       ]
                     
                     

    window = sg.Window('TikBot ', layout, icon = logo )
    while True:     
        
        event, values = window.read()

        if event == None: 
            break
        
        if event == "Create Collection":
            
            collection_path =  os.path.join(get_collections_folderpath(), os.path.normpath(values['collection']))
            
            if not DupeCheck(collection_path):
                
                notif('Your collection has begun downloading...')
                os.makedirs(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
        if event == "Back":
            window.close()
            Intro()
            
        if event == "Compile Collection":
            pop("Not Yet Implemented")
                
             
    window.close()
    
    
 '''  
    
    
def notif(msg):
    sg.popup( msg, icon = logo)

def pop(msg = 'Something went wrong'):
    sg.popup('Error:', msg)
    
def write_default_config():
    config = configparser.ConfigParser()
    config['config'] = {
            'working directory': os.path.dirname(os.path.realpath(__file__))
            }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def get_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        di = config['config']['working directory']
    except:
        write_default_config()
        config.read('config.ini')
    return config

def get_working_directory():
    config = get_config()
    return config['config']['working directory']

def set_working_directory(path):
    config = get_config()
    config['config'] = {
            'working directory': path
            }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
     

def get_temp_folder():
    return os.path.join(get_working_directory(), 'temp')      
        
def get_collections_folderpath():
    return os.path.join(get_working_directory(), 'collections')

def get_compilations_folderpath():
    return os.path.join(get_working_directory(), 'compilations')
        
def get_collection_names():
    return [f.name for f in os.scandir(get_collections_folderpath()) if f.is_dir() ]

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
    '''       
    if len(comps) == 0:
        comps.append("None")
    '''
    
    string = ''
    for comp in comps:
        string = string + '\n' + comp
    print(string)
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
        if not os.path.isdir(os.path.join(get_working_directory(),folder)):
            os.mkdir(os.path.join(get_working_directory(),folder)) 
        

    
def main():
    check()
    main_window()
    
    
    
main()

# [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],