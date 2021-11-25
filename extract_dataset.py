import tarfile
import os

PATH_IMAGES = '.images/'

if os.path.exists(PATH_IMAGES) == False:
	os.system('cat utfpr_sbd3.part* > ./utfpr_sbd3.tar.gz') 

	file_path  = './utfpr_sbd3.tar.gz'
	file = tarfile.open(file_path)
	file.extractall('./')
	file.close()
print("Finished!")
