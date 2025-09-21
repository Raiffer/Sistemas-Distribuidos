import json
import os

class Leitor:
    def __init__(self):
        self.mensagens = 0

    def criar_mensagem(self,destinatario,mensagem,remetente):
        dados = {
            "destinatario": destinatario,
            "mensagem": mensagem,
            "remetente": remetente
        }

        pasta = "C:\\Users\\Bernardo\\Documents\\Sistemas Distribuidos\\mensagens"
        os.makedirs(pasta, exist_ok=True)  

        nome_arquivo = str(self.mensagens) + ".json"

        caminho_completo = os.path.join(pasta, nome_arquivo)

        with open(caminho_completo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        self.mensagens = self.mensagens + 1
        
        return caminho_completo
    
    def ler_mensagem(self, conteudo):
        try:
            json_obj = json.loads(conteudo)
            mensagem = json_obj.get("mensagem")
            remetente = json_obj.get("remetente")
        except Exception as e:
            print(f"Erro ao processar JSON: {e}")

        print(f"\n{remetente}: {mensagem}")
        self.mensagens = self.mensagens + 1