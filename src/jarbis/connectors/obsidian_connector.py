import requests
import urllib3

# Disabilita il warning per certificati SSL self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ObsidianConnector:
    BASE_URL = "https://127.0.0.1:27124"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Per certificati self-signed
    
    def get_page_content(self, page: str) -> str:
        """
        Legge il contenuto di una pagina Obsidian.
        
        Args:
            page: Nome del file (con o senza estensione .md)
        
        Returns:
            Contenuto della pagina come stringa
        """
        # Imposta il file attivo
        self.session.put(
            f"{self.BASE_URL}/active/",
            json={"file": page}
        )
        
        # Leggi il contenuto
        response = self.session.get(f"{self.BASE_URL}/active/")
        response.raise_for_status()
        
        return response.text
        
    def update_page_content(self, page: str, content: str) -> str:
        """
        Sovrascrive completamente il contenuto di una pagina.
        
        Args:
            page: Nome del file
            content: Nuovo contenuto completo
        
        Returns:
            Messaggio di conferma
        """
        # Imposta il file attivo
        self.session.put(
            f"{self.BASE_URL}/active/",
            json={"file": page}
        )
        
        # Aggiorna il contenuto
        response = self.session.patch(
            f"{self.BASE_URL}/active/",
            json={"content": content}
        )
        response.raise_for_status()
        
        return f"Pagina '{page}' aggiornata con successo"
        
    def append_page_content(self, page: str, content: str) -> str:
        """
        Aggiunge contenuto alla fine di una pagina esistente.
        
        Args:
            page: Nome del file
            content: Contenuto da aggiungere
        
        Returns:
            Messaggio di conferma
        """
        # Imposta il file attivo
        self.session.put(
            f"{self.BASE_URL}/active/",
            json={"file": page}
        )
        
        # Aggiungi contenuto (usa POST per append)
        response = self.session.post(
            f"{self.BASE_URL}/active/",
            json={"content": content}
        )
        response.raise_for_status()
        
        return f"Contenuto aggiunto a '{page}' con successo"


obsidian_connector = ObsidianConnector()