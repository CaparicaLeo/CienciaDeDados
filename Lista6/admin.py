import firebase_admin
from firebase_admin import credentials

def initialize_firebase(service_account_path):
    try:
        cred = credentials.Certificate(service_account_path)
        
        app = firebase_admin.initialize_app(cred)
        
        print(f"Sucesso! Aplicativo Firebase inicializado: {app.name}")
        
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")

if __name__ == "__main__":
    PATH_TO_JSON = "Lista6/data-science-d5ca2-firebase-adminsdk-fbsvc-a77e99e337.json"
    initialize_firebase(PATH_TO_JSON)