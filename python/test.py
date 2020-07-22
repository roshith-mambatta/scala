#!/usr/bin/python

import subprocess
import shutil
import os
import git
import stat
import paramiko
import csv
from os import path

mydir="/your"
for root, dirs, files in os.walk(mydir):
    for dir in dirs:
        os.chmod(path.join(root, dir), stat.S_IRWXU)
    for file in files:
        os.chmod(path.join(root, file), stat.S_IRWXU)

try:
    shutil.rmtree(mydir)
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))

git.Repo.clone_from('https://github.com/roshith-mambatta/demo-project.git',
                        '/your/repo/dir/',
                        branch='master')  #


def call_win_batch(gitUrl,localGitPath):
    subprocess.call([r'C:\00_MyDrive\ccm_packager\run.bat', 'test'])
    print("Git cloned")

def git_clone(gitUrl,localGitPath):
    print("Git cloned")

def remote_transfer_files(method,sshClient,remotefilepath,localfilepath):
    if (method=="get"):
        ftp_client = sshClient.open_sftp()
        ftp_client.get(remotefilepath, localfilepath)
        ftp_client.close()
    else:
        ftp_client = sshClient.open_sftp()
        ftp_client.put(localfilepath, remotefilepath)
        ftp_client.close()

def run_batchOnCCMServer(appCode,pubFile):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("test.ccm.server.com", username=username, password=password)
    remote_transfer_files('put', "test.ccm.server.com", '', inputPath)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    remote_transfer_files('get', "test.ccm.server.com", '', inputPath)

def gen_report(mode,testCase):
    if mode=="batch":
        run_batchOnCCMServer()
    else:
        call_win_batch()

def compare_output():
    call_win_batch()

# main metthod

#initial content
with open('/your/testReport.csv','w') as f:
    f.write('appCode,testCase,testCaseDesc,status,errorDesc\n') # TRAILING NEWLINE

git_clone()

appCodes=[]

for appCode in appCodes:
    # Read test cases and loop # Read  xml to json
    testCases = []
    for testCase in testCases:
        try:
            gen_report()
            compare_output()
            with open('/your/testReport.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ADV', 'TC1', 'Test Case Description', 'SUCCESS', ''])
        except:
            print("Oops!")
