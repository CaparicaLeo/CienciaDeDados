import firebase_admin
from firebase_admin import credentials, auth, firestore, storage, messaging, exceptions
import os

# --- 1. CONFIGURAÇÃO E INICIALIZAÇÃO ---
def initialize_firebase(json_path):
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(json_path)
            app = firebase_admin.initialize_app(cred, {
                'storageBucket': 'seu-projeto-id.appspot.com'
            })
            print(f"✅ Firebase inicializado: {app.name}")
        return firestore.client()
    except Exception as e:
        print(f"❌ Erro crítico na inicialização: {e}")
        exit()

# --- 2. GERENCIAMENTO DE USUÁRIOS (AUTH) ---
def manage_user(email, password):
    print("\n--- Gerenciamento de Usuário ---")
    try:
        user = auth.create_user(email=email, password=password)
        print(f"Usuário criado: {user.uid}")

        user_info = auth.get_user(user.uid)
        print(f"Informações recuperadas: {user_info.email}")
        return user.uid
    except exceptions.FirebaseError as e:
        print(f"Erro no Auth: {e}")

# --- 3. OPERAÇÕES DE FIRESTORE (UPDATE) ---
def update_product_price(db, product_id, new_price):
    print("\n--- Atualização de Produto ---")
    try:
        doc_ref = db.collection('produtos_mysql').document(str(product_id))
        doc_ref.update({'preco': new_price})
        print(f"Produto {product_id} atualizado para R$ {new_price}")
    except exceptions.FirebaseError as e:
        print(f"Erro ao atualizar Firestore: {e}")

# --- 4. CONSULTAS AVANÇADAS ---
def query_products(db, threshold):
    print(f"\n--- Produtos acima de R$ {threshold} ---")
    try:
        docs = db.collection('produtos_mysql').where('preco', '>', threshold).stream()
        for doc in docs:
            p = doc.to_dict()
            print(f"ID: {doc.id} | Nome: {p.get('nome')} | Preço: R$ {p.get('preco')}")
    except exceptions.FirebaseError as e:
        print(f"Erro na consulta: {e}")

# --- 5. UPLOAD PARA STORAGE ---
# def upload_file_content(filename, content):
#     print("\n--- Upload para Storage ---")
#     try:
#         bucket = storage.bucket()
#         blob = bucket.blob(filename)
#         blob.upload_from_string(content, content_type='text/plain')
#         print(f"Arquivo '{filename}' enviado com sucesso!")
#     except exceptions.FirebaseError as e:
#         print(f"Erro no Storage: {e}")
        

# --- 6. ENVIO DE NOTIFICAÇÃO (MESSAGING) ---
def send_test_notification(topic="alerts"):
    print("\n--- Envio de Notificação ---")
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title='Alerta de Sistema',
                body='O script Python rodou com sucesso!',
            ),
            topic=topic,
        )
        response = messaging.send(message)
        print(f"Notificação enviada: {response}")
    except exceptions.FirebaseError as e:
        print(f"Erro no Messaging: {e}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    CREDENTIALS_PATH = "Lista6/data-science-d5ca2-firebase-adminsdk-fbsvc-a77e99e337.json" 
    
    if os.path.exists(CREDENTIALS_PATH):
        db_client = initialize_firebase(CREDENTIALS_PATH)

        manage_user("leonardo_teste@exemplo.com", "senha_segura_123")
        
        update_product_price(db_client, "101", 19.90)
        
        query_products(db_client, 15.00)

        # Upload Storage
        # upload_file_content("logs_execucao.txt", "Olá, Firebase Storage! Registro de teste.")

        send_test_notification("geral")

        print("\n Todas as operações finalizadas.")
    else:
        print(f" Erro: Arquivo '{CREDENTIALS_PATH}' não encontrado.")