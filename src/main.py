# Orthographic Translator - A program that converts texts between writing systems while maintaining word pronunciation.
# Copyright 2022 Xavier Mercerweiss, xavifmw@gmail.com. Licensed under the MIT License.

from ipa_to_orthography import orthography
from translator import Translator


INPUT = "in.txt"
OUTPUT = "out.txt"
FROM_PDF = False


def main():
    translate = Translator(orthography.MAPPING)
    translate.translate_file(INPUT, OUTPUT, FROM_PDF)


if __name__ == "__main__":
    main()
