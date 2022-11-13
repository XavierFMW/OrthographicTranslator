from phonetics import from_ipa, to_ipa
from phoneticize import Phoneticizer


INPUT = "in.txt"
OUTPUT = "out.txt"

TO_IPA = to_ipa.WORD_TO_IPA
ONE_CHAR_KEYS = from_ipa.ONE_CHAR_KEYS
TWO_CHAR_KEYS = from_ipa.TWO_CHAR_KEYS


def main():
    phoneticizer = Phoneticizer(TO_IPA, ONE_CHAR_KEYS, TWO_CHAR_KEYS)
    phoneticizer.phoneticize(file_in=INPUT, file_out=OUTPUT)


if __name__ == "__main__":
    main()
