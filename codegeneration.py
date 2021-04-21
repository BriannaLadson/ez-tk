#Standard Python Modules
from tkinter import *
import shelve

def generate_code(save_path):
	MainFile(save_path).write()

	
class File:
	def __init__(self, save_path, file_name):
		self.save_path = save_path
		self.data_path = save_path + "/data"
		self.code_path = save_path + "/code"
	
		self.file_name = file_name
		
		self.get_data()
		
	def write(self):
		file = open(self.code_path + "/" + self.file_name, 'w')
		
		for line in self.code_lines:
			file.write(line + "\n")
		
		file.close()
		
	def get_data(self):
		file = shelve.open(self.data_path)
		
		for iid in self.iids:
			data = file[iid]
			
			setattr(self, iid, data)
			
		file.close()
	
class MainFile(File):
	def __init__(self, save_path):
		self.iids = [
			'root_title',
			'root_fullscreen',
			'root_screenwidth',
			'root_screenheight',
		]
	
		super().__init__(save_path, "main.py")
		
		self.code_lines = [
			"from tkinter import *",
			"",
			"root = Tk()",
			"root.title('{}')".format(self.root_title),
			"root.attributes('-fullscreen', {})".format(self.root_fullscreen),
			"root.geometry('{}x{}')".format(self.root_screenwidth, self.root_screenheight),
			"",
			"if __name__ == '__main__':",
			"	root.mainloop()"
		]