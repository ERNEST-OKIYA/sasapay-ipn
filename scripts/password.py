import base64
import hashlib
import subprocess


InitiatorPassword = 'Jijenge%2021.'
PUBLIC_CERT_PATH='/home/josh/lab/projects/qb.ipn/scripts/cert.cer'

def encrypt_initiator_password_php(cert_path,password):
    """ encrypt initiator password but use php"""
    command="php /home/josh/lab/projects/qb.ipn/scripts/encrypt.php %s %s"%(cert_path,password)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    encrypted=proc.stdout.read()
    return (encrypted).decode()

cert=encrypt_initiator_password_php(PUBLIC_CERT_PATH,InitiatorPassword)
print(cert)
