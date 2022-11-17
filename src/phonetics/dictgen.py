from from_ipa import *
import re


IPA_FILE = "en_US_ipa.txt"
OUTPUT_FILE = "phonetic_words.py"

DICT_NAME = "WORD_TO_PHONETIC"
REMOVED_CHARS = "/ˈˌ,"
SPLIT_REGEX = r"[ \t]"

HEADER_FORMAT = "\n%s = {\n"
MAPPING_FORMAT = '\t"%s": "%s",\n'
FOOTER_FORMAT = "}\n"


def get_phonetic_from_ipa(ipa):
    phoneticized = ""
    index = 0
    length = len(ipa)
    while index < length:
        increment = index + 1
        head = ipa[index]
        if increment == length or head + ipa[increment] not in TWO_CHAR_KEYS.keys():
            phoneticized += ONE_CHAR_KEYS.setdefault(head, head)
            index += 1
        else:
            tail = ipa[increment]
            phoneticized += TWO_CHAR_KEYS[head + tail]
            index += 2

    return phoneticized


def get_mapping_from_line(line):
    unzipped = re.split(SPLIT_REGEX, line)
    word = unzipped[0]
    ipa = unzipped[1].strip().translate(
        {ord(i): None for i in REMOVED_CHARS}
    )
    phoneticized = get_phonetic_from_ipa(ipa)
    return MAPPING_FORMAT % (word, phoneticized)


def main():

    with open(OUTPUT_FILE, "w") as output:
        output.write(HEADER_FORMAT % DICT_NAME)
        with open(IPA_FILE, "r") as ipa:
            for line in ipa.readlines():
                mapping = get_mapping_from_line(line)
                output.write(mapping)
        output.write(FOOTER_FORMAT)


if __name__ == "__main__":
    main()
