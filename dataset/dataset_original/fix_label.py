import os

labels = os.listdir('labels')
#labels = ['line-74.xml']

for lbl in labels:
    with open(f'labels/{lbl}','r', encoding='ISO-8859-1') as f:
        content = f.read()
#        print(content)
#        print(content.find('hornors'))
        content = content.replace('hornors','honors')
        with open(f'fixed_labels/{lbl}', 'w+') as outf:
            outf.write(content)