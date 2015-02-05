#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ponezhil
#
# Created:     05-01-2014
# Copyright:   (c) Ponezhil 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import gpr_file
import os
import clearcase
import Maint_Tool

from Tkinter import *

def whichSelected () :
    print(select.curselection()[0])
    return int(select.curselection()[0])

def importErrors():
    global dist_errors_list, errors_list, error_test
    dist_errors_list = []
    errors_list = []
    error_test = {}
    Maint_Tool.import_errors(dist_errors_list,error_test, errors_list)
    select.delete(0,END)
    for error in errors_list :
        select.insert (END, error)

def update():
    file_names = []
    file_list = []
    err = errors_list[whichSelected()]
    Maint_Tool.get_file_name(err,error_test,file_names)
    print(file_names)
    ini = initVar.get()
    rep = replaceVar.get()
    print('error is ',err)
    print('Initialised with ',ini)
    print('Replaced with ',rep)
    Maint_Tool.call_error_fixer(file_names,err,ini,rep)
    top = Toplevel()
    top.title("Confirm")

    msg = Message(top, text='Repaced!!')
    msg.pack()

    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()

def makeWindow():
    global select, replaceVar, initVar
    error_test = {}
    error_list = []
    mainwin = Tk()


    frame1 = Frame(mainwin)       # select of error
    frame1.pack()
    scroll = Scrollbar(frame1, orient=VERTICAL)
    select = Listbox(frame1, yscrollcommand=scroll.set, height = 15, width = 100)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)

    frame2 = Frame(mainwin)       # select of error
    frame2.pack()
    Label(frame2, text="Initialise :").grid(row=0, column=0, sticky=W)
    Label(frame2, text="Replace String").grid(row=1, column=0, sticky=W)
    initVar = StringVar()
    init = Entry(frame2, textvariable=initVar, width = 90)
    init.grid(row=0, column=1, sticky=W)
    replaceVar = StringVar()
    replace = Entry(frame2, textvariable=replaceVar, width = 90)
    replace.grid(row=2, column=1, sticky=W)

    frame = Frame(mainwin)
    frame.pack()
    importButton = Button(frame,text=" ImportErrors  ",command=importErrors, bg = 'red')
    importButton.grid(row=0, column=0, sticky=N+S+E+W)
    replaceButton = Button(frame,text=" Replace  ",command=update, bg = 'green')
    replaceButton.grid(row=0, column=2, sticky=N+S+E+W)
    return mainwin

win = makeWindow()
win.mainloop()


file_names = []
error_test = {}
error_list = []
##import_errors(error_list, error_test)
##get_file_name(error_list, error_test, file_names)


