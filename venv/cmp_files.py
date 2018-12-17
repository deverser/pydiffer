import os
import re


dir2017 = '/media/user/Work/temp/2017/'
dir2018 = '/media/user/Work/temp/2018/Ресурс/'

# dir1path = '/media/user/Work/temp/2017/=JM01E69+DRA03/=JM01E69+DRA03_20170317/' # не совпадает количество
# dir2path = '/media/user/Work/temp/2018/Ресурс/=JM01E69+DRA03/=JM01E69+DRA03/' #

# dir1path = '/media/user/Work/temp/2017/=JD01E11+DRA01/=JD01E11+DRA01/'
# dir2path = '/media/user/Work/temp/2018/Ресурс/=JD01E11+DRA01/=JD01E11+DRA01/' # нет А в 12 и выше

# dir1path = '/media/user/Work/temp/2017/=JD01E06+DRA01/'
# dir2path = '/media/user/Work/temp/2018/Ресурс/=JD01E06+DRA01/'

# dir1path = '/media/user/Work/temp/2017/=JC01E05+DRM01/=JC01E05+DRM01/' # тоже нет А
# dir2path = '/media/user/Work/temp/2018/Ресурс/=JC01E05+DRM01/'

dir1path = '/media/user/Work/temp/2017/=JD01E11+MCS02/'
dir2path = '/media/user/Work/temp/2018/Ресурс/=JD01E11+MCS02/'

REG = r'^[2-9][0-9]\.[0-9]{2}\:' # regexp to get only 20.00 - 100.00 params
# example
# 25.04: TORQUE REF B [%];Par.25.4;4;0;-200;200;;3;2
AREG = '^A\d'
BASEDIR = '/media/user/Work/temp/cmp_test/'

fpath1 = '/media/user/Work/temp/cmp_test/А120 20170406.dwp'
fpath2 = '/media/user/Work/temp/cmp_test/A120_20180413.dwp'

# print('cwd = ', os.getcwd())
# print('список файлов', os.listdir(BASEDIR))
# files_list = os.listdir(BASEDIR)


def write_diffs(file1, file2):
    # пишем отличия в отдельный tmp файл
    l = 0
    with open('tmp', 'w', encoding='utf-8') as tmp_file:
        #
        # diffs_file.write('cabname = ' + cabname)
        # diffs_file.write('\n')
        # diffs_file.write('filename = ' + file1_path)
        # diffs_file.write('\n')
        # diffs_file.write('filename = ' + file2_path)
        # diffs_file.write('\n')

        l1 = len(file1)
        l2 = len(file2)

        if l1 > l2:
            l = l1
        else: l = l2

        for i in range(l):
            if file1[i] != file2[i]:
                tmp_file.write(file1[i])
                tmp_file.write(file2[i]+'\n')


# def write_cabname_to_file():
#     with open()


def get_file_data(file_path):
    # читаем файл, удаляем лишнее, пишем в список
    with open(file_path, 'r', encoding='utf-8') as file:
        alist = []
        for line in file:
            # alist.append(line)
            if re.match(REG, line):
                alist.append(line)
        return alist


def get_files_list(dir, extra=None):
    result = []
    res_dict = {}
    for address, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dwp"):
                # print(address+'/'+file)                   # первый вариант
                # print(os.path.join(os.getcwd(), file))    # второй вариант
                # full_path = os.path.join(os.getcwd() + '/' + address, file)
                # result.append(full_path)   # добавить полный путь
                result.append(file)# не добавлять полный путь
                if extra:
                    res_dict['filename']=file
                    res_dict['folder_name'] = address
                    res_dict['full_path'] = os.path.join(os.getcwd() + '/' + address, file)
    if extra:
        return result, res_dict
    else:
        return result


# os.rename(old, new)
def rename(flist):
    # Add A and digit to file name if missing
    l = len(flist)
    for i in range(l):
        if not re.match(AREG, flist[i]):
            print(os.path.abspath(os.curdir))
            # os.chdir('..')
            # print(os.getcwd())


cab1_files_list = get_files_list(dir1path)
cab2_files_list = get_files_list(dir2path)

# cab1_files_dict = get_files_list(dir1path, extra=True)
# print(cab1_files_dict)

sorted_cab1_flist = sorted(cab1_files_list)
sorted_cab2_flist = sorted(cab2_files_list)

# print(len(cab1_files_list), len(cab2_files_list))

# for i in range(len(sorted_cab1_flist)):
#     if sorted_cab1_flist[i]:
#         print(sorted_cab1_flist[i]+','+sorted_cab2_flist[i])


# file1 = get_file_data(fpath1)
# file2 = get_file_data(fpath2)
#
# write_diffs(file1, file2)
#
#
# renamed = rename(cab2_files_list)
# print('got some files with bad names', renamed)


def folder(address):
    address = address.split('/')
    print('after split: ', address)
    address = address[-2:-1]
    print('slice:' , address)
    return address


# {filename:'', folder_name:'', full_path:''}
def file_to_dict(dir):
    res_list = []
    res_dict = {}
    for address, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dwp"):
                print('address = ', address)
                print('file = ', file)
                # print(address+'/'+file)                   # первый вариант
                # print(os.path.join(os.getcwd(), file))    # второй вариант
                # full_path = os.path.join(os.getcwd() + '/' + address, file)
                # result.append(full_path)   # добавить полный путь
                # result.append(file)# не добавлять полный путь
                dictname = file
                dictname = {}
                dictname['filename']=file
                dictname['folder_name'] = folder(address)
                dictname['full_path'] = address
                res_list.append(dictname)
    return res_list

tmplist = file_to_dict(dir1path)
print(tmplist)

#
def folder(address):
    address = address.split('/')
    address = address[-1:2]
    return address
