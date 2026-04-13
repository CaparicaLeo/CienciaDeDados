from firebase_admin import messaging, exceptions

def send_test_notification(topic):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title='Notificacao teste',
                body='Mensagem do Admin SDK',
            ),
            topic=topic,
        )
        response = messaging.send(message)
        print(f"Mensagem enviada: {response}")
    except exceptions.FirebaseError as e:
        print(f"Erro no Messaging: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    send_test_notification("geral")