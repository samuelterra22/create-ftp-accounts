import os.path
import os 
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


os.system("passwd bruno")
