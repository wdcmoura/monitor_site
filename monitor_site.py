import requests
import time
from datetime import datetime

# URL para monitorar
url = "http://google.com"

# Configurações de tempo
intervalo_verificacao = 1  # segundos entre cada verificação
timeout = 60  # tempo máximo de resposta em segundos

# Função para registrar logs de falha
def registrar_falha(mensagem):
    with open("falhas_unimed.log", "a") as log:
        log.write(f"{datetime.now()} - {mensagem}\n")
    print(f"{datetime.now()} - {mensagem}")

# Função principal de monitoramento
def monitorar():
    while True:
        try:
            resposta = requests.get(url, timeout=timeout)

            # Se o status não for 200, algo deu errado
            if resposta.status_code != 200:
                if 400 <= resposta.status_code < 500:
                    registrar_falha(f"ERRO CLIENTE {resposta.status_code} - O site retornou erro do lado do cliente.")
                elif 500 <= resposta.status_code < 600:
                    registrar_falha(f"ERRO SERVIDOR {resposta.status_code} - O site retornou erro do lado do servidor.")
                else:
                    registrar_falha(f"RESPOSTA INESPERADA {resposta.status_code} - Código fora do esperado.")

        except requests.exceptions.Timeout:
            registrar_falha(f"TIMEOUT - O site não respondeu em {timeout} segundos.")
        
        except requests.exceptions.ConnectionError:
            registrar_falha("ERRO DE CONEXÃO - Não foi possível se conectar ao site.")
        
        except requests.exceptions.RequestException as e:
            registrar_falha(f"FALHA DESCONHECIDA - {e}")

        time.sleep(intervalo_verificacao)

if __name__ == "__main__":
    monitorar()
