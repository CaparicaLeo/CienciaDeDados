from firebase_admin import storage, exceptions

def upload_file_content(filename, content):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_string(content, content_type='text/plain')
        print(f"Arquivo {filename} enviado com sucesso")
    except exceptions.FirebaseError as e:
        print(f"Erro no Storage: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    upload_file_content("meu_arquivo.txt", "Olá, Firebase Storage!")