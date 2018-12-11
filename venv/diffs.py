import os
import re

dir2017 = '/media/user/Work/temp/2017/'
dir2018 = '/media/user/Work/temp/2018/Ресурс/'

BASEDIR = '/media/user/Work/temp/'
REG = r'^[2-9][0-9]\.[0-9]{2}\:'

def show_dirs():  # return dirs appended in list
    dirs_list = []
    for item in os.scandir():
        if item.is_dir():
            dirs_list.append(item.name)
            dirs_list.sort()
    # print(dirs_list)
    return dirs_list

def chdir(dir):
    try:
        os.chdir(dir)
        print('\nПерешел в {}'.format(dir))
    except FileNotFoundError:
        print('\nТакой папки не существует\n')

# get all dwp files in dir, also add path to file
def get_files_list_full_path(dir):
    ########  список файлов с путем
    result = []
    for address, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dwp"):
                # print(address+'/'+file)                   # первый вариант
                # print(os.path.join(os.getcwd(), file))    # второй вариант

                full_path = os.path.join(os.getcwd() + '/' + address, file)
                # print(os.path.join(os.getcwd()+'/'+address,file))
                result.append(full_path)
    return result


def get_files_list(dir):
    result = []
    for address, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".dwp"):
                # print(address+'/'+file)                   # первый вариант
                # print(os.path.join(os.getcwd(), file))    # второй вариант
                # full_path = os.path.join(os.getcwd() + '/' + address, file)
                # result.append(full_path)   # добавить полный путь
                result.append(file)# не добавлять полный путь
    return result


def get_file_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        alist = []
        for line in file:
            # alist.append(line)
            if re.match(REG, line):
                alist.append(line)
        return alist

# compare two files and show diffs
def show_diffs(file1, file2):
        l1 = len(file1)
        for i in range(l1):
            if file1[i] != file2[i]:
                # tmp_file.write(file1[i])
                # tmp_file.write(file2[i])
                print(file1[i])

def write_diffs():
    with open('tmp', 'w', encoding='utf-8') as tmp_file:
        l1 = len(file1)
        for i in range(l1):
            if file1[i] != file2[i]:
                tmp_file.write(file1[i])
                tmp_file.write(file2[i])




chdir(dir2017)                                              # go to main dir
cabs_list = show_dirs()                                     # get list of cabinets
# files_in_cabinet_full_path=get_files_list(cabs_list[0])     # get all dwp files in dir, also add path to file
# files_names_in_cabinet=get_files_list(cabs_list[0])
# print(files_names_in_cabinet,sep='\n')


cab1=cabs_list[1]                                   # first cabinet folder
# files1=get_files_list(cab1)                         # create list with filenames
print('cab1 = ',cab1)
os.chdir(dir2017+cab1)                              # enter to this folder
# file1=os.getcwd()+'/'+files1[0]                   #
file1_path=get_files_list_full_path(cab1)[0]             # get full path for file1
print('file1_path = ', file1_path)
# ========================================== ^ code for file1
# ========================================== v code for file2
chdir(dir2018)
cabs_list2 = show_dirs()
print('cabs_count1 = ', len(cabs_list), 'cabs_count2 = ', len(cabs_list2))

print('[cabs list1]', cabs_list)
print('[cabs_list2]', cabs_list2)


cab2=cabs_list2[1]
print('cab2 = ', cab2)
os.chdir(dir2018+cab2)
print('cwd = ', os.getcwd())
print('os.join', os.path.join(os.getcwd()))
file2_path=get_files_list_full_path(cab2)[0]
print('file2_path = ', file2_path)

file1 = get_file_data(file1_path)
file2 = get_file_data(file2_path)


# название папки, название файла, потом разницу
def create_diffs_file(file1, file2, cabname, diff_file_path):
    print('diff_file_path = ', diff_file_path)
    with open(diff_file_path, 'w', encoding='utf-8') as diffs_file:
        diffs_file.write('cabname = '+cabname)
        diffs_file.write('\n')
        diffs_file.write('filename = '+file1_path)
        diffs_file.write('\n')
        diffs_file.write('filename = '+file2_path)
        diffs_file.write('\n')

        if len(file1) > len(file2):
            longest_file=file1
            print('file1>file2')
        else:
            longest_file=file2
            print('file1<file2, file1 len = {}, file2 len = {}'.format(len(file1),len(file2)))

            lines=len(longest_file)
            for line in range(lines):
                try:
                    if file1[line] != file2[line]:
                        write1 = (file1[line])
                        write2 = (file2[line])
                        print('write1', write1)
                        print(write2)
                        # diffs_file.write(file1[line])
                        # diffs_file.write(file2[line])
                        diffs_file.write(write1)
                        diffs_file.write(write2)
                        diffs_file.writable('\n')
                except IndexError:
                    print('index error')
                    # diffs_file.write(file2[i])


diff_file_path=dir2017+'DIFF'+cab1+'.txt'

create_diffs_file(file1,file2,cab1,diff_file_path)



# *** shiny *** #
# for cabinet in cabs_list:
#     print(cabinet)
#     for file in get_files_list(cabinet):
#         print(file)
# *** end of shiny *** #