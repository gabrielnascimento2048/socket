#Cliente TCP
import socket
import rsa
from threading import Thread

# Endereco da chave publica
nome_arq_chave_pub = 'Pub.txt'
#Endereco da chave privada
nome_arq_chave_pri = 'Pri.txt'

#Abre o arquivo com a chave
arq_chave_pub = open(nome_arq_chave_pub, 'r')
arq_chave_pri = open(nome_arq_chave_pri, 'r')

#Carrega a chave PUBLICA
txt_chave_pub = ''
for linha in arq_chave_pub:
   txt_chave_pub = txt_chave_pub + linha
arq_chave_pub.close()
#carrega a chave PRIVADA
txt_chave_pri = ''
for linha in arq_chave_pri:
   txt_chave_pri = txt_chave_pri + linha
arq_chave_pri.close()

#decodifica para o formato expoente e modulo
chave_pub = rsa.PublicKey.load_pkcs1(txt_chave_pub, format='PEM')
chave_pri = rsa.PrivateKey.load_pkcs1(txt_chave_pri, format='PEM')
#envia a mensagem
def conexao_envia(tcp):
    msg_enviada = None
    while msg_enviada <> '\x18':
        if msg_enviada:
            # cifra a msg_enviada
            msg_enviada_criptografada = rsa.encrypt(msg_enviada, chave_pub)
            tcp.send(msg_enviada_criptografada)
        msg_enviada = raw_input()
    tcp.close()
#carrega msg descrip
def conexao_recebe(tcp):
    while True:
        msg_recebida = tcp.recv(1024)
        if msg_recebida:
            print('criptografada: ' + msg_recebida + '\n')
            # Decifra a msg_recebida
            msg_recebida_descriptografada = rsa.decrypt(msg_recebida, chave_pri)
            print('descriptografada: ' + msg_recebida_descriptografada + '\n')
    tcp.close()

#Endereco IP do Servidor
SERVER = '127.0.0.1'
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (SERVER, PORT)
tcp.connect(dest)

print('Para sair use CTRL+X\n')

tr = Thread(target=conexao_recebe, args=[tcp])
tr.start()
te = Thread(target=conexao_envia, args=[tcp])
te.start()
