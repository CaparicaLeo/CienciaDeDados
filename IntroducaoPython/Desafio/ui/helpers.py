def linha():
    print("-" * 50)

def titulo(texto: str):
    linha()
    print(f"  {texto}")
    linha()

def pausar():
    input("\n  [Enter para continuar]")

def menu(opcoes: dict) -> str:
    """Exibe um dicionário {chave: descrição} e retorna a opção digitada."""
    for k, v in opcoes.items():
        print(f"  [{k}] {v}")
    return input("\n  Opção: ").strip()