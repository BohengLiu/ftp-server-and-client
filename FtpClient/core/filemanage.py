import os
import re

class CloudHandler():
    '''
     put all the command of file together
    '''

    def __init__(self,name,space,permission):

        self.name = name
        self.space = space
        self.permission = permission

        pardir = os.path.dirname(os.getcwd())
        homedir = os.path.join(pardir,'home',name)
        if not os.path.exists(homedir):
            os.makedirs(homedir)

        self.homedir = homedir
        self.cwd = homedir
        self.used = self.getdirsize(homedir)

    def getdirsize(self,dir):
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size

    def lsdir(self):
        return os.listdir(self.cwd)

    def chdir(self,dirname):
        # two syntax can change current workdirectory: cd dir; cd /dir1/dir2
        if '/' in dirname or '\\\\' in dirname:
            dirs = re.split('/|\\\\', dirname)
            cwd = os.path.join(self.homedir,*dirs)
            if os.path.exists(cwd):
                self.cwd = cwd
                return True
            else:
                return False
        else:
            cwd = os.path.join(self.cwd,dirname)
            if os.path.exists(cwd):
                self.cwd = cwd
                return True
            else:
                return False

    def rename(self,oldname,newname):
        dirs_list = self.lsdir()
        if oldname not in dirs_list:
            raise ValueError('The target file does not exists in current dir!')
        if newname in dirs_list:
            raise ValueError('The new filename has existed!')
        oldpath = os.path.join(self.cwd,oldname)
        newpath = os.path.join(self.cwd,newname)
        os.rename(oldpath,newpath)
        return True

    def create_dir(self,name):
        dirs_list = self.lsdir()
        if name in dirs_list:
            raise ValueError("The dir has existed!")
        newpath = os.path.join(self.cwd,name)
        os.mkdir(newpath)

    def delete_target(self,target):
        dirs_list = self.lsdir()
        if target not in dirs_list:
            raise ValueError("The target does not exist!")
        newpath = os.path.join(self.cwd,target)
        if os.path.isfile(newpath):
            os.remove(newpath)
        else:
            os.rmdir(newpath)
        return True

    def get_download_link(self,target):
        dirs_list = self.lsdir()
        if target not in dirs_list:
            raise ValueError("The target does not exist!")
        newpath = os.path.join(self.cwd, target)
        if os.path.isfile(newpath):
            return [os.path.join(self.cwd,target)]
        else:
            res = []
            for par,dirs,filenames in os.walk(newpath):
                for filename in filenames:
                    filepath = os.path.join(par,filename)
                    res.append(filename)
            return res

    def get_upload_dest(self,filename):
        dirs_list = self.lsdir()
        while filename in dirs_list:
            filename = filename + '(1)'
        return os.path.join(self.cwd,filename)



if __name__ == '__main__':
    c = CloudHandler('dog1',1024024,1)
    print(c.homedir,c.name,c.permission,c.space,c.used)
    c.create_dir('newdir1')
    c.create_dir('newdir2')
    print(c.lsdir())
    c.chdir('newdir1')
    c.create_dir('sondir1')
    c.create_dir('sondir2')
    c.delete_target('sondir1')
    c.rename('sondir2','newsondir2')
    print(c.get_download_link('newsondir2'))
    print(c.get_upload_dest('uploadfile'))
