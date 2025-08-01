#################################################################################################################
# Aplicação: extract_email_be
# Autor     : Claude Code                                                     31/07/2025
#            
# Finalidade: Esta aplicação tem como objetivo processar dados de casos de email e armazená-los em uma
#             base de conhecimento ChromaDB. Executa os seguintes passos:
#             1) Lê arquivo JSON com casos de email
#             2) Extrai e processa conteúdo dos emails
#             3) Gera chunks de conteúdo por caso/conversa
#             4) Calcula embeddings e armazena no ChromaDB
#
#             Baseado na estrutura do extract_pdf_be.py para manter consistência arquitetural.
#
#################################################################################################################
import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
import re
from datetime import datetime

def _extract_email_be(nmsg, message):
    """
    Função principal para processar dados de email
    """
    print('--->', message)
    
    # Obtém parâmetros da mensagem
    [parm_file, parm_out_file, option] = message.split('@')
    
    if not os.path.exists(parm_file):
        resp = "O arquivo de parâmetros não existe: " + parm_file
        return nmsg, False, resp
    
    try:
        with open(parm_file, 'r', encoding='utf-8') as fp:
            parametros = json.load(fp)
            
        # Extrai parâmetros do arquivo de configuração
        data_source = parametros['data_source']  # Arquivo JSON com os casos de email
        local_bd = parametros['local_bd']        # Diretório do ChromaDB
        collection_name = parametros['collection'] # Nome da coleção
        max_chunk_size = parametros.get('max_chunk_size', 1000)  # Tamanho máximo do chunk
        
    except KeyError as e:
        resp = f"Parâmetro obrigatório não encontrado: {e}"
        return nmsg, False, resp
    except Exception as e:
        resp = f"Erro ao ler arquivo de parâmetros: {e}"
        return nmsg, False, resp
    
    # Verifica se o arquivo de dados existe
    if not os.path.exists(data_source):
        resp = f"Arquivo de dados não encontrado: {data_source}"
        return nmsg, False, resp
    
    # Processa os dados de email
    Ok, resp = _process_email_data(data_source, local_bd, collection_name, max_chunk_size, option)
    
    return nmsg, Ok, resp

def _process_email_data(data_source, local_bd, collection_name, max_chunk_size, option):
    """
    Processa os dados de email e armazena no ChromaDB
    """
    try:
        # Inicializa ChromaDB
        chroma_client = chromadb.PersistentClient(local_bd)
        
        # Se opção de recriar foi especificada, deleta coleção existente
        if option.lower() == '-r':
            try:
                chroma_client.delete_collection(name=collection_name)
                print(f"Coleção {collection_name} removida para recriação")
            except:
                print(f"Coleção {collection_name} não existia, criando nova")
        
        # Cria ou acessa a coleção
        collection = chroma_client.get_or_create_collection(name=collection_name)
        
        # Inicializa modelo de embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
    except Exception as e:
        return False, f"Erro ao inicializar ChromaDB: {e}"
    
    try:
        # Carrega dados de email
        with open(data_source, 'r', encoding='utf-8') as file:
            email_data = json.load(file)
        
        print(f"Carregados {len(email_data)} casos de email")
        
        chunk_count = 0
        
        # Processa cada caso de email
        for case_idx, case in enumerate(email_data):
            try:
                # Extrai informações do caso
                case_info = _extract_case_info(case)
                print(f"Processando caso {case_idx + 1}/{len(email_data)}: {case_info['case_number']}")
                
                # Processa emails do caso
                email_chunks = _process_case_emails(case, case_info, max_chunk_size)
                print(f"Gerados {len(email_chunks)} chunks para caso {case_info['case_number']}")
                
                # Armazena chunks no ChromaDB
                for chunk_idx, chunk_data in enumerate(email_chunks):
                    chunk_id = f"case_{case_info['case_number']}_chunk_{chunk_idx}"
                    
                    # Verifica se chunk já existe
                    existing = collection.get(ids=[chunk_id])
                    if existing['documents'] == []:
                        # Calcula embedding e adiciona
                        embedding = model.encode(chunk_data['content'])
                        collection.add(
                            documents=[chunk_data['content']], 
                            embeddings=[embedding],
                            ids=[chunk_id],
                            metadatas=[chunk_data['metadata']]
                        )
                        chunk_count += 1
                        print(f"Adicionado chunk: {chunk_id}")
                    else:
                        print(f"Chunk já existe: {chunk_id}")
                        
            except Exception as e:
                print(f"Erro ao processar caso {case_idx}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return True, f"Processamento concluído. {chunk_count} chunks adicionados à coleção {collection_name}"
        
    except Exception as e:
        return False, f"Erro ao processar dados de email: {e}"

def _extract_case_info(case):
    """
    Extrai informações principais do caso
    """
    return {
        'case_number': str(case.get('case_number', 'unknown')),  # Converte para string
        'account_name': case.get('account_name', ''),
        'user_name': case.get('user_name', ''),
        'case_status': case.get('case_status', ''),
        'case_reason': case.get('case_reason', ''),
        'case_created_date': case.get('case_created_date', ''),
        'case_closed_date': case.get('case_closed_date', ''),
        'thread_id': case.get('thread_id', '')
    }

def _process_case_emails(case, case_info, max_chunk_size):
    """
    Processa emails de um caso e gera chunks
    """
    chunks = []
    
    # Chunk com informações do caso
    case_summary = f"""Caso: {case_info['case_number']}
Empresa: {case_info['account_name']}
Usuário: {case_info['user_name']}
Status: {case_info['case_status']}
Motivo: {case_info['case_reason']}
Data Criação: {case_info['case_created_date']}
Data Fechamento: {case_info['case_closed_date']}"""
    
    # Processa emails do caso
    emails = case.get('emails', [])
    email_content = ""
    
    for email_idx, email in enumerate(emails):
        email_text = f"""
--- Email {email_idx + 1} ---
De: {email.get('from', '')}
Para: {email.get('to', '')}
Assunto: {email.get('subject', '')}
Data: {email.get('date', '')}
Tipo: {email.get('sender_type', '')}

Conteúdo:
{email.get('body', '')}
"""
        
        # Se adicionar este email ultrapassar o limite, cria novo chunk
        if len(email_content + email_text) > max_chunk_size and email_content:
            chunks.append({
                'content': case_summary + "\n\n" + email_content,
                'metadata': {
                    'case_number': case_info['case_number'],
                    'account_name': case_info['account_name'],
                    'chunk_type': 'emails',
                    'email_count': email_content.count('--- Email')
                }
            })
            email_content = email_text
        else:
            email_content += email_text
    
    # Adiciona último chunk se houver conteúdo
    if email_content:
        chunks.append({
            'content': case_summary + "\n\n" + email_content,
            'metadata': {
                'case_number': case_info['case_number'],
                'account_name': case_info['account_name'],
                'chunk_type': 'emails',
                'email_count': email_content.count('--- Email')
            }
        })
    
    # Se não há emails, cria chunk apenas com informações do caso
    if not chunks:
        chunks.append({
            'content': case_summary,
            'metadata': {
                'case_number': case_info['case_number'],
                'account_name': case_info['account_name'],
                'chunk_type': 'case_info',
                'email_count': 0
            }
        })
    
    return chunks