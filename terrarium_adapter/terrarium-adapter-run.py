# script to be built with nuitka
import terrarium_adapter  
import subprocess

# Тестирование адаптера. Запуск «террариумных и внетеррариумных бинарников»
# Для проверки на виртуалках внешних систем
# Включая компиляцию с нуиткой.

for cmds_ in [
        ('start-compton',),    
    ]:
    print('*'*20, ' '.join(cmds_) + ':\n')
    try:
    # if 1:
        subprocess.run(cmds_)
    except Exception as ex_:
        print('Failed to run!')

for cmds_ in [
        ('/vagrant/out-debug/ebin/start-compton',),    
        ('/usr/bin/xdg-user-dir',),
        ('ls', '-l', '/'),
        ('uname', '-a'),
        ('gsettings', '--version'),
        ('compton', '--version'),
        ('gs', '-v'),
        ('python3.8', '-V'),
            ]:
    print('*'*20, ' '.join(cmds_) + ':\n')
    try:
    # if 1:
        print('*'*20, ' '.join(cmds_) + ':\n')
        ls = subprocess.check_output(cmds_)
        print(ls)
    except Exception as ex_:
        print('Failed to run!')
    print('-'*20)

