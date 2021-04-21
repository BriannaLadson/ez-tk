import os

#Dir & File
def create_dir(path):
	if os.path.isdir(path) == False:
		os.mkdir(path)
		
		return False
		
	else:
		return True