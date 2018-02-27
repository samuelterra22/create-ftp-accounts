import os
import os.path
import time
from shutil import copyfile


def change_vsftpd_file(vsftpd_conf_path='/etc/vsftpd.conf'):
    # cria backup do arquivo
    create_backup(vsftpd_conf_path)

    chroot_changed = False

    file = open(vsftpd_conf_path, 'r')
    saida = ''
    for line in file:
        if 'write_enable' in line and '_write_enable' not in line:
            saida += 'write_enable=YES\n'

        # so aplica essa modificacao se o for informado um diretorio diferente de vazio
        elif 'chroot_local_user=' in line and not chroot_changed:
            saida += '\nchroot_local_user=YES\n'
            # saida += 'user_sub_token='+user+'\n'
            # saida += 'local_root= ' + user_directory + '\n\n'
            chroot_changed = True

        elif 'ssl_enable=' in line:
            saida += 'ssl_enable=YES\n'

        else:
            saida += line

    file.close()

    # apaga o arquivo antigo
    os.remove(vsftpd_conf_path)

    # escreve o novo de acordo com as modificacoes
    open(vsftpd_conf_path, 'w').write(saida)


def change_ssh_port(path='/etc/ssh/sshd_config', port='2510'):
    # cria backup do arquivo
    create_backup(path)

    file = open(path, 'r')
    saida = ''
    for line in file:
        if 'Port ' in line:
            saida += 'Port ' + str(port) + '\n'
        else:
            saida += line

    file.close()

    # apaga o arquivo antigo
    os.remove(path)

    # escreve o novo de acordo com as modificacoes
    open(path, 'w').write(saida)


def create_backup(file_path):
    backup_pattern = '-' + str(time.strftime("%X"))
    backup = file_path + backup_pattern
    copyfile(file_path, backup)


# change_ssh_port('sshd_config', '2510')
# change_vsftpd_file('vsftpd.conf', '~/mydomain.com')

user_name = input('Choose username:\t')
user_password = input('Choose password for \'' + user_name + '\':\t')
user_folder = input('Choose folder name for \'' + user_name + '\' (folder will be created if it does not exist.):\t')

print('Updating system...')
os.system("sudo apt-get update")

print('Upgrading system dependencies...')
os.system("sudo apt-get dist-upgrade")

print('Installing \'vsftpd\'...')
os.system("sudo apt-get install vsftpd")

print('Adding user \'' + user_name + '\'...')
os.system("sudo useradd " + user_name)

print('Adding group \'' + user_name + '\'...')
os.system("sudo groupadd " + user_name)

print('Setting password for user...')
os.system("sudo passwd " + user_password)

print('Giving permissions to folders...')
os.system("sudo chown -R " + user_name + ":" + user_name + " " + user_folder)
os.system("sudo gpasswd -a " + user_name + " " + user_name)
os.system("sudo chgrp -R " + user_name + " " + user_folder)
os.system("sudo chmod -R g+rw " + user_folder)

print('Restarting vsftpd services...')
os.system("sudo systemctl restart vsftpd")

r = input('Reboot now?(s/n)')

os.system("sudo reboot now") if r.lower() == 's' else print('End of installation')
