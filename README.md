Para relembrar…

Nada mais prático que um guia rápido para a customização de sistemas com a arquitetura estudada neste ebook. Assim, segue uma sequência de passos que mostra de forma clara o quanto é simples customizar uma aplicação na abordagem aqui proposta. Os passos são:
Criar o ambiente operacional. Para isso, basta seguir o processo descrito nessa Unidade. 
Baixar os códigos do github. Os códigos podem ser obtidos com a digitação, em um browse, do seguinte URL:

https://github.com/AKCIT-Geral/RH-NLP-M10-APMPEPM-V1 ou 
https://github.com/sandrerleypires/ebook10.git

     A seguinte estrutura deve ser o resultado final da obtenção dos códigos: 
     ![image](https://github.com/user-attachments/assets/5de6592c-4e16-4cdf-af36-f5efa663ae3e)


Como Customizar o SAD
Criação do banco de dados do Gerenciador de Mensagem. Em uma Janela de Comando, digite:
...\sad> python ..\arquitetura\bd.py -dbname message.db -r

Ativação do Gerenciador Assíncrono de Mensagens: 
...\sad> fastapi dev ..\arquitetura\gerenciador.py

 Ativação do controlador. Em uma nova Janela de Comando, digite: 
...\sad> python ..\arquitetura\controlador.py

Criação da base de conhecimento a partir de dados de um banco de dados. Inicialmente, deve-se criar arquivos de parâmetros (já existem os arquivos do exemplo). Em um terceira Janela de Comandos, executar:
...\sad> python ..\arquitetura\extract_sql_fe.py
...\sad> python ..\arquitetura\business_rules_fe.py

Ativando o Flask. Em uma quarta Janela de Comandos, digitar:
...\sad> set FLASK_APP=app.py
...\sad> python app.py

Após esses passos é possível acessar o SAD em um browser web.
O endereço a ser digitado no browser é: http://127.0.0.1:5000

Customizar o chatbot
Criação do banco de dados do Gerenciador de Mensagem. Em uma Janela de Comando, digite:
...\chatbot> python ..\arquitetura\bd.py -dbname message.db -r

Ativação do Gerenciador Assíncrono de Mensagens: 
...\chatbot> fastapi dev ..\arquitetura\gerenciador.py

 Ativação do controlador. Em uma nova Janela de Comando, digite: 
...\chatbot> python ..\arquitetura\controlador.py

Extração do conteúdo do livro e armazenamento desse na base de conhecimento. Inicialmente, deve-se criar arquivos de parâmetros já existe o arquivo do exemplo). Em um terceira Janela de Comandos, executar:
...\chatbot> python ..\arquitetura\extract_pdf_fe.py

Ativando o Flask. Em uma quarta Janela de Comandos, digite:
...\chatbot> set FLASK_APP=app.py
...\chatbot> python app.py

Após esses passos, é possível acessar o SAD em um browser web. 
O endereço a ser digitado no browser é: http://127.0.0.1:5000 


Saiba mais…
Para mais informações sobre como configurar o ambiente Anaconda®, sugere-se alguns tutoriais, como:
DATACAMP. Instalando o Anaconda no Windows. Datacamp, 2024. Disponível em: https://www.datacamp.com/pt/tutorial/installing-anaconda-windows. Acesso em: 10 jan. 2025.
BRAINS. Anaconda: introdução e instalação. Brains, 2023. Disponível em: https://brains.dev/2023/anaconda-introducao-e-instalacao/. Acesso em: 10 jan. 2025.
HASHTAG PROGRAMAÇÃO. Instalando o Jupyter - Pacote Anaconda para Programação em Python. YouTube, 2021. Disponível em: https://www.youtube.com/watch?v=_eK0z5QbpKA. Acesso em: 10 jan. 2025. 
Ressalta-se que existem inúmeros tutoriais que tratam de instalação e uso de ambientes de desenvolvimento em Python® com o produto Anaconda®.

