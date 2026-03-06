from collections import Counter

def examine_phrase(phrase):
    words = phrase.split()
    return Counter(words).most_common(3)

if __name__ == "__main__":
    phrase = input("Digite uma frase: ")
    print(examine_phrase(phrase))
    