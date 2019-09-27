import collections
import os

directory = '/media/denis/dados/dev/face_bds_changed'

dic = {}
for dirname in os.listdir(directory):
    if dirname.endswith('fail'):
        count = 0
        for dirperson, directories, files in os.walk(os.path.join(directory, dirname)):
            for file in files:
                if file.startswith('1') or file.startswith('2') or file.startswith('3') or file.startswith(
                        '4') or file.startswith('5') or file.startswith('6') or file.startswith('7') or file.startswith(
                        '8') or file.startswith('9'):
                    count += 1
        dic[dirname] = count

odic = collections.OrderedDict(sorted(dic.items()))

with open('/media/denis/dados/dev/face_bds_changed/FACES_OFF.csv', 'w') as file:
    for dirn, dir_count in odic.items():
        file.writelines('{};{}\n'.format(dirn, dir_count / 860))
        # print('{};{}'.format(dirn, dir_count / 860))

for dirn, dir_count in odic.items():
    print('{}'.format(dir_count / 860))
