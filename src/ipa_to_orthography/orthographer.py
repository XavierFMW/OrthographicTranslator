# Orthographic Translator - A program that converts texts between writing systems while maintaining word pronunciation.
# Copyright 2022 Xavier Mercerweiss, xavifmw@gmail.com. Licensed under the MIT License.

from from_ipa import *
import re


INPUT_FILE = "en_US_ipa.txt"
OUTPUT_FILE = "orthography.py"

DICT_NAME = "MAPPING"
REMOVED_CHARS = "/ˈˌ,"
SPLIT_REGEX = r"[ \t]"

HEADER_FORMAT = "\n%s = {\n"
MAPPING_FORMAT = '\t"%s": "%s",\n'
FOOTER_FORMAT = "}\n"


class Orthographer:
    """
    Produces a Python dictionary mapping each word of a language with its equivalent written in a given orthography.
    The aforementioned orthography exists in the dictionaries pasted to the class on instantiation, each of which
    should map a given sound expressed using the International Phonetic Alphabet (IPA) with an equivalent string of
    characters.

    :param from_ipa_one: A dictionary mapping every sound represented by a single character within the IPA
        with an equivalent string of text.
    :param from_ipa_two: A dictionary mapping every sound represented by two characters within the IPA
        with an equivalent string of text.
    :param removed: A string containing every character to be removed from each line of the input file during
        processing.
    :param delimiter: A regex string containing the text along which each line of the input file is to be split.
    :param header: The format of the opening line of the output Python dictionary.
    :param mapping: The format of each content line of the output Python dictionary.
    :param footer: The format of the closing line of the output Python dictionary.
    """

    def __init__(self, from_ipa_one=ONE_CHAR_KEYS, from_ipa_two=TWO_CHAR_KEYS,
                 removed=REMOVED_CHARS, delimiter=SPLIT_REGEX,
                 header=HEADER_FORMAT, mapping=MAPPING_FORMAT, footer=FOOTER_FORMAT
                 ):
        self.from_ipa_one = from_ipa_one
        self.from_ipa_two = from_ipa_two
        self.removed = removed
        self.delimiter = delimiter
        self.header = header
        self.mapping = mapping
        self.footer = footer

    def generate_orthography(self, path_in, path_out, dict_name=DICT_NAME):
        """
        Given a text file mapping a series of words with their pronunciations expressed in the International Phonetic
        Alphabet (IPA), a Python dictionary is generated mapping each word to its equivalent in the given
        orthography within the output file.

        :param path_in: The path of the input file.
        :param path_out: The path of the output file.
        :param dict_name: The name of the output Python dictionary.
        """
        with open(path_out, "w") as output:
            output.write(HEADER_FORMAT % dict_name)
            with open(path_in, "r") as ipa:
                for line in ipa.readlines():
                    mapping = self._get_mapping_from_line(line)
                    output.write(mapping)
            output.write(FOOTER_FORMAT)

    def _get_mapping_from_line(self, line):
        """
        Given a line of text containing both a word and its pronunciation expressed in the International Phonetic
        Alphabet (IPA), a line of text mapping the word to its equivalent in the given orthography within a Python
        dictionary.

        :param line: The line of text to be converted into a mapping.
        :return: A line of text mapping a word to its equivalent in the given orthography within a Python
            dictionary.
        """
        unzipped = re.split(self.delimiter, line)
        old = unzipped[0]
        ipa = unzipped[1].strip().translate(
            {ord(i): None for i in self.removed}
        )
        new = self._ipa_to_new(ipa)
        return self.mapping % (old, new)

    def _ipa_to_new(self, ipa):
        """
        Given a string of letters from the International Phonetic Alphabet (IPA), a word with an equivalent
        pronunciation is created using the given orthography.

        :param ipa: A string of letters from the IPA.
        :return: A word written in the given orthography with a pronunciation equivalent to that of the given IPA
            characters.
        """
        output = ""
        index = 0
        length = len(ipa)
        while index < length:
            increment = index + 1
            head = ipa[index]
            if increment == length or head + ipa[increment] not in self.from_ipa_two.keys():
                output += self.from_ipa_one.setdefault(head, head)
                index += 1
            else:
                tail = ipa[increment]
                output += self.from_ipa_two[head + tail]
                index += 2

        return output


if __name__ == "__main__":
    orthographer = Orthographer()
    orthographer.generate_orthography(INPUT_FILE, OUTPUT_FILE)
