#!/usr/bin/python
# -*- coding: utf-8 -*-

##################################################################################
# Script criado para encontrar padrões cd Cartão de Crédito nos arquivos         #
# Do HD e notificar por e-mail, o arquivo e a linha que o pattern foi encontrado #
#           Autor: Matheus Fidelis <@fidelissauro>  <16/12/2016>                 #
##################################################################################

from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib as s
import re
import os
import sys

#Configuracoes do Script
path = "/home/"
patternMasterCard = re.compile("(.+?)5[1-5][0-9]{14}(.+?)$")
patternVISA = re.compile("(.+?)4[0-9]{12}(?:[0-9]{3})?(.+?)$")
patternETC = re.compile(".*[^\d][456][0-9]{3}[\s-]*[0-9]{4}[\s-]*[0-9]{4}[\s-]*[0-9]{4}[^\d].*")
permitidos = ('.txt', '.log', '.sql', '.ini', 'file', '.php', '.sh', 'xls', 'doc')

## Credenciais de E-mail
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_user = "slave@email.com"
email_pass = "123456"
email_admin = "admin@email.com"
email_subject = "Encontrado padrão de Cartão de Crédito"
conn = "" #Objeto de Conexão com o servidor de e-mail
messages = ""

# Main Function
def main():
    search();

# Retorna o hostname do servidor
def hostname():
    return "Servidor: %s" % os.uname()[1]

# Retorna um objeto de conexão com o servidor de E-mail
def connection():
    conn = s.SMTP(smtp_server, smtp_port)
    conn.starttls()
    conn.ehlo
    conn.login(email_user, email_pass)
    return conn

#Envia o e-mail para o Admin com os resultados encontrados
def sendmail(msg):
    message = MIMEMultipart()
    message['From'] = hostname()
    message['To'] = email_admin
    message['Subject'] = email_subject
    message.attach(MIMEText(msg, 'plain'))
    email = message.as_string()
    return conn.sendmail(email_user, email_admin, email)

# Lista todos os arquivos do HD
def search():
    global messages
    #Lista todos os diretórios do sistema
    for root, dirs, files in os.walk(path):
         #Lista cada arquivo dentro do diretório e aplica o Regex
         for file in files:
             filetest = os.path.join(root, file) # Caminho Absoluto
             regexinfile(filetest)

    #Se houver mensagens, envia o e-mail
    if messages != "":
        return sendmail(messages)

#Aplica os pattens no arquivo, listando todas as linhas do mesmo
def regexinfile(file):
    global messages
    try:
        if file.endswith(('.txt', '.log', '.sql', '.ini', 'file', '.php', '.sh', 'bkp')):
            for i, line in enumerate(open(file)):

                #Procura por padrões aleatórios de Visa/Master/Dinner dentro de strings
                for match in re.finditer(patternETC, line):
                    msg = 'Padrao de Cartão encontrado na linha %s:  do arquivo %s' % (i+1,file)
                    messages = "%s \n %s" % (messages, msg)

                #Procura pelo padrao Mastercard
                for match in re.finditer(patternMasterCard, line):
                    msg = 'Padrao Mastercard encontrado na linha %s:  do arquivo %s' % (i+1,file)
                    messages = "%s \n %s" % (messages, msg)

                #Procura pelo padrao VISA
                for match in re.finditer(patternVISA, line):
                    msg = 'Padrao Visa encontrado na linha %s:  do arquivo %s' % (i+1,file)
                    messages = "%s \n %s" % (messages, msg)
        else:
            pass
    except:
        return False

conn = connection();
main()
