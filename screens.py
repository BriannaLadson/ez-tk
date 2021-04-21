from tkinter import *
from tkinter import ttk

import codegeneration as codegen

#Screen Types
class Screen:
	def __init__(self, app):
		self.app = app
		
		self.main_fr = Frame(app, bg="white")
		self.main_fr.pack(fill=BOTH, expand=1)
		
	def destroy(self):
		self.main_fr.destroy()
		
class Popup:
	def __init__(self, app, title):
		self.app = app
		
		self.top = Toplevel(app, bg="white")
		self.top.title(title)
		self.top.grab_set()
		
		self.fr = Frame(self.top, bg="white")
		self.fr.pack()
		
#Screens
class Main(Screen):
	def __init__(self, app, path):
		super().__init__(app)
		
		#Treeview
		treeview_fr = Frame(self.main_fr, bg="white")
		treeview_fr.pack(fill=Y, side=LEFT)
		
		self.tree = Tree(app, treeview_fr, path)
		self.tree.pack()
		
#Popups
class SaveCurrentProjectFirst(Popup):
	def __init__(self, app, func):
		super().__init__(app, "Save Project")
		
		self.func = func
		
		lbl = Label(self.fr, text="Do you want to save the current project first?", bg="white")
		lbl.pack()
		
		btn_fr = Frame(self.top, bg="white")
		btn_fr.pack()
		
		yes_btn = Button(btn_fr, text="Yes", command=lambda: self.continue_(True))
		yes_btn.pack(side=LEFT)
		
		no_btn = Button(btn_fr, text="No", command=lambda: self.continue_(False))
		no_btn.pack(side=LEFT)
		
	def continue_(self, bool):
		app = self.app
		
		if bool == True:
			app.save_project()
			
		app.save_path = "projects/"
			
		self.func()
		
		self.top.destroy()
		
class OverwriteCodeDir(Popup):
	def __init__(self, app):
		super().__init__(app, "Overwrite Code Directory")
		
		lbl = Label(self.fr, text="Do you want to overwrite the project's code directory?", bg="white")
		lbl.pack()
		
		btn_fr = Frame(self.top, bg="white")
		btn_fr.pack()
		
		yes_btn = Button(btn_fr, text="Yes", command=lambda: self.continue_(True))
		yes_btn.pack(side=LEFT)
		
		no_btn = Button(btn_fr, text="No", command=lambda: self.continue_(False))
		no_btn.pack(side=LEFT)
		
	def continue_(self, bool):
		app = self.app
		
		if bool == True:
			save_path = app.save_path
			
			codegen.generate_code(save_path)
			
		self.top.destroy()

class EditProjectName(Popup):
	def __init__(self, app, tree):
		super().__init__(app, "Edit Project Name")
		
		self.var = StringVar()
		
		ent = Entry(self.fr, textvariable=self.var)
		ent.pack(side=LEFT)
		
		ok = Button(self.fr, text="OK", command=lambda: self.ok(app, tree))
		ok.pack(side=LEFT)

		
	def ok(self, app, tree):
		string = self.var.get()
		
		if len(string) > 0:
			tree.heading('#0', text=string)
			
			app.save_path = "projects/" + string
			
		self.top.destroy()
		
class EditItemText(Popup):
	def __init__(self, app, tree, iid):
		title, prefix = tree.get_full_title_from_iid(iid)
		
		super().__init__(app, "Edit " + title)
		
		self.var = StringVar()
		
		ent = Entry(self.fr, textvariable=self.var)
		ent.pack(side=LEFT)
		
		ok = Button(self.fr, text="OK", command=lambda: self.ok(tree, iid, prefix))
		ok.pack(side=LEFT)
		
	def ok(self, tree, iid, prefix):
		string = self.var.get()
		
		if len(string) > 0:
			tree.item(iid, text=prefix + string)
			
		self.top.destroy()
		
