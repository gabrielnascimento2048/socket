#!/usr/bin/python2
import socket
import rsa
from threading import Thread
import tornado.web
import tornado.websocket
import tornado.ioloop

from tornado.options import define, options, parse_command_line
define("port", default=8888, help="run on the given port", type=int) 
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
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("repete.html")
  def conexao_envia(tcp):
    msg_enviada = None
    while msg_enviada <> '\x18':
        if msg_enviada:
            # cifra a msg_enviada
            msg_enviada_criptografada = rsa.encrypt(msg_enviada, chave_pub)
            tcp.send(msg_enviada_criptografada)
        msg_enviada = raw_input()
    tcp.close()         
 ##
app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/websocket", WebSocketHandler),
])
 
if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
