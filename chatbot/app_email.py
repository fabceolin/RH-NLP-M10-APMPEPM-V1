#################################################################################################################
# Aplicação: app_email.py - Versão para consultar dados de email
# Baseado em: app.py
# Modificado por: Claude Code                                              31/07/2025            
#            
# Finalidade: Interface web para consultar a base de dados de casos de email
#            
#################################################################################################################
import requests
from datetime import datetime
import time
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Função para enviar mensagem usando configuração de email
def send_message(user_question):
    API_URL = "http://localhost:8000/send"
    message = {
        "messagem":  0,
        "moment":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender":   "chatbot_fe",
        "receiver": "virtual_assistant_be",
        "control":  5,
        "content":  user_question+'@./virtual_assistant_email.json',    # USA CONFIGURAÇÃO DE EMAIL
        "log":      "False",
        "status":   "E"
        }
    response = requests.post(API_URL, json=message) 
    return response 

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    user_question = ""
    bot_response = ""

    if request.method == 'POST':
        if 'submit' in request.form:
            question = request.form.get('question', '')
            response = send_message(question)
            
            # Simples lógica de exemplo de resposta
            API_URL = "http://localhost:8000/finished/" + str(response.json())
            start_time = time.time()
            max_seconds = 30
            while time.time() - start_time < max_seconds:
                resp = requests.get(API_URL) 
                if resp.json() !='Nok':                    
                    break
                time.sleep(1)
                
            if time.time() - start_time < max_seconds:
                bot_response = f"Você perguntou: '{question}'. \n\nResposta: {resp.json()}"
            else:
                bot_response = "Você perguntou: '{question}'. \n\n" + \
                               "Resposta: Tempo de espera da resposta está esgotado. Tente mais tarde."       
        elif 'exit' in request.form:
            return redirect(url_for('exit_app'))

    return render_template('chatbot.html', question=user_question, response=bot_response)

@app.route('/exit')
def exit_app():
    return "Aplicação encerrada. Obrigado por usar o chatbot de casos de email!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Usando porta 5001 para não conflitar