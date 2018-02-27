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


def change_proftpd_file(proftpd_conf_path='/etc/proftpd/proftpd.conf', group=''):
    # cria backup do arquivo
    create_backup(proftpd_conf_path)

    file = open(proftpd_conf_path, 'r')
    saida = ''
    for line in file:
        if 'DefaultRoot' in line and '~' in line:
            saida += 'DefaultRoot                     ~ ' + group + ', !staff'

        else:
            saida += line

    file.close()

    # apaga o arquivo antigo
    os.remove(proftpd_conf_path)

    # escreve o novo de acordo com as modificacoes
    open(proftpd_conf_path, 'w').write(saida)


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
    backup_pattern = '-' + str(time.strftime('%X'))
    backup = file_path + backup_pattern
    copyfile(file_path, backup)


# FTP_GROUP = 'ftpaccess'

user_name = input('[?] Choose username:\t')
user_folder = input(
    '[?] Choose folder name for \'' + user_name + '\' (folder will be created if it does not exist.):\t')
ssh_port = input('[?] Choose ssh port:\t')

print('[!] Summary:')
print('\t[>] Username:' + user_name)
print('\t[>] User password: You will choose.')
print('\t[>] User folder:' + user_folder)
print('\t[>] SSH Port:' + ssh_port)
print('\t[>] \'proftpd\' will be installed.')

c = input('Continue? (y/n)')

exit(-1) if c.lower() == 'n' else print('Continuing installation!')

print('[-] Updating system...')
os.system('sudo apt-get update')

print('[-] Upgrading system dependencies...')
os.system('sudo apt-get -y dist-upgrade')
os.system('sudo apt-get -y autoremove')
os.system('sudo apt-get -y autoclean')

# print('[-] Installing \'proftpd\'...')
# os.system('sudo apt-get -y install proftpd')

print('[-] Installing \'vsftpd\'...')
os.system('sudo apt-get -y install vsftpd')

print('[-] Changing ssh port...')
change_ssh_port(port=str(ssh_port))

# print('[-] Changing proftpd file...')
# change_proftpd_file(group=FTP_GROUP)

print('[-] Changing vsftpd file...')
change_vsftpd_file()

print('[-] Adding user \'' + user_name + '\'...')
os.system('sudo useradd -s /bin/false ' + user_name)

print('[-] Setting password for user...')
os.system('sudo passwd ' + user_name)

print('[-] Creating user folder...')
os.system('sudo mkdir -p ' + user_folder)

print('[-] Giving permissions to folders...')
os.system('sudo chown -R ' + user_name + ':' + user_name + ' ' + user_folder)
os.system('sudo gpasswd -a ' + user_name + ' ' + user_name)
os.system('sudo chgrp -R ' + user_name + ' ' + user_folder)
os.system('sudo chmod -R g+rw ' + user_folder)
os.system('sudo usermod -d ' + user_folder + ' ' + user_name)

print('[-] Restarting proftpd services...')
os.system('sudo service proftpd restart')

print('[-] Restarting ssh services...')
os.system('sudo service sshd restart')

r = input('Reboot now?(y/n)')

os.system('sudo reboot now') if r.lower() == 's' else print('End of installation')
