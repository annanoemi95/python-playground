from google import genai
from dotenv import load_dotenv
import os
from google.api_core import exceptions

load_dotenv()

def city_temperature():
    nome_citta = input("Inserisci il nome di una città per sapere quanti gradi ci sono al momento:\n")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    try:
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=f"Dimmi quanti gradi ci sono in media nella città di {nome_citta} senza aggiungere altro, rispondi solo con il numero relativo ai gradi"
            )
        risposta_definitiva = ""
        for chunk in response:
           risposta_definitiva += chunk.text
        return risposta_definitiva
    except exceptions.ResourceExhausted:
        print("Errore 429: Troppe richieste!")
    except exceptions.ServiceUnavailable:
        print("Errore 503: Il server di Google è momentaneamente giù.")
    except Exception as e:
        print(f"Errore imprevisto:{e}")
    
def mostra_temperatura(risposta_definitiva):
    print(f"La temperatura della citta e di {risposta_definitiva} gradi")

def main():
    risposta = city_temperature()
    if not risposta:
        print("C'è stato un Errore")
    else:
        mostra_temperatura(risposta)    


main()