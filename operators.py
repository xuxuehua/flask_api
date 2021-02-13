import subprocess

query_port = 'firewall-cmd --permanent --add-port={src_port}/tcp'
add_port = '''
firewall-cmd --permanent --add-masquerade
firewall-cmd --permanent --add-port={src_port}/tcp
firewall-cmd --permanent --add-port={src_port}/udp
firewall-cmd --permanent --add-forward-port=port={src_port}:proto=tcp:toaddr={ip}:toport={dest_port}
firewall-cmd --permanent --add-forward-port=port={src_port}:proto=udp:toaddr={ip}:toport={dest_port}
'''

remove_port = '''
firewall-cmd --permanent --remove-port={src_port}/tcp
firewall-cmd --permanent --remove-port={src_port}/udp
firewall-cmd --permanent --remove-forward-port=port={src_port}:proto=tcp:toaddr={ip}:toport={dest_port}
firewall-cmd --permanent --remove-forward-port=port={src_port}:proto=udp:toaddr={ip}:toport={dest_port}
'''

reload_service = 'firewall-cmd --reload'


subprocess.call('ls -l', shell=True)


def firewalld_configuration(ip, src_port, dest_port):
    env = {
        'ip': ip,
        'src_port': src_port,
        'dest_port': dest_port
    }
    ret = subprocess.call(query_port.format(**env), shell=True)
    if ret == 0:
        subprocess.call(remove_port.format(**env), shell=True)
        subprocess.call(add_port.format(**env), shell=True)
        subprocess.call(reload_service, shell=True)
    else:
        subprocess.call(add_port.format(**env), shell=True)
        subprocess.call(reload_service, shell=True)
