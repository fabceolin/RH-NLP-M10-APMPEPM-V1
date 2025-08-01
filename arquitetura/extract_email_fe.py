#################################################################################################################
# Aplicação: extract_email_fe
# Autor     : Claude Code                                                     31/07/2025
#            
# Finalidade: Esta aplicação tem como objetivo estabelecer comunicação com o gerenciador
#             assíncrono de mensagens para processar dados de casos de email.
#             Interface frontend para o extract_email_be.py
#
#             Baseado na estrutura do extract_pdf_fe.py para manter consistência.
#
#################################################################################################################
import argparse
import requests
from datetime import datetime
import time

def send_message(parametros_json, outfile, option):
    """
    Envia mensagem para o gerenciador processar dados de email
    """
    API_URL = "http://localhost:8000/send"
    message = {
        "messagem": 0,
        "moment": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender": "extract_email_fe",
        "receiver": "extract_email_be",
        "control": 7,  # Novo código de controle para emails
        "content": parametros_json + '@' + outfile + '@' + option,
        "log": "False",
        "status": "E"
    }
    response = requests.post(API_URL, json=message) 
    return response

if __name__ == "__main__":
    # Configuração dos argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Processamento de dados de casos de email para ChromaDB.")
    parser.add_argument("-j", default="../chatbot/extract_email.json", 
                       help="Nome do arquivo JSON com configurações para processamento de emails")
    parser.add_argument("-o", default="", 
                       help="Nome do arquivo de saída (opcional)")
    parser.add_argument("-r", default="", 
                       help="Se esta opção é informada (-r), a coleção é recriada")
    
    args = parser.parse_args()

    print(f'Processando dados de email com configuração: {args.j}')
    print(f'Arquivo de saída: {args.o if args.o else "não especificado"}')
    print(f'Opção: {args.r if args.r else "manter coleção existente"}')
    
    # Envia mensagem para processamento
    response = send_message(args.j, args.o, args.r)
    
    # Laço de espera pelo resultado
    API_URL = "http://localhost:8000/finished/" + str(response.json())
    start_time = time.time()
    max_seconds = 120  # 2 minutos para dados de email (pode ser mais demorado)
    
    print("Aguardando processamento...")
    
    while time.time() - start_time < max_seconds:
        try:
            resp = requests.get(API_URL)
            if resp.json() != 'Nok':
                break
        except:
            pass
        time.sleep(2)  # Verifica a cada 2 segundos
        
    if time.time() - start_time < max_seconds:
        elapsed_time = time.time() - start_time
        print(f'Processamento de emails concluído com sucesso!')
        print(f'Tempo de execução: {elapsed_time:.2f} segundos')
        try:
            result = requests.get(API_URL).json()
            print(f'Resultado: {result}')
        except:
            print('Processamento concluído.')
    else:
        print('Timeout: O processamento demorou mais que o esperado.')
        print('Verifique os logs do sistema ou tente novamente.')