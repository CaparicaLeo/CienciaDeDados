import firebase_admin
from firebase_admin import credentials, auth, exceptions

def create_user_with_error_handling(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        print(f"Usuario criado: {user.uid}")
        
    except exceptions.AlreadyExistsError:
        print("Erro: Este e-mail ja esta cadastrado")
    except exceptions.InvalidArgumentError:
        print("Erro: Argumentos invalidos (e-mail malformado ou senha fraca)")
    except exceptions.InternalError:
        print("Erro: Problema interno no servidor do Firebase")
    except exceptions.FirebaseError as e:
        print(f"Erro no Firebase Admin SDK: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        create_user_with_error_handling("teste_excecao@exemplo.com", "senha123")
    except Exception as e:
        print(f"Erro ao inicializar o SDK: {e}")