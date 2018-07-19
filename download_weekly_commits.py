from git import Repo
from datetime import datetime
from operator import itemgetter
import os
import urllib.request
import zipfile

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

repo = Repo('D:/sonarqube/incubator-mxnet')
commits = list(repo.iter_commits('master'))

commits_in_week={}
list_allweek = []
for each in commits:
	each_time = datetime.fromtimestamp(each.committed_date)
	each_date = datetime.date(each_time)
	each_hour = datetime.time(each_time)
	hash = each.hexsha

	list_each = [each_time.isocalendar()[YEAR], each_time.isocalendar()[WEEK], each_time.isocalendar()[DAY], each_hour, hash]
	list_allweek.append(list_each)

list_allweek.sort(key=itemgetter(YEAR, WEEK, DAY, TIME))
len_list_allweek = len(list_allweek)
i = 0

while i + 1 < len_list_allweek:
	if ((list_allweek[i][YEAR] == list_allweek[i + 1][YEAR]) and (list_allweek[i][WEEK] == list_allweek[i + 1][WEEK])):
		list_allweek.pop(i)
		len_list_allweek -= 1
	else:
		i += 1

for each in list_allweek:
    print(each)

file_path = r'D:\sonarqube\to_analyze\incubator-mxnet-test'
file_name_prefix_repository = r'incubator-mxnet-'
file_ext_name = r'.zip'
url_prefix = r'https://github.com/apache/incubator-mxnet/archive/'
counter = 1

file = open(r'D:\sonarqube\to_analyze\incubator-mxnet-test' + '.bat','w')

for each in list_allweek:

	file_name = str(counter)
	file_fullname = file_name + file_ext_name
	dest_dir_file = os.path.join(file_path, file_fullname)
	print(dest_dir_file)

	download_url = url_prefix + each[SHA] + file_ext_name
	print(download_url)
	urllib.request.urlretrieve(download_url, dest_dir_file)

	unzip_dirpath = os.path.join(file_path, file_name)
	unzipFile(unzip_dirpath, dest_dir_file)

	file.write(r'call' + r' ' + r'cd' + r' ' + unzip_dirpath + '\n')
	file.write(r'call' + r' ' + r'sonar-scanner -D sonar.projectKey=incubator-mxnet -D sonar.projectName=incubator-mxnet -D sonar.projectVersion=' + str(counter) + r' ' + r'-D sonar.sources=.' + r' ' + r'-D sonar.host.url=http://localhost:9000' + '\n')
	file.write(r'call' + r' ' + r'cd..' + '\n')

	counter += 1

file.close();
