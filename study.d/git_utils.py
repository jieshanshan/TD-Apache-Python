from git import Repo
from datetime import datetime
from operator import itemgetter
import os
import shutil
import urllib.request
import zipfile


def unzip_file(unzip_dir, zipfile_name):
	zip_file = zipfile.ZipFile(zipfile_name, 'r')
	os.mkdir(unzip_dir)
	zip_file.extractall(unzip_dir)
	zip_file.close()

def download_repo(user, project, dst_path):
    ghurl = f'https://github.com/{user}/{project}'
    print(f'Cloning {user}/{project}')
    try:
        Repo.clone_from(ghurl, dst_path)
    except:
        print(f'ERROR: {user}/{project}')

def download_weekly_commits(user, project, repo_local_path, branch_name, dst_folder):
    YEAR = 0
    WEEK = 1
    DAY = 2
    TIME = 3
    SHA = 4

    repo = Repo(repo_local_path)
    commits = list(repo.iter_commits(branch_name))

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

    proj_path = os.path.join(dst_folder,user,project)
    url_prefix = f'https://github.com/{user}/{project}/archive'
    counter = 1

    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
    
    file = open(os.path.join(proj_path,f'{project}.sh'),'w+')

    for idx, each in enumerate(list_allweek):
        
        print(f'Processing {project}({idx+1}/{len(list_allweek)}): commit {each[SHA]}')
        
        commit_url = f'{url_prefix}/{each[SHA]}.zip'
        commit_dir = os.path.join(proj_path, str(counter))
        commit_zip = f'{commit_dir}.zip'
        
        file.write('/home/sonar/study.d/vendor/sonar-scanner/bin/sonar-scanner'
                  f' -D sonar.projectKey={project}'
                  f' -D sonar.projectName={project}'
                  f' -D sonar.projectVersion={str(counter)}'
                  f' -D sonar.sources={commit_dir}'
                   ' -D sonar.host.url=http://sonarqube:9000\n')
        
        counter += 1
        
        # SKIP - commit downloaded already
        if os.path.isdir(commit_dir) and not os.path.exists(commit_zip):
            continue
        
        # Delete remainings of unsuccessful download
        if os.path.isdir(commit_dir):
            shutil.rmtree(commit_dir)
        if os.path.exists(commit_zip):
            os.remove(commit_zip)

        # Download commit
        urllib.request.urlretrieve(commit_url, commit_zip)
        unzip_file(commit_dir, commit_zip)
        os.remove(commit_zip)

    file.close();
