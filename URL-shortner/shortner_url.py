#!/usr/bin/env python3

import json
import os
import requests
from datetime import datetime
import uuid

DB_FILE = os.path.join(os.path.dirname(__file__), "db.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return {"links": [], "categories": ["lavoro", "social", "tools"]}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("⚠️ Errore nel caricamento del database. Viene creato un nuovo DB vuoto.")
        return {"links": [], "categories": ["lavoro", "social", "tools"]}

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("❌ Errore nel salvataggio del database.")

def shorten_api(url, alias=None):
    api_url = "https://is.gd/create.php?format=json"
    params = {'url': url}
    if alias:
        params['shorturl'] = alias
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        data = response.json()
        
        if 'shorturl' in data:
            return data['shorturl']
        elif 'errorcode' in data:
            # is.gd error codes: 1=url problem, 2=alias problem, etc.
            error_msg = data.get('errormessage', 'Unknown error')
            if data['errorcode'] == 2 and alias:
                 print(f"❌ Alias '{alias}' non disponibile o non valido.")
            else:
                 print(f"❌ API Error: {error_msg}")
            return None
    except requests.RequestException as e:
        print(f"❌ Errore di connessione: {e}")
        return None
    return None

def add_link(db, url, alias=None, category=None):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"⏳ Accorciamento di '{url}'...")
    short_url = shorten_api(url, alias)
    
    if short_url:
        new_link = {
            "id": str(uuid.uuid4()),
            "original_url": url,
            "short_url": short_url,
            "alias": alias if alias else short_url.split('/')[-1],
            "category": category,
            "created_at": datetime.now().isoformat()
        }
        db['links'].append(new_link)
        save_db(db)
        print(f"✅ Link creato! ✂️ {short_url}")
        print(f"🔗 Originale: {url}")
    else:
        print("❌ Creazione link fallita.")

def list_links(db):
    if not db['links']:
        print("📭 Nessun link salvato.")
        return

    print(f"\n{'ALIAS':<15} | {'SHORT URL':<25} | {'ORIGINAL URL'}")
    print("-" * 60)
    for link in db['links']:
        alias = link.get('alias', 'N/A') or 'N/A'
        short = link['short_url']
        original = link['original_url']
        # Truncate original if too long
        if len(original) > 40:
            original = original[:37] + "..."
        print(f"{alias:<15} | {short:<25} | {original}")
    print("-" * 60)

def delete_link(db, identifier):
    initial_count = len(db['links'])
    # Filter out links matching alias or short_url
    db['links'] = [l for l in db['links'] if l.get('alias') != identifier and l['short_url'] != identifier and identifier not in l['short_url']]
    
    if len(db['links']) < initial_count:
        save_db(db)
        print(f"🗑️ Link '{identifier}' eliminato.")
    else:
        print(f"❌ Nessun link trovato con identificativo '{identifier}'.")

def search_links(db, query):
    results = [l for l in db['links'] if query.lower() in l['original_url'].lower() or query.lower() in (l.get('alias') or '').lower()]
    if not results:
        print(f"🔍 Nessun risultato per '{query}'.")
        return
    
    print(f"\n🔍 Risultati per '{query}':")
    for link in results:
        print(f"- {link.get('alias', 'N/A')}: {link['short_url']} -> {link['original_url']}")

def show_stats(db):
    total = len(db['links'])
    print(f"\n📊 Statistiche:")
    print(f"🔗 Totale Link: {total}")
    if db['links']:
        last = db['links'][-1]
        print(f"🆕 Ultimo creato: {last['short_url']} ({last.get('created_at', 'N/A')})")

def manage_categories(db):
    while True:
        print("\n📂 Gestione Categorie")
        print("1. Lista categorie")
        print("2. Aggiungi categoria")
        print("3. Indietro")
        choice = input("Scelta: ")
        
        if choice == '1':
            print("Categorie esistenti:", ", ".join(db.get('categories', [])))
        elif choice == '2':
            new_cat = input("Nome nuova categoria: ").strip()
            if new_cat and new_cat not in db.get('categories', []):
                db.setdefault('categories', []).append(new_cat)
                save_db(db)
                print(f"✅ Categoria '{new_cat}' aggiunta.")
        elif choice == '3':
            break

def interactive_menu():
    db = load_db()
    while True:
        print("\n--- URL Shortener CLI ---")
        print("1. ✂️  Accorcia URL")
        print("2. 📋 Lista Link")
        print("3. 🔍 Cerca Link")
        print("4. 🗑️  Elimina Link")
        print("5. 📂 Categorie")
        print("6. 📊 Statistiche")
        print("0. 🚪 Esci")
        
        choice = input("Scelta: ")
        
        if choice == '1':
            url = input("Inserisci URL lungo: ").strip()
            if not url: continue
            
            use_alias = input("Vuoi un alias personalizzato? (s/N): ").lower()
            alias = None
            if use_alias == 's':
                alias = input("Alias desiderato (da 4 a 10 caratteri alfanumerici): ").strip()
                save_db(db)    
                
            category = input("Categoria: ").strip()
            if category not in db.get('categories', []):
                db.setdefault('categories', []).append(category)
                save_db(db)
            add_link(db, url, alias, category)
            
        elif choice == '2':
            list_links(db)
        elif choice == '3':
            q = input("Cerca (URL o alias): ").strip()
            search_links(db, q)
        elif choice == '4':
            ident = input("Inserisci alias o short URL da eliminare: ").strip()
            delete_link(db, ident)
        elif choice == '5':
            manage_categories(db)
        elif choice == '6':
            show_stats(db)
        elif choice == '0':
            print("👋 Bye!")
            break
        else:
            print("❌ Scelta non valida.")

def main():
    interactive_menu()

    
if __name__ == "__main__":
    main()
