import requests
import json
from datetime import datetime


def get_followers_logins(username: str) -> list[str]:
    url = f"https://api.github.com/users/{username}/followers?page="
    i:int = 1
    lista_user = []
    while True:
        r = requests.get(url+f"{i}", headers={"Accept": "application/vnd.github+json"}, timeout=10)
        r.raise_for_status()
        i +=1  

        data = r.json()  # lista di dizionari
        if data == []:
            break 
       
        for user in data:
            lista_user.append(user["login"])
        
    return lista_user
    

def salva_lista_in_json(lista_user, prefisso_file="followers"):
    # 1) Converte lista in dizionario con chiavi crescenti (1,2,3...)
    dati = {}
    for i, elemento in enumerate(lista_user):
        dati[str(i + 1)] = elemento
    
    # 2) Crea un nome file unico usando data e ora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_file = f"{prefisso_file}_{timestamp}.json"

    # 3) Salva su file
    with open(nome_file, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)

    return nome_file


def main():
    username = input("Inserire l'username per accedere alla lista dei follower:\n")
    lista_user = get_followers_logins(username)
    print(f"Il totoale dei follower di {username} è: {len(lista_user)}")
    salva_lista_in_json(lista_user, prefisso_file=f"followers_{username}")

if __name__=="__main__":
  main()