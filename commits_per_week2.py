from git import Repo
from datetime import datetime
from operator import itemgetter
import time
import os
import urllib.request
import zipfile
import sys

def unzipFile(unzip_dir, zipfile_name):
    zip_file = zipfile.ZipFile(zipfile_name, 'r')
    os.mkdir(unzip_dir)
    zip_file.extractall(unzip_dir)
    zip_file.close()

YEAR = 0
WEEK = 1
DAY = 2
TIME = 3
SHA = 4
DATE = 5



repo = Repo('D:/sonarqube/projects/incubator-ariatosca')
commits = list(repo.iter_commits('master'))

commits_in_week={}
list_allweek = []
list_eachday = []
for each in commits:
    each_time = datetime.fromtimestamp(each.committed_date)
    each_date = datetime.date(each_time)
    each_hour = datetime.time(each_time)
    hash = each.hexsha
    author = each.author

#	list_eachday.append(each_date)

    list_each = [each_time.isocalendar()[YEAR], each_time.isocalendar()[WEEK], each_time.isocalendar()[DAY], each_hour, hash, each_date]
    list_allweek.append(list_each)

list_allweek.sort(key=itemgetter(YEAR, WEEK, DAY, TIME))
len_list_allweek = len(list_allweek)

list_eachday.sort(reverse=False)
for each in list_eachday:
    print(each)

i = 0


while i + 1 < len_list_allweek:
    if ((list_allweek[i][YEAR] == list_allweek[i + 1][YEAR]) and (list_allweek[i][WEEK] == list_allweek[i + 1][WEEK])):
        list_allweek.pop(i)
        len_list_allweek -= 1
    else:
        i += 1

    for each in list_allweek:
        print(each)

project_name = r'incubator-ariatosca'
file_path = r'D:\sonarqube\to_analyze' + '\\'+ project_name + r'-test'
file_name_prefix_repository = project_name + '-'
file_ext_name = r'.zip'
url_prefix = r'https://github.com/apache/' + project_name + '/archive/'
file = open(file_path + '.bat','w')


for each in list_allweek:

#	file_name = str(counter)
#    print(each[YEAR],each[WEEK])

    file_name = str(each[SHA])
#    print(file_name)
    file_fullname = file_name + file_ext_name

    dest_dir_file = os.path.join(file_path, file_fullname)
#    print(dest_dir_file)

#    if not os.path.exists(dest_dir_file):
#        os.makedirs(dest_dir_file)

    download_url = url_prefix + each[SHA] + file_ext_name


  #  print(download_url)


    urllib.request.urlretrieve(download_url, dest_dir_file)
    unzip_dirpath = os.path.join(file_path, file_name)
    unzipFile(unzip_dirpath, dest_dir_file)

    old_dirpath = os.path.join(file_path, file_name) + '\\' + file_name_prefix_repository + each[SHA]

    new_dirpath = os.path.join(file_path, file_name) + '\\' + project_name

    os.renames(old_dirpath, new_dirpath)

    file.write(r'call' + r' ' + r'cd' + r' ' + unzip_dirpath + '\n')
#    file.write(r'call' + r' ' + r'sonar-scanner -D sonar.projectKey=cloudstack-documentation -D sonar.projectName=cloudstack-documentation -D sonar.projectVersion=' + str(each[SHA]) + r' ' + r'-D sonar.sources=. -D sonar.language=py -D sonar.projectDate='+ str(each[DATE]) + r' ' + r'-D sonar.host.url=http://localhost:9000' + '\n')
    file.write(r'call' + r' ' + r'sonar-scanner -D sonar.projectKey=' + str(project_name) + r' ' + r'-D sonar.projectName=' + str(project_name) + r' ' + r'-D sonar.projectVersion=' + str(each[SHA]) + r' ' + r'-D sonar.sources=. -D sonar.language=py -D sonar.projectDate='+ str(each[DATE]) + r' ' + r'-D sonar.host.url=http://localhost:9000' + '\n')
    file.write(r'call' + r' ' + r'cd..' + '\n')


file.close();