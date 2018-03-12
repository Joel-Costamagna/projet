#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from tkinter import Frame, Menu, Scrollbar, Text, Tk, filedialog, messagebox

import sys
from tkinter.messagebox import showinfo


class keyboard:
    """les raccourcis clavier du menu"""
    _macOS = (sys.platform == "darwin")
    _cmd = "cmd" if _macOS else "ctrl"

    NEW = "{}-n".format(_cmd)
    OPEN = "{}-o".format(_cmd)
    SAVE = "{}-s".format(_cmd)
    SAVE_AS = "{}-Shift-S".format(_cmd)
    UNDO = "{}-z".format(_cmd)
    REDO = "{}-y".format(_cmd)
    QUIT = "cmd-q" if _macOS else "alt-F4"


class Editor:

    def __init__(self, master):
        self.root = master
        self.TITLE = "Text Editor"
        self.file_path = None
        self.set_title()

        _frame = Frame(master)
        self.yscrollbar = Scrollbar(_frame, orient="vertical")
        self.editor = Text(_frame, yscrollcommand=self.yscrollbar.set)
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config(wrap="word",  # use word wrapping
                           undo=True,  # Tk 8.4
                           width=80)
        self.editor.focus()
        self.yscrollbar.pack(side="right", fill="y")
        self.yscrollbar.config(command=self.editor.yview)
        _frame.pack(fill="both", expand=1)

        # instead of closing the window, execute a function
        master.protocol("WM_DELETE_WINDOW", self.file_quit)

        # create a top level menu
        self.menubar = Menu(master)
        # Menu item File
        filemenu = Menu(self.menubar, tearoff=0)  # tearoff = 0 => can't be seperated from window
        filemenu.add_command(label="New", underline=1, command=self.file_new, accelerator=keyboard.NEW)
        filemenu.add_command(label="Open...", underline=1, command=self.file_open, accelerator=keyboard.OPEN)
        filemenu.add_command(label="Save", underline=1, command=self.file_save, accelerator=keyboard.SAVE)
        filemenu.add_command(label="Save As...", underline=5, command=self.file_save_as, accelerator=keyboard.SAVE_AS)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=2, command=self.file_quit, accelerator=keyboard.QUIT)
        self.menubar.add_cascade(label="File", underline=0, menu=filemenu)

        # help menu
        helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=lambda x: showinfo("About", "WIP"))

        # asm menu
        program_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Code", menu=program_menu)
        execute_menu = Menu(program_menu, tearoff=0)

        program_menu.add_cascade(label="execute current file", menu=execute_menu)
        execute_menu.add_command(label="clock mode", command=lambda x: showinfo("About", "WIP"))
        execute_menu.add_command(label="button click simulate clock", command=lambda x: showinfo("About", "WIP"))

        program_menu.add_command(label="load in ROM", command=lambda x: showinfo("About", "WIP"))
        program_menu.add_command(label="Assembler", command=lambda x: showinfo("About", "WIP"))
        program_menu.add_command(label="Program", command=lambda x: showinfo("About", "WIP"))

        status_menu = Menu(program_menu, tearoff=0)
        program_menu.add_cascade(label="status Display", menu=status_menu)
        status_menu.add_command(label="register content", command=lambda x: showinfo("About", "WIP"))
        status_menu.add_command(label="screen output", command=lambda x: showinfo("About", "WIP"))
        status_menu.add_command(label="...", command=lambda x: showinfo("About", "WIP"))
        status_menu.add_command(label="...", command=lambda x: showinfo("About", "WIP"))

        input_menu = Menu(program_menu, tearoff=0)
        program_menu.add_cascade(label="Input Buffer", menu=input_menu)
        input_menu.add_command(label="read keyboard", command=lambda x: showinfo("About", "WIP"))
        input_menu.add_command(label="stock key & status", command=lambda x: showinfo("About", "WIP"))
        input_menu.add_command(label="...", command=lambda x: showinfo("About", "WIP"))
        input_menu.add_command(label="...", command=lambda x: showinfo("About", "WIP"))

        # display the menu
        master.config(menu=self.menubar)

    def save_if_modified(self):
        if self.editor.edit_modified():  # modified
            response = messagebox.askyesnocancel("Save?",
                                                 "This document has been modified. Do you want to save changes?")  #
            # yes = True, no = False, cancel = None
            if response:  # yes/save
                result = self.file_save()
                if result == "saved":  # saved
                    return True
                else:  # save cancelled
                    return None
            else:
                return response  # None = cancel/abort, False = no/discard
        else:  # not modified
            return True

    def file_new(self, event=None):
        result = self.save_if_modified()
        if result is not None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.editor.delete(1.0, "end")
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.file_path = None
            self.set_title()

    def file_open(self, event=None, filepath=None):
        result = self.save_if_modified()
        if result is not None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            if filepath is None:
                filepath = filedialog.askopenfilename()
            if filepath is not None and filepath != '':
                with open(filepath, encoding="utf-8") as f:
                    file_contents = f.read()  # Get all the text from file.
                # Set current text to file contents
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, file_contents)
                self.editor.edit_modified(False)
                self.file_path = filepath

    def file_save(self, event=None):
        if self.file_path is None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath=self.file_path)
        return result

    def file_save_as(self, event=None, filepath=None):
        if filepath is None:
            print("asking filename")
            filepath = filedialog.asksaveasfilename(
                    filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*')))
        try:
            with open(filepath, 'wb') as f:
                text = self.editor.get(1.0, "end-1c")
                f.write(bytes(text, 'UTF-8'))
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "saved"
        except FileNotFoundError as e:
            print('FileNotFoundError : {}'.format(e))
            return "cancelled"

    def file_quit(self, event=None):
        result = self.save_if_modified()
        if result is not None:  # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.root.destroy()  # sys.exit(0)

    def set_title(self, event=None):
        if self.file_path is not None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def undo(self, event=None):
        self.editor.edit_undo()

    def redo(self, event=None):
        self.editor.edit_redo()

    def main(self, event=None):
        self.editor.bind_all(keyboard.OPEN, self.file_open)
        self.editor.bind_all(keyboard.SAVE, self.file_save)
        self.editor.bind_all(keyboard.SAVE_AS, self.file_save_as)
        self.editor.bind_all(keyboard.REDO, self.redo)
        self.editor.bind_all(keyboard.UNDO, self.undo)


if __name__ == "__main__":
    root = Tk()
    root.wm_state('zoomed')
    editor = Editor(root)
    editor.main()
    root.mainloop()
