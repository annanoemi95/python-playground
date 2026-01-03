import json
import os
from datetime import datetime



def gestionecorsi(lista_corsi):
    print(lista_corsi)
    nuovo_corso = input("Inserire un nuovo corso:\n")
    if nuovo_corso not in lista_corsi:
        lista_corsi.append(nuovo_corso)
        print(f"Il corso {nuovo_corso} è stato creato con successo")
    return lista_corsi    



def gestionepartecipanti(lista_corsi, partecipanti, corsi):
    nuovo_partecipante = input("Inserire Nome e Cognome del nuovo partecipante:\n")
    if nuovo_partecipante not in partecipanti:
        partecipanti.append(nuovo_partecipante)
    scelta_corso = input(f"Inserire il nome del corso a cui iscrivere {nuovo_partecipante}:\n")    
    if scelta_corso in lista_corsi:
        corsi.setdefault(scelta_corso, {})[nuovo_partecipante] = (0, "")
    else:
        print("Il corso inserito non esiste")    
    return partecipanti, corsi    

def assegnazione_goleador(corsi):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_partecipante = input("Inserire il nome del partecipante da valutare:\n")
    nome_corso = input("Inserire il nome del corso da valutare:\n")
    voto = input("Inserire numero goleador vinte da 1 a 10:\n")
    if nome_corso in corsi and nome_partecipante in corsi[nome_corso]:
        corsi[nome_corso][nome_partecipante] = (int(voto), timestamp)
    return corsi



def salva_in_json(lista_corsi, partecipanti, corsi, GoleadorAcademy):
    dati = {
        "lista_corsi": lista_corsi,
        "partecipanti": partecipanti,
        "punteggio": corsi
    }
    with open(GoleadorAcademy, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)

def leggi_json(GoleadorAcademy):
    if os.path.exists(GoleadorAcademy):
        with open(GoleadorAcademy, "r", encoding="utf-8") as file:
            dati = json.load(file)
            return dati["lista_corsi"], dati["partecipanti"], dati["punteggio"]
    else:
        return [], [], {}

def statistiche(corsi):
    totale_goleador = {}
    for corso in corsi:
        tot = 0
        for studente in corsi[corso]:
            tot += corsi[corso][studente][0]
        totale_goleador[corso] = tot
        print(f"Il totale delle goleador per il corso {corso} è {tot}")  

    totale = {}
    for corso in corsi:
        for studente in corsi[corso]:
            if studente not in totale:
                totale[studente] = 0
            voto = corsi[corso][studente][0]
            totale[studente] += voto

    tmp_max = 0
    best = ""
    for studente in totale:
        voto = totale[studente]
        if voto > tmp_max:
            best = studente
            tmp_max = voto
    print(f"Il voto massimo è di {best} ed è {tmp_max}")      

        
        

def main():
    lista_corsi, partecipanti, corsi = leggi_json("GoleadorAcademy.json")

    print("Benvenuto nel Goleador Academy")
    while True: 
        scelta = input("Scegliere l'azione desiderata:\n1.Aggiungere un nuovo corso\n2.Aggiungere un nuovo partecipante\n3.Assegna un punteggio a un partecipante\n4. Visualizza statistiche\n")
        if scelta == "1":
            lista_corsi = gestionecorsi(lista_corsi)
        elif scelta == "2":
            partecipanti, corsi = gestionepartecipanti(lista_corsi, partecipanti, corsi)
        elif scelta == "3":
            corsi = assegnazione_goleador(corsi)
        elif scelta == "4":
            statistiche(corsi)
        else:
            return

        salva_in_json(lista_corsi, partecipanti, corsi, "GoleadorAcademy.json")
    
main()