
from requests import get, exceptions
import re


URL: str = "https://github.com"
REPO_PATTERN = r'<a\s+[^>]*itemprop="name codeRepository"[^>]*>([^<]+)<\/a>'
BRANCH_PATTERN = r'<div[^>]*class="prc-Truncate[^"]*"[^>]*>([^<]+)<\/div>'
PATTERN = r'<h3[^>]*data-testid="commit-group-title"[^>]*>\s*Commits on\s*([^<]+)\s*</h3>'

    
def raccolta_dati_utente():     
    nome_utente = input("Inserire il nome dell'utente da controllare: ")
    if not nome_utente:
        raise ValueError("Il nome utente non può essere vuoto")
    nome_repository = input("Inserire il nome della repository da controllare: ")
    if not nome_repository:
        raise ValueError
    nome_branch = input("Inserire il nome del branch: ")
    if not nome_branch:
        raise ValueError
    url = f"{URL}/{nome_utente}/{nome_repository}/commits/{nome_branch}/"       
    return url

def ottieni_html(url:str):
    try:
        response = get(url)
        
        if response.status_code != 200:
            
            raise ValueError(f"API Error! Status code: {response.status_code}")
            
        return response.text

    except exceptions.RequestException as e:
       print(f"A network error occurred: {e}")
    except ValueError as e:
        # This catches the error we raised manually above
        print(f"Data error: {e}")

def check_commits(url:str):
    html = ottieni_html(url)
    match = re.search(PATTERN, html)
    if match:
        return match.group(1).strip()
    return None

def ottieni_lista_repo(nome_utente:str):
    
    url_repo = f"{URL}/{nome_utente}?tab=repositories"
    print(url_repo)
    try:
        response = get(url_repo)
        html = response.text
        if response.status_code != 200:
            raise ValueError(f"API Error! Status code: {response.status_code}")
            
    except exceptions.RequestException as e:
       print(f"A network error occurred: {e}")
    except ValueError as e:
        print(f"Data error: {e}")   

    lista_repo_tmp = []
    lista_repo_tmp.extend(re.findall(REPO_PATTERN, html))
    lista_repo = [l.strip() for l in lista_repo_tmp]

    print("REPO TROVATE:", len(lista_repo))
    for i, j in enumerate(lista_repo, start=1):
        print(f"Repository[{i}]:{j}")

    try:
        scelta = input(f"\nScegli un numero (da 1 a {len(lista_repo)}): ")   
        if not scelta:
            print("Errore: Non hai inserito nulla.")
            return
        indice = int(scelta)-1 #Controllo se il numero è nell'intervallo della lista
        if 0 <= indice < len(lista_repo):
            nome_repo = lista_repo[indice].strip()
            print(f"Hai selezionato:{nome_repo}")
            return nome_repo
        else:
            print("Errore: Il numero inserito è fuori dall'intervallo.")

    except ValueError: #casi in cui l'utente scrive "due" o "abc" invece di "2"
        print("Errore: Devi inserire un numero intero valido.")


def ottieni_lista_branches(nome_utente:str, nome_repo:str): 
    url_branch:str = f"{URL}/{nome_utente}/{nome_repo}/branches"
    print(url_branch)
    
    try:
        response = get(url_branch)
        html = response.text
        if response.status_code != 200:
            raise ValueError(f"API Error! Status code: {response.status_code}")
            
    except exceptions.RequestException as e:
       print(f"A network error occurred: {e}")
    except ValueError as e:
        print(f"Data error: {e}")

    lista_branches_tmp = []
    lista_branches_tmp.extend(re.findall(BRANCH_PATTERN, html))
    lista_branches = [l.strip() for l in lista_branches_tmp]
    print("BRANCHES TROVATI:", len(lista_branches))
    for i, j in enumerate(lista_branches, start=1):
        print(f"Branches[{i}]:{j}")
    if len(lista_branches) == 1:
        return lista_branches[0]
    try:
        scelta = input(f"Scegli un numero (da 1 a {len(lista_branches)}): ")
        if not scelta:
            print("Errore: Non hai inserito nulla.")
            return
        indice = int(scelta)-1 #Controllo se il numero è nell'intervallo della lista
        if 0 <= indice < len(lista_branches):
            branch_scelto = lista_branches[indice]
            print(f"Hai selezionato: {branch_scelto}")
            return branch_scelto
        else:
            print("Errore: Il numero inserito è fuori dall'intervallo.")

    except ValueError: #casi in cui l'utente scrive "due" o "abc" invece di "2"
        print("Errore: Devi inserire un numero intero valido.")    



def main():
    print(f"{'*'*50}\nVedo i tuoi commit su GitHub🕵️\n{'*'*50}")
    scelta = input("Per controllare i commits devi conoscere il nome utente, se conosci anche quelli di repository e branch premi 's', se non li conosci premi 'x' e te li mostro🔮: ")
    if scelta == 's':
        u = raccolta_dati_utente()
        print(u)
        risposta = input("Le informazioni nell'url sono corrette? Premi 's' se sono corrette altrimenti premi 'n': ")
        if risposta == 's':
            data = check_commits(u)
            print("Data ultimo commit:", data)
        else:
            main()
            
    else:
        nome_utente = input("Inserisci il nome utente: ")
        nome_repo = ottieni_lista_repo(nome_utente)
        nome_branch = ottieni_lista_branches(nome_utente, nome_repo)
        url_ottenuto = f"{URL}/{nome_utente}/{nome_repo}/commits/{nome_branch}"
        data_commit = check_commits(url_ottenuto)
        print("Data ultimo commit: ", data_commit)

    

if __name__=="__main__":
  main()