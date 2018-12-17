import os
import re

'''
TODO#
помечаем папки, в которых количество файлов не совпадает

'''

PATH_2017 = '/media/user/Work/temp/2017/'
PATH_2018 = '/media/user/Work/temp/2018/Ресурс/'

DIR_NAME = '=JD01E11+MCS02'

REG = r'^[2-9][0-9]\.[0-9]{2}\:' # regexp to get only 20.00 - 100.00 params
# example
# 25.04: TORQUE REF B [%];Par.25.4;4;0;-200;200;;3;2

AREG = '^A\d' # to check that file startswith A2 or A3 smthing like that

class Cabinet():
    def __init__(self, path2017, path2018, dirname):
        self.path2017 = path2017
        self.path2018 = path2018
        self.result_path = '/media/user/Work/temp/test/'
        self.dirname = dirname
        self.path2017 = PATH_2017+DIR_NAME
        self.path2018 = PATH_2018+DIR_NAME
        self.dict2017 = {}
        self.dict2018 = {}


    def create_dict(self, path):
        # dir_example = '/media/user/Work/temp/2017/=JD01E11+MCS02/'
        # create dict {'filename'   :'А40 13122017.dwp',
        #              'folder_name':'A29_RT_AT_UFR_EXIT_2'
        #              'full_path'  :'А40 13122017.dwp'}
        files_list = []
        result = {}
        for address, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".dwp"):
                    # print('address = ', address)
                    # print('file = ', file)
                    # print(address+'/'+file)                   # первый вариант
                    # print(os.path.join(os.getcwd(), file))    # второй вариант
                    # full_path = os.path.join(os.getcwd() + '/' + address, file)
                    # result.append(full_path)   # добавить полный путь
                    # result.append(file)# не добавлять полный путь
                    dictname = {}

                    foldername = self.prepare_filename(address)
                    dictname['folder_name'] = foldername
                    dictname['full_path'] = address
                    dictname['filename'] = self.rename(file, foldername, address)
                    files_list.append(dictname) # dict with all data

        result['files'] = files_list
        result['files_qty'] = len(files)

        return result

    # get folder name and add this name to filename if filename is bad
    def prepare_filename(self, address):
        address = address.split('/')
        address = address[-2:-1]
        address = str(address[0])
        return address


    def rename(self, file, foldername, fullpath):
        # os.rename('old', 'new') << rename file
        # Add A and digit to file name if missing
        if not re.match(AREG, file):
            # print(foldername,'__', file)
            print(fullpath+'/'+file)
            old_name = fullpath+'/'+file
            new_name = foldername+'__'+file
            os.rename(old_name, new_name)
            return new_name
        else:
            return file


    def start(self):
        self.dict2017 = self.create_dict(self.path2017)
        self.dict2018 = self.create_dict(self.path2018)

        print('[...] Checking files quantity')

        if self.dict2017['files_qty'] == self.dict2018['files_qty']:
            print('[ + ] Quantity is okay.\n' )
        else:
            print('[ERROR] Quantity is NOT okay. ')
            print('[ERROR] Files quantity in dict2017 : {}'.format(self.dict2017['files_qty']))
            print('[ERROR] Files quantity in dict2017 : {}'.format(self.dict2017['files_qty']))

        # добавить логику, если количество файлов не равно
        return print('[INFO] Creating dicts with files info Finished.\n')

    def compare(self):
        for file2017 in self.dict2017['files']:
            # print('dict2017 filename : ', file2017['filename'][:3])
            # print(file2017['full_path']+'/'+file2017['filename'])
            path_to_file2017 = file2017['full_path']+'/'+file2017['filename']
            file2017_data = self.get_file_data(path_to_file2017)

            for file2018 in self.dict2018['files']:
                if file2018['filename'][:3] == file2017['filename'][:3]: # если имена файлов совпадают
                    print('[ + ] Match! Checking diffs')
                    path_to_file2018 = file2018['full_path']+'/'+file2018['filename']
                    file2018_data = self.get_file_data(path_to_file2018)
                    self.write_diff(file2017_data, file2018_data, file2018['filename'])


    def write_diff(self, file2017, file2018, result_filename): #
        diffs_counter = 0
        with open(self.result_path+DIR_NAME+result_filename, 'a+', encoding='utf-8') as tmp_file:
            l1 = len(file2017)
            l2 = len(file2018)

            if l1 > l2:
                l = l1
            else: l = l2
            for i in range(l):
                if file2017[i] != file2018[i]:
                    diffs_counter += 1
                    tmp_file.write(file2017[i])
                    tmp_file.write(file2018[i]+'\n')
            tmp_file.write('\n' + result_filename + '\n')
            if diffs_counter > 0:
                tmp_file.write('No difference found in {}'.format(result_filename))

    def get_file_data(self, file_path):
        # читаем файл, удаляем лишнее, пишем в список
        with open(file_path, 'r', encoding='utf-8') as file:
            alist = []
            for line in file:
                # alist.append(line)
                if re.match(REG, line):
                    alist.append(line)
            return alist


test1 = Cabinet(PATH_2017, PATH_2018, DIR_NAME )
result = test1.start()
result = test1.compare()