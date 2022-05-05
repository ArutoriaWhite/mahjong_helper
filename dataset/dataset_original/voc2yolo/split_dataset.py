import os
import random

os.system('rm -rf train')
os.system('rm -rf valid')
os.system('rm -rf test')

os.system('mkdir train')
os.system('mkdir train/images')
os.system('mkdir train/labels')
os.system('mkdir valid')
os.system('mkdir valid/images')
os.system('mkdir valid/labels')
os.system('mkdir test')
os.system('mkdir test/images')
os.system('mkdir test/labels')

images = sorted(os.listdir('images'))
labels = sorted(os.listdir('labels'))
img_and_lbl = [(i,l) for i,l in zip(images,labels)]

random.shuffle(img_and_lbl)

for i, (img, lbl) in enumerate(img_and_lbl):
    if i/len(img_and_lbl) < 0.9:
        os.system(f'cp images/{img} train/images/{img}')
        os.system(f'cp labels/{lbl} train/labels/{lbl}')        
    if i/len(img_and_lbl) > 0.8 and i/len(img_and_lbl) < 0.95 :
        os.system(f'cp images/{img} valid/images/{img}')
        os.system(f'cp labels/{lbl} valid/labels/{lbl}')   
    if i/len(img_and_lbl) >= 0.95:
        os.system(f'cp images/{img} test/images/{img}')
        os.system(f'cp labels/{lbl} test/labels/{lbl}')                   