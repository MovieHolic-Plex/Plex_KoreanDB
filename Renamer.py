from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

# 데이터베이스 주소. (변경하지 마세요)
github_link = r'https://raw.githubusercontent.com/MovieHolic-Plex/Plex_KoreanDB/master/Names'

# 이름이 바뀔 컨텐츠들이 있는 폴더들. 하위 폴더까지 검색함.
Target_Folders = [r'E:\test1' , r'E:\test2' , r'E:\test3']

# 변경하지 않을 확장자. 해당 확장자의 파일은 이름을 변경하지 않는다.
exc_nope = ['!qb', '!bt', 'exe']

database = str(BeautifulSoup(urlopen(github_link), "html.parser")).split('\n')
names_list_before = []
names_list_after = []
for part in database:
    if part.count(r'==&gt;==') == 0 :
        continue
    try:
        names_list_before.append(part.split(r'==&gt;==')[0].strip())
        names_list_after.append(part.split(r'==&gt;==')[1].strip())
    except IndexError:
        pass


def Folder_Check(dir):
    files = os.listdir(dir)
    for file in files:
        fullFilename = os.path.join(dir, file)
        if os.path.isdir(fullFilename) == True:
            Folder_Check(fullFilename)
        else:
            ext = os.path.splitext(fullFilename)[1].replace('.','').lower()
            if ext in exc_nope:
                # 확장자 exclude
                continue
            for name in names_list_before:
                if file.count(name) > 0:
                    try:
                        idx = names_list_before.index(name)
                        replace_name = names_list_after[idx]
                        filename_after = file.replace(name, replace_name)
                        os.renames(fullFilename, os.path.join(dir, filename_after))
                        print(fullFilename, '\nto',os.path.join(dir, filename_after),'\n')
                    except:
                        print(fullFilename, '이름 변경 실패')




for dir in Target_Folders:
    Folder_Check(dir)
