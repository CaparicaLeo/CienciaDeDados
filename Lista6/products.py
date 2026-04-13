from firebase_admin import firestore, exceptions

def update_product_price(db, product_id, new_price):
    print(f"\n--- Atualizando Produto ID: {product_id} ---")
    try:
        doc_ref = db.collection('produtos_mysql').document(str(product_id))
        
        doc_ref.update({
            'preco': new_price,
            'ultima_atualizacao': firestore.SERVER_TIMESTAMP # Boa prática: salvar quando mudou
        })
        
        print(f"✅ Sucesso: Produto {product_id} atualizado para R$ {new_price:.2f}")

    except exceptions.FirebaseError as e:
        print(f"Erro ao atualizar no Firestore: {e}")
    except Exception as e:
        print(f" Ocorreu um erro inesperado: {e}")

# Exemplo de chamada (assumindo que 'db_client' já foi inicializado)
# update_product_price(db_client, 101, 29.90)