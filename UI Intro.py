import PySimpleGUI as sg
import title_generator as tg
import threading
import GetClip as gc
import sys
import os

import shutil
import icon
logo = icon.logo

config = {}
config['dir'] = ''


def Intro():
    sg.theme('SystemDefaultForReal')
    layout = [  [sg.Text('Welcome to TikBot!', size = (15,1))],
                [sg.Text('-'*130, text_color = 'light grey')],
                [sg.Text('Please set your working directory:',  size=(35, 1))],      
                     [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='middle'), sg.InputText(config['dir'], key = 'dir'), sg.FolderBrowse()], 
                [sg.Button('Next'), sg.Button('Cancel')] ]
    window = sg.Window('TikBot ', layout, icon = logo )
        
    event, values = window.read()
        
    if event == 'Next':
        config['dir'] = os.path.normpath(values['dir'])
        window.close()
        
    if event in (None, 'Cancel'): 
        window.close()
        sys.exit()
    
        
        

def PageTwo():
    sg.theme('SystemDefaultForReal')
    layout = [       [sg.Text('Name this collection: ')],
                     [sg.Text(config['dir'] + '\\', text_color = 'grey'), sg.InputText( key='collection', size= (60,1))],
                     [sg.Text('-'*180, text_color = 'light grey')],
                     [sg.Text('Paste the links to each tiktok you would like to add to this collection, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(100, 10), key = 'urls')],
                     [sg.Text('-'*180, text_color = 'light grey')],
                     [sg.Button('Create Collection'), sg.Button('Cancel'), sg.Text(" "*100), sg.Button('Compile Collection', tooltip = 'Edit a collection into a compilation')] ]

    window = sg.Window('TikBot ', layout, icon = logo )
    while True:
        
        event, values = window.read()
        
        
        if event in (None, 'Cancel'): 
            break
        if event == "Create Collection":
            
            collection_path = os.path.join(config['dir'], values['collection'])
            
            if not DupeCheck(collection_path):
                os.mkdir(collection_path)
                thread = threading.Thread(target = gc.GetClip, args = (collection_path, values['urls'].split()))
                thread.start()
                
                
                
    window.close()


def pop(msg = 'Something went wrong'):
    sg.popup('Error:', msg)
    
    
    

def DupeCheck(collection):
    if os.path.exists(collection):
        if sg.PopupYesNo('This collection already exists. Overwrite?', icon = logo) == 'Yes':
            shutil.rmtree(collection)
            return False
        else:
            return True
        
    
        
        
        #overwrite, delete, return false
        
        
        
    
def main():
    Intro()
    PageTwo()
    
    
main()

# [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],