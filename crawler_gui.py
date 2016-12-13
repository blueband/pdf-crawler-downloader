from tkinter import *
import tkinter.filedialog
import  tkinter.messagebox
import os
file_name = None

#PROJECT_DIR = os.curdir()
project_root = Tk()
project_root.geometry('550x200+500+200')    # Arrange the Display windows at the center of the screen
PROGRAM_NAME = 'BlueRazor ver: 3.1r(PDF File Crawler and Downloader ver: 3.1r)'
PROJECT_DIR = os.getcwd()
project_root.title(PROGRAM_NAME)
search_terms = StringVar()

project_menu = Menu(project_root)

# OS path to the Application Directory
# def appDir():
#     from os import path as App
#     print(os.getcwd())
#     print(App)

# define a function to be print on the screen
def about_messagebox_display(event=None):
    tkinter.messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME, "\n This is An Experimental Software, Use at your Risk")
    )

def help_messagebox_display(event=None):
    from gui_scrubbie_search import Spider as filepath
    PROJECT_DIR = filepath.project_directory_name
    tkinter.messagebox.showinfo("Help","{}{}".format("Software Usage available at", PROJECT_DIR))

# File Opener Menu
# def file_open(event=None):
#     input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", ".txt")])
#     if input_file_name:
#         global  file_name
#         file_name = input_file_name
#         project_root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
#         cont

# Unbounding the Search Terms
def search_word():
    global search_terms
    keyword = search_terms.get()
    from gui_scrubbie_search import Spider
    Spider(keyword)
    print('hello ', keyword)

# We adding File menu to Main Menu
file_menu = Menu(project_menu, tearoff=0)

# Menu_list will be add here
project_menu.add_cascade(label='File', menu=file_menu)
project_menu.add_cascade(label='Edit', menu=file_menu)
project_menu.add_cascade(label='View', menu=file_menu)

# About Menu
about_menu = Menu(project_menu, tearoff=0)
about_menu.add_command(label='About', command=about_messagebox_display)
about_menu.add_command(label='Help', command=help_messagebox_display)

project_menu.add_cascade(label='About', menu=about_menu)

project_root.config(menu=project_menu)

# implementing Logo Area
Label(project_root, text='PDF Crawler & Downloader',font="helvetica 30 bold italic").grid(row=1, columnspan=10)
Label(project_root, text='Enter Book Name to Search').grid(row=2, column=0, sticky=W)
project_keyword_search = Entry(project_root, textvariable=search_terms, width=50).grid(row=2, column=1, sticky=W)
Radiobutton(project_root, text='PDF only', value=1).grid(row=2, column=2,sticky=E)
project_search_button = Button(project_root, text='Search Now', command=search_word).grid(row=3, column=1)
#project_message_frame = Frame(project_root)
Message(project_root, text='hello world').grid(row=4, columnspan=6, sticky=W)







project_root.mainloop()