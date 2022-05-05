import os

suit = ['man', 'pin', 'sou']
suit_out = ['c', 'd', 'b']

honors_num = ['ton', 'nan', 'sha', 'pei', 'haku', 'hatsu', 'chun']
honors_num_out = ['east', 'south', 'west', 'north', 'white', 'green', 'red']

for s,so in zip(suit,suit_out):
    for i in range(1,10):
        os.system(f'wget -O {so}-{i}.png http://mahjong.onevis.net/images/tile_{s}{i}.png')

for h,ho in zip(honors_num, honors_num_out):
    os.system(f'wget -O honors-{ho}.png http://mahjong.onevis.net/images/tile_{h}.png')