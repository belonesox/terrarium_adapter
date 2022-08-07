# script to be built with nuitka
import terrarium_adapter  
import subprocess
import os

# Тестирование адаптера. Запуск «террариумных и внетеррариумных бинарников»
# Для проверки на виртуалках внешних систем
# Включая компиляцию с нуиткой.

# for cmds_ in [
#         ('start-compton',),    
#     ]:
#     print('*'*20, ' '.join(cmds_) + ':\n')
#     try:
#     # if 1:
#         subprocess.run(cmds_)
#     except Exception as ex_:
#         print('Failed to run!')

LD_LIBRARY_PATH = ''
if 'LD_LIBRARY_PATH' in os.environ: 
    LD_LIBRARY_PATH = os.environ['LD_LIBRARY_PATH'] 


print("*"*80)
print("Test 5")
print("*"*80)

os.environ['WTF_WTF'] = 'WTF_WTF'

preloadso_ = []
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

# os.environ['LD_PRELOAD_PATH'] = LIBDIR
# os.environ['LD_LIBRARY_PATH'] = ':'.join([LIBDIR, '/usr/lib64', '/usr/lib/x86_64-linux-gnu/', LD_LIBRARY_PATH])
os.environ['LD_PRELOAD']=' '.join(preloadso_)

os.posix_spawn('/lib64/ld-linux-x86-64.so.2', ['/lib64/ld-linux-x86-64.so.2', '/bin/bash', '/vagrant/out/ebin/set-for-dmprinter'], dict(os.environ))


print("*"*80)
print( "2222--06 "*4)
print("*"*80)


for cmds_ in [
         '/vagrant/out/ebin/set-for-dmprinter',    
        ]:
    ls = subprocess.check_output(['/bin/bash', cmds_], shell=False, env=dict(os.environ))
    print(ls)


# for cmds_ in [
#         ('/vagrant/out/ebin/set-for-dmprinter',),    
# #        ('/vagrant/out-debug/ebin/start-compton',),    
# #        ('/usr/bin/xdg-user-dir',),
#         ('ls', '-l', '/'),
#         ('uname', '-a'),
#         ('gsettings', '--version'),
# #        ('compton', '--version'),
#         ('gs', '-v'),
#         ('python3', '-V'),
#             ]:
#     print('*'*20, ' '.join(cmds_) + ':\n')
#     try:
#     # if 1:
#         print('*'*20, ' '.join(cmds_) + ':\n')
#         ls = subprocess.check_output(cmds_)
#         print(ls)
#     except Exception as ex_:
#         print('Failed to run!')
#     print('-'*20)

