import os
def rename(path):
    filelist = os.listdir(path)
    for files in filelist:
        Olddir = os.path.join(path, files)
        if os.path.isdir(Olddir):
            rename(Olddir)
            continue
        f,p = os.path.splitext(files)
        f1,p1 = os.path.splitext(f)
        Newdir = os.path.join(path, f1 + '.your_ext') 
        os.rename(Olddir, Newdir)

if __name__ == "__main__":
    path = '/to/your/path' 
    rename(path)
