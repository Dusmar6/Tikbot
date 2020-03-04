import PySimpleGUI as sg
import title_generator as tg
import threading
import GetClip as gc

import icon
logo = icon.logo

config = {}
config['dir'] = 'TikBot_Projects'


def Intro():
    sg.theme('SystemDefaultForReal')
    layout = [  [sg.Text('Welcome to TikBot!', size = (15,1))],
                [sg.Text('_'*77, text_color = 'light grey')],
                [sg.Text('Please set your working directory:', size=(35, 1))],      
                     [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='middle'), sg.InputText('Tikbot'), sg.FolderBrowse()], 
                [sg.Button('Next'), sg.Button('Cancel')] ]
    window = sg.Window('TikBot ', layout, icon = logo )
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'): 
            break
        window.close()
        return values[0]
    

def PageTwo():
    sg.theme('SystemDefaultForReal')
    layout = [       [sg.Text('Name this project: '), sg.InputText(tg.generate_title(), key='title', size= (60,1))],
                     [sg.Text(' '*26),sg.Button(button_text="Generate Random Title")],
                     [sg.Text('_'*77, text_color = 'light grey')],
                     [sg.Text('Enter the links to each tiktok you would like to download, seperated by a new line.\nThese can be found by right clicking the video and going to "Inspect Element"')],
                     [sg.Multiline(default_text='', size=(50, 10), key = 'urls')],
                     [sg.Text('_'*77, text_color = 'light grey')],
                     [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()] ]
    window = sg.Window('TikBot ', layout, icon = logo )
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'): 
            break
        if event == "Generate Random Title":
            window['title'].update(tg.generate_title())
        if event == "Submit":
            print(values['urls'])
            thread = threading.Thread(target = gc.GetClip, args = (values['title'], values['urls'].split()))
            thread.start()
    window.close()


def pop(msg = 'Something went wrong'):
    sg.popup('Error:', msg)
    
def main():
    Intro()
    PageTwo()
    
    
main()

