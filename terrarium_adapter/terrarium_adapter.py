"""Main module."""

import sys
import os
import subprocess
import shutil  
import time  

original_open = subprocess.Popen

def  our_popen(scmd):
    print('Fake!!!')
    pass

preloadso_ = []          
LIBDIR = '/lib/x86_64-linux-gnu'  
ok_ = False
for LIBDIR in ['/lib64', '/lib/x86_64-linux-gnu', '/lib']:
    if os.path.exists(LIBDIR):
        for file_ in os.listdir(LIBDIR):
            filep_ = os.path.join(LIBDIR, file_)
            # print(file_)
            if '.so' in file_ and not os.path.islink(filep_) and not 'libthread_db' in file_ and os.path.getsize(filep_)>1024:
                okl_ = False
                # for start_ in ['lib']:
                for start_ in ['libc-', 'libdl-', 'libcap']:
                    okl_ = okl_ or file_.startswith(start_)
                    if okl_:
                        break
                if okl_:            
                    preloadso_.append(filep_)
                    ok_ = True    
    if ok_:
        break                

LDSO_HOST = ''
for p_ in ['/lib64/ld-linux-x86-64.so.2']:
    if os.path.exists(p_):
        LDSO_HOST = p_     
        break

LD_LIBRARY_PATH = ''
if 'LD_LIBRARY_PATH' in os.environ: 
    LD_LIBRARY_PATH = os.environ['LD_LIBRARY_PATH'] 

root_dir = None
dirs_ = ['ebin', 'pbin']
for dir_name in dirs_:
    if dir_name in sys.executable:
        root_dir = sys.executable.split(dir_name)[0]
        break
    if dir_name in sys.argv[0]:
        root_dir = sys.argv[0].split(dir_name)[0]
        break


class TerraPopen(subprocess.Popen):
    """ Execute a child program in a new process.

    For a complete description of the arguments see the Python documentation.

    Arguments:
      args: A string, or a sequence of program arguments.

      bufsize: supplied as the buffering argument to the open() function when
          creating the stdin/stdout/stderr pipe file objects

      executable: A replacement program to execute.

      stdin, stdout and stderr: These specify the executed programs' standard
          input, standard output and standard error file handles, respectively.

      preexec_fn: (POSIX only) An object to be called in the child process
          just before the child is executed.

      close_fds: Controls closing or inheriting of file descriptors.

      shell: If true, the command will be executed through the shell.

      cwd: Sets the current directory before the child is executed.

      env: Defines the environment variables for the new process.

      text: If true, decode stdin, stdout and stderr using the given encoding
          (if set) or the system default otherwise.

      universal_newlines: Alias of text, provided for backwards compatibility.

      startupinfo and creationflags (Windows only)

      restore_signals (POSIX only)

      start_new_session (POSIX only)

      pass_fds (POSIX only)

      encoding and errors: Text mode encoding and error handling to use for
          file objects stdin, stdout and stderr.

    Attributes:
        stdin, stdout, stderr, pid, returncode
    """
    _child_created = False  # Set here since __del__ checks it

    def __init__(self, args, **kwargs):
        args_ = None
        args_is_str = isinstance(args, str)
        # print("@"*10, args)
        if args_is_str:
            args_ = list(args.split())
        else:    
            args_ = list(args)
        # print("+"*10, args_)

        if root_dir:
            ldso = os.path.join(root_dir, 'pbin', 'ld.so')
            utterms_ = os.path.split(args_[0])
            # print(utterms_)
            utname = utterms_[-1]
            pbin_path = os.path.join(root_dir, 'pbin', utname)
            ebin_path = os.path.join(root_dir, 'ebin', utname)
            os.environ['LD_PRELOAD'] = ''
            os.environ['LD_PRELOAD_PATH'] = ''
            os.environ['LD_LIBRARY_PATH'] = LD_LIBRARY_PATH
            if os.path.exists(pbin_path):
                args_[0] = pbin_path
            else:
                # Here we should 
                if utterms_[0] == '':
                    if os.path.exists(ebin_path):
                        args_[0] = ebin_path
                    else:    
                        utname_ = shutil.which(utname)
                        # print(utname, '*'*20, utname_)
                        if utname_:
                            args_[0] = utname_

                header = open(args_[0], "rb").read(32)     
                if not b'ELF' in header:
                    interpreter = '/bin/sh'
                    shebang_start = b'#!'
                    if header.startswith(shebang_start):
                        headerline = header.split(b'\n')[0][len(shebang_start):]
                        for terms_ in reversed(headerline.split()):
                            args_.insert(0, terms_)    
                    else:    
                        args_.insert(0, interpreter)    
                ldso = LDSO_HOST     
                os.environ['LD_PRELOAD_PATH'] = LIBDIR
                os.environ['LD_LIBRARY_PATH'] = ';'.join([LIBDIR, '/usr/lib64', '/usr/lib/x86_64-linux-gnu/', LD_LIBRARY_PATH])
                os.environ['LD_PRELOAD']=' '.join(preloadso_)
                # print("os.environ['LD_PRELOAD']", os.environ['LD_PRELOAD'])
                # print("os.environ['LD_PRELOAD_PATH']", os.environ['LD_PRELOAD_PATH'])
                # print('*****')
            # args_.insert(0, '/bin/sh')    
            args_.insert(0, ldso)    

        # time.sleep(5)
        # print("!"*10, args_)
        if args_is_str:
            args_ = " ".join(args_)

        super().__init__(args_, **kwargs)
        pass


subprocess.Popen=TerraPopen
