import PySimpleGUI as sg
import title_generator as tg
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
                ['About']] 
    
    
 
    tab_1_1_layout = [    [sg.T('This is inside tab 1')]] 
    
    tab_1_2_layout = [ [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(100, 10), key = 'urls')]]
                     
    tab_1_layout = [       [sg.Text('\nName this collection: ')],
                     [sg.InputText( key='collection', size= (60,1))],
                     [sg.Text('')],
                     [sg.TabGroup([[sg.Tab('Scrape By Hashtag', tab_1_1_layout ), sg.Tab('Add Tiktoks Individually', tab_1_2_layout)]])],   
                     [sg.Text(' ')],
                       [sg.Button('Create Collection'), sg.Text(" "*110)] 
                       ]
    
    tab_2_layout = [       [sg.Text('\nSelect a collection to compile: ')],
                     [sg.InputCombo(get_collection_names(), size=(20, 1))],
                       [sg.Button('Create Collection'), sg.Text(" "*110)] 
                       ]
    
    tab_3_layout = [       [sg.Text('Select a collection to compile: ')],
                     [sg.InputText(key='collection', size= (60,1))],
                       [sg.Button('Create Collection'), sg.Text(" "*110)] 
                       ]
    
    tab_4_layout = [      [sg.Text('\nChange your working directory: '+ ' '*60)],      
                     [sg.Text('Your Folder', size=(20, 1), auto_size_text=False, justification='middle'), sg.InputText(get_working_directory(), key = 'dir'), sg.FolderBrowse()], 
                [sg.Button('Save')],
                [sg.Text('-'*130, text_color = 'light grey')]
                                ]
                       

    
    
    layout =   [[sg.Menu(menu_def, )],
                 [sg.TabGroup([[sg.Tab('Create A Collection', tab_1_layout )], [sg.Tab('Compile A Collection', tab_2_layout )],  [sg.Tab('Upload a Compilation to Youtube', tab_3_layout )],  [sg.Tab('Settings', tab_4_layout )]])]   
                       
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
                
            
        if event == "Compile Collection":
            print()
        
        if event == "Save":
            set_working_directory(os.path.normpath(values['dir']))
                
             
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
        
def get_collections_folderpath():
    return os.path.join(get_working_directory(), 'collections')
        

def get_collection_names():
    return [f.name for f in os.scandir(get_collections_folderpath()) if f.is_dir() ]


def DupeCheck(collection):
    if os.path.exists(collection):
        if sg.PopupYesNo('This collection already exists. Overwrite?', icon = logo) == 'Yes':
            shutil.rmtree(collection)
            return False
        else:
            return True
         
        
        #overwrite, delete, return false
        
        
def check():
    
    if not os.path.isdir(os.path.join(get_working_directory(),'collections')):
        os.mkdir(os.path.join(get_working_directory(),'collections')) 
        
    if not os.path.isdir(os.path.join(get_working_directory(),'compilations')):
        os.mkdir(os.path.join(get_working_directory(),'compilations')) 

    
def main():
    check()
    main_window()
    
    
    
main()

# [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],