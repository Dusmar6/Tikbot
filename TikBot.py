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
    layout = [       [sg.Text('Name this collection: ')],
                     [sg.InputText( key='collection', size= (60,1))],
                     [sg.Text('-'*180, text_color = 'light grey')],
                     [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(100, 10), key = 'urls')],
                     [sg.Text('-'*180, text_color = 'light grey')],
                     [sg.Button('Create Collection'), sg.Button('Back'), sg.Text(" "*110), sg.Button('Compile Collection', tooltip = 'Edit a collection into a single video')] ]

    window = sg.Window('TikBot ', layout, icon = logo )
    while True:     
        
        event, values = window.read()

        if event == None: 
            break
        
        if event == "Create Collection":
            
            collection_path =  os.path.normpath(values['collection'])
            
            if not DupeCheck(collection_path):
                os.makedirs(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
        if event == "Back":
            window.close()
            Intro()
            
        if event == "Compile Collection":
            pop("Not Yet Implemented")
                
             
    window.close()
    
    
    


def pop(msg = 'Something went wrong'):
    sg.popup('Error:', msg)
    
def write_default_config():
    config = configparser.ConfigParser()
    config['config'] = {
            'collections directory': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'collections')
            }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def get_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        di = config['config']['collections directory']
    except:
        write_default_config()
        config.read('config.ini')
    return config

def get_working_directory():
    config = get_config()
    return config['config']['collections directory']

def set_working_directory(path):
    config = get_config()
    config['config'] = {
            'collections directory': path
            }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        
        
        
    

def DupeCheck(collection):
    if os.path.exists(collection):
        if sg.PopupYesNo('This collection already exists. Overwrite?', icon = logo) == 'Yes':
            shutil.rmtree(collection)
            return False
        else:
            return True
         
        
        #overwrite, delete, return false
        
        
        
    
def main():
    print(os.path.dirname(os.path.realpath(__file__)))

    Intro()
    
    
    
main()

# [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],