class EditItemTextToInt(Popup):
	def __init__(self, app, tree, iid):
		title, prefix = tree.get_full_title_from_iid(iid)

		super().__init__(app, "Edit " + title)
		
		self.var = StringVar()
		self.var.trace_add("write", self.trace)
		
		ent = Entry(self.fr, textvariable=self.var)
		ent.pack(side=LEFT)
		
		self.ok_btn = Button(self.fr, text="OK", state=DISABLED, command=lambda: self.ok(tree, iid, prefix))
		self.ok_btn.pack(side=LEFT)
		
		self.trace()
		
	def trace(self, *args):
		value = self.var.get()
		
		try:
			value = int(value)
			
			if value <= 0:
				raise ValueError
				
			else:
				self.ok_btn.config(state=NORMAL)
			
		except ValueError:
			self.ok_btn.config(state=DISABLED)
			
	def ok(self, tree, iid, prefix):
		value = self.var.get()
		
		tree.item(iid, text=prefix + value)
		
		self.top.destroy()
		
class EditItemBool(Popup):
	def __init__(self, app, tree, iid):
		title, prefix = tree.get_full_title_from_iid(iid)
		
		super().__init__(app, "Edit " + title)
		
		self.var = BooleanVar()
		
		true_rb = Radiobutton(self.fr, text="True", variable=self.var, value=True, bg="white")
		true_rb.pack(side=LEFT)
		
		false_rb = Radiobutton(self.fr, text="False", variable=self.var, value=False, bg="white")
		false_rb.pack(side=LEFT)
		
		ok_btn = Button(self.fr, text="OK", command=lambda: self.ok(tree, iid, prefix))
		ok_btn.pack()
		
	def ok(self, tree, iid, prefix):
		bool = self.var.get()
		
		tree.item(iid, text = prefix + str(bool))
		
		self.top.destroy()
		
#Widgets
class Tree(ttk.Treeview):
	def __init__(self, app, parent, path):
		super().__init__(parent, selectmode=BROWSE)
		
		self.app = app
		
		#Column
		self.column("#0", anchor=W)
		
		#Heading
		self.heading('#0', text="New Project", anchor=W)
		
		#Root
		self.insert(parent ='', index = 'end', iid= "root", text="Root", values=("Root"))
		self.insert(parent="root", index='end', iid="root_title", text="Title")
		self.insert(parent="root", index='end', iid="root_fullscreen", text="Fullscreen: True")
		self.insert(parent="root", index='end', iid="root_screenwidth", text="Screenwidth: 1")
		self.insert(parent="root", index='end', iid="root_screenheight", text="Screenheight: 1")
		
		#iids sets
		self.text_iids = {
			'root_title',
		}
		
		self.text_to_int_iids = {
			'root_screenwidth',
			'root_screenheight',
		}
		
		self.bool_iids = {
			'root_fullscreen',
		}
		
		self.bind("<Double-Button-1>", lambda e: self.edit(e))
		
	def edit(self, event):
		app = self.app
		
		iid = self.focus()
		
		row = self.identify_row(event.y)
		
		if row == '':
			EditProjectName(app, self)
			
		elif iid in self.text_iids:
			EditItemText(app, self, iid)
			
		elif iid in self.text_to_int_iids:
			EditItemTextToInt(app, self, iid)
			
		elif iid in self.bool_iids:
			EditItemBool(app, self, iid)
			
	def get_full_title_from_iid(self, iid):
		split_str = iid.split("_")
		
		title = ""
		
		for i in split_str:
			title += i.capitalize() + " "
			
		prefix = split_str[-1].capitalize() + ": "
				
		return title, prefix
		
	def get_prefix_from_iid(self, iid):
		split_str = iid.split("_")
		
		prefix = split_str[-1].capitalize() + ": "
		
		return prefix
		
	def get_item_text(self, iid):
		raw_text = self.item(iid)['text']
		
		split_str = raw_text.split(": ")
		
		return split_str[-1]