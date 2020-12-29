import tkinter
from tkinter import *
from tkinter.constants import *
from tkinter import ttk
from tkinter.ttk import *

class Gui(tk.Frame):
        def __init__(self, master=None, **kwargs):

                tk.Frame.__init__(self, master, **kwargs)
                self.pack(fill=tk.BOTH)

                self.Options = WorkflowOptions()

                space_label = tk.Label(self, text=' ')
                space_label.grid(column=0, row=0)

                # Input CPACS file
                self.label = tk.Label(self, text='  Input CPACS file')
                self.label.grid(column=0, row=1)

                self.path_var = tk.StringVar()
                self.path_var.set(self.Options.cpacs_path)
                value_entry = tk.Entry(self, textvariable=self.path_var, width= 45)
                value_entry.grid(column=1, row=1)

                self.browse_button = tk.Button(self, text="Browse", command=self._browse_file)
                self.browse_button.grid(column=2, row=1, pady=5)

                # Notebook for tabs
                self.tabs = ttk.Notebook(self)
                self.tabs.grid(column=0, row=2, columnspan=3,padx=10,pady=10)

                self.TabPre = Tab(self, 'Pre')
                self.TabOptim = Tab(self, 'Optim')
                self.TabPost = Tab(self, 'Post')

                self.tabs.add(self.TabPre, text=self.TabPre.name)
                self.tabs.add(self.TabOptim, text=self.TabOptim.name)
                self.tabs.add(self.TabPost, text=self.TabPost.name)

                # General buttons
                self.close_button = tk.Button(self, text='Save & Quit', command=self._save_quit)
                self.close_button.grid(column=2, row=3)
