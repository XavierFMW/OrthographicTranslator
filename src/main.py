from phonetics import phonetic_words
from phoneticize import Phoneticizer


INPUT = "in.txt"
OUTPUT = "out.txt"


def main():
    phoneticizer = Phoneticizer(phonetic_words.WORD_TO_PHONETIC)
    phoneticizer.phoneticize(file_in=INPUT, file_out=OUTPUT)


if __name__ == "__main__":
    main()
