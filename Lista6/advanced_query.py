from firebase_admin import exceptions
def query_expensive_products(db, threshold):
    try:
        produtos_ref = db.collection('produtos_mysql')
        query = produtos_ref.where('preco', '>', threshold).stream()

        count = 0
        for doc in query:
            produto = doc.to_dict()
            nome = produto.get('nome', 'N/A')
            preco = produto.get('preco', 0.0)
            print(f"ID: {doc.id} | Nome: {nome} | Preco: {preco:.2f}")
            count += 1
        
        if count == 0:
            print("Nenhum produto encontrado")
            
    except exceptions.FirebaseError as e:
        print(f"Erro no Firestore: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")