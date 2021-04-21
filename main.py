#Standard Python Modules
from tkinter import *
from tkinter import filedialog
import shelve
import os

#EZ Tk Modules
import helpfunctions as helpf
import screens
import codegeneration as codegen

class App(Tk):
	def __init__(self):
		helpf.create_dir("projects")
		
		super().__init__()
		
		self.title("EZ Tk")
		
		self.save_path = "projects/"
		
		w = self.winfo_screenwidth()
		h = self.winfo_screenheight()
		self.geometry("{}x{}".format(w, h))
		
		#iids
		self.iids = {
			'root_title',
			'root_fullscreen',
			'root_screenwidth',
			'root_screenheight',
		}
		
		self.init_menubar()
		
	def init_menubar(self):
		self.menubar = menubar = Menu(self)
		
		self.config(menu=menubar)
		
		#File Menu
		file_menu = Menu(menubar, tearoff=0)

		file_menu.add_command(label="New Project", command=self.new_project)
		
		file_menu.add_command(label="Open Project", command=self.load_project)
		
		file_menu.add_command(label="Save", command=self.save_project)
		
		#Code Menu
		code_menu = Menu(menubar, tearoff=0)
		
		code_menu.add_command(label="Generate Code", command=self.start_generate_code)
		
		#Add Menus to Menubar
		menubar.add_cascade(label="File", menu=file_menu)
		menubar.add_cascade(label="Code", menu=code_menu)
		
	def new_project(self):
		if not self.save_path == "projects/":
			screens.SaveCurrentProjectFirst(self, self.new_project)
			
		else:
			self.main_screen.destroy()
		
			self.main_screen = screens.Main(self, None)
		
	def save_project(self):
		save_path = self.save_path
		
		helpf.create_dir(save_path)
		
		self.save_tree_items()
		
	def save_tree_items(self):
		save_path = self.save_path
		tree = self.main_screen.tree
		
		#Open File
		file = shelve.open(save_path + "/data")
		
		#Project Name
		file['#0'] = tree.heading('#0')['text']
		
		#Get iid text and save to file with iid as key
		for iid in self.iids:
			text = tree.get_item_text(iid)
			
			file[iid] = text
		
		#Close File
		file.close()
		
	def load_project(self):
		if not self.save_path == "projects/":
			screens.SaveCurrentProjectFirst(self, self.load_project)
			
		else:
			load_path = filedialog.askdirectory(initialdir="projects", mustexist=True)
		
			if len(load_path) > 0:
				self.save_path = load_path
		
				self.load_tree_items(load_path)
		
	def load_tree_items(self, load_path):
		tree = self.main_screen.tree
		
		#Open File
		file = shelve.open(load_path + "/data")
		
		#Project Name
		project_name = file['#0']
		
		tree.heading('#0', text=project_name)
		
		#Use iid to get text from file, obtain its prefix, place in tree
		for iid in self.iids:
			text = file[iid]
			
			prefix = tree.get_prefix_from_iid(iid)
			
			tree.item(iid, text=prefix + text)
		
		#Close File
		file.close()
		
	def start_generate_code(self):
		tree = self.main_screen.tree
		
		if not self.save_path == "projects/":
			screens.SaveCurrentProjectFirst(self, self.start_generate_code)
			
		else:
			self.save_path += tree.heading('#0')['text']
			
			save_path = self.save_path
		
			code_path = save_path + "/code"
		
			code_dir = helpf.create_dir(code_path)
		
			if not code_dir:
				codegen.generate_code(save_path)
			
			else:
				#Ask user if they want to overwrite code directory.
				screens.OverwriteCodeDir(self)

if __name__ == "__main__":
	app = App()
	
	app.main_screen = screens.Main(app, None)
	
	app.mainloop()