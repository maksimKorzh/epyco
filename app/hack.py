import os

'''
This module forwards linux bash commands "ls", "cat", "touch", "rm" and "mkdir"
to the "https://maksimkorzh.pythonanywhere.com/" python environment

create instance: hack = HackingAround()
'''

def getcwd():
    '''
    Prints current working directory to console
    usage: hack.getcwd()
    '''
    print(os.getcwd())

def ls(path):
    '''
    Prints "ls" command output at given path
    args: path, e.g. '' - empty to "ls" cwd, './GUEST' - to ls "GUEST" folder files
    usage: hack.ls('') | hack.ls('./GUEST')
    '''
    
    os.system('ls ' + path+ ' -a > ls.txt')
    ls = ''
    
    with open('ls.txt', 'r') as f:
        for line in f.read():
            ls += line
    
    print(ls)

def cat(path):
    '''
    Prints file content to console
    args: path, e.g. 'ls.txt' - file in cwd | './GUEST/bass.csv'
    usage: hack.cat('ls.txt') | hack.cat('./GUEST/bass.csv')
    '''
    
    content = ''
    
    with open(path, 'r') as f:
        for line in f.read():
            content += line
    
    print(content)

def touch(path, content):
    '''
    Creates file at given path filling with a given content
    args: path, content, e.g. './YOURFOLDER/yourfile', 'your content'
    usage: hack.touch('yourfile.txt', 'hello') // writes "hello" to "yourfile"
    '''
    
    with open(path, 'w') as f:
        f.write(content)

def rm(path):
    '''
    Removes file from the given path
    args: path
    usage: hack.rm('yourfile.txt') - removes file "yourfile.txt" | hack.rm('-r YOURDIR') - removes "YOURDIR" directory
    '''
    
    os.system('rm ' + path)

def mkdir(name):
    '''
    Creates directory at given path
    args: path
    usage: hack.mkdir('YOURDIR') | hack.mkdir('./YOURDIR/SUBDIR') - creates "SUBDIR" directory in "YOURDIR" assuming YOURDIR exiscts
    '''
    
    os.system('mkdir ' + name)
