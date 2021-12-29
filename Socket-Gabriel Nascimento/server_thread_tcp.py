#Servidor TCP
import socket
from threading import Thread
import rsa

#Endereco da chave privada
nome_arq_chave_pri = 'Pri.txt'
#Endereco da chave publica
nome_arq_chave_pub = 'Pub.txt'

#abre o arquivo com a chave
arq_chave_pri = open(nome_arq_chave_pri, 'r')
arq_chave_pub = open(nome_arq_chave_pub, 'r')

#Carrega a chave em uma variavel
txt_chave_pri = ''
for linha in arq_chave_pri:
   txt_chave_pri = txt_chave_pri + linha
arq_chave_pri.close()

txt_chave_pub = ''
for linha in arq_chave_pub:
   txt_chave_pub = txt_chave_pub + linha
arq_chave_pub.close()

#decodifica para o formato expoente e modulo
chave_pri = rsa.PrivateKey.load_pkcs1(txt_chave_pri, format='PEM')
chave_pub = rsa.PublicKey.load_pkcs1(txt_chave_pub, format='PEM')
 
def conexao_recebe(con, cli):
    while True:
        msg_recebida = con.recv(1024)
        if not msg_recebida:
            break
        print('criptografada:' + msg_recebida + '\n')
        msg_recebida_descriptografada = rsa.decrypt(msg_recebida, chave_pri)
        print('descriptografada: ' + msg_recebida_descriptografada + '\n')
    print('Finalizando conexao do cliente', cli)
    con.close()

def conexao_envia(con, cli):
    msg_enviada = None
    while msg_enviada <> '\x18':
        if msg_enviada:
            # Cifra a msg_enviada
            msg_enviada_criptografada = rsa.encrypt(msg_enviada, chave_pub)
            con.send(msg_enviada_criptografada)
        msg_enviada = raw_input()
    print('Finalizando conexao do cliente', cli)
    con.close() 

#Endereco IP do Servidor
HOST_SERV = ''
#Porta que o Servidor vai escutar
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig_serv = (HOST_SERV, PORT)
tcp.bind(orig_serv)
tcp.listen(1)
while True:
    con, cliente = tcp.accept()
    print('Conectado por ', cliente)
    tr = Thread(target=conexao_recebe, args=[con, cliente])
    tr.start()
    print('Para sair use CTRL+X\n')
    te = Thread(target=conexao_envia, args=[con, cliente])
    te.start()
