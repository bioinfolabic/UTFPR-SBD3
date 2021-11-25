import tarfile
import cv2
import os
import numpy as np
import seaborn as sns # Seaborn is a Python data visualization library based on matplotlib
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpl


def give_color_to_seg_img(seg, n_classes,  colors):

    if len(seg.shape)==3:
        seg = seg[:,:,0]
    seg_img = np.zeros( (seg.shape[0],seg.shape[1],3) ).astype('float')
    
    
    for c in range(1,n_classes):
        
        segc = (seg == c)
        seg_img[:,:,0] += (segc*( int(colors[c][0]*255) ))
        seg_img[:,:,1] += (segc*( int(colors[c][1]*255) ))
        seg_img[:,:,2] += (segc*( int(colors[c][2]*255) ))

    return(seg_img)


def loadClasses(file_name='clases.txt'):
	arq = open(file_name)
	classes = []
	for aClass in arq:
		classes.append(aClass.strip())
	return classes



PATH_ANNOTATIONS = 'annotations/'
PATH_MASKS = 'masks/'
PATH_IMAGES = 'images/'
CLASSES_PATH = './classes.txt'


if os.path.exists(PATH_IMAGES) == False:
	path  = 'dataset.tar.gz'
	opener, mode = tarfile.open, 'r:gz'
	cwd = os.getcwd()

	try:
		print("Extracting dataset")
		file = opener(path, mode)
		try: file.extractall()
		finally: file.close()
	finally:
		os.chdir(cwd)


target_names=loadClasses(CLASSES_PATH)
mpl.rcParams['font.size'] = 14
n_classes=len(target_names)
colors = sns.color_palette("husl", len(target_names))

fig = plt.figure(figsize=(31,30)) 
img_list = os.listdir(PATH_IMAGES)

img_name = img_list[5]

print("Image Generated: ", img_name)
img_path = os.path.join(PATH_IMAGES, img_name)
annot_path = os.path.join(PATH_ANNOTATIONS, img_name)
mask_path = os.path.join(PATH_MASKS, img_name)

#Reading Image, annotation and mask
img = cv2.imread(img_path)    
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
annot = cv2.imread(annot_path.split(".")[0]+".png")   
mask = cv2.imread(mask_path.split(".")[0]+".png")   

#Selecting classes id
classesImg = np.unique(annot)
annot = give_color_to_seg_img(annot, len(target_names), colors)
annot = np.array(annot, dtype=np.uint8)
annot = cv2.cvtColor(annot,cv2.COLOR_BGR2RGB)

#Saving Figure
fig = plt.figure()
ax1 = fig.add_subplot(1,3,1)
ax1.imshow(np.squeeze(img))
ax1.set_title("Original")
ax1.set_yticklabels([])
ax1.set_xticklabels([])

ax2 = fig.add_subplot(1,3,2)
ax2.imshow(mask)
ax2.set_title("Mask")
ax2.set_yticklabels([])
ax2.set_xticklabels([])

ax3 = fig.add_subplot(1,3,3)
ax3.imshow(np.squeeze(annot))
ax3.set_title("Annotation")

#Creating color palette
classes = []
listap = []
names = []
for i in classesImg:
	
	nameClass = target_names[i]
	if nameClass == 'BK': continue
	classes.append(nameClass)
	b = colors[i][0]
	g = colors[i][1]
	r = colors[i][2]

	p1 = ax3.bar([0, 1, 2], [0.2, 0.3, 0.1],  width=0.4, label=nameClass, align="center", color=[r,g,b])

	if nameClass not in names:
		listap.append(p1)
		names.append(nameClass)
	else:
		print(nameClass, " exists in ", target_names)
	ax3.legend(listap, names, loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
ax3.set_yticklabels([])
ax3.set_xticklabels([])

plt.axis('off')
plt.tight_layout()
plt.savefig("output_"+img_name)
	
