import json
import boto3

def lambda_handler(event, context):
   #0 VARS
   caminho_do_arquivo_local = "/tmp/arquivo.txt"
   nome_do_arquivo_local = "arq_dentro_do_s3.txt"
   nome_do_s3 = "rendell-s3-origem"
   
   #1 CRIA UM ARQUIVO
   arquivo = open(caminho_do_arquivo_local, 'w')
   arquivo.write('linha 01 \n')
   arquivo.write('linha 02 \n')
   arquivo.write('linha 03 \n')
   arquivo.close()
   
   #2 REALIZAR UPLOUD
   s3 = boto3.client('s3')
   with open(caminho_do_arquivo_local, 'rb') as f:
       s3.upload_fileobj(f, nome_do_s3, nome_do_arquivo_local)
