import re


IPA_FILE = "en_US_ipa.txt"
OUTPUT_FILE = "to_ipa.py"

DICT_NAME = "WORD_TO_IPA"
REMOVED_CHARS = "/ˈˌ,"
SPLIT_REGEX = r"[ \t]"

HEADER_FORMAT = "\n%s = {\n"
MAPPING_FORMAT = '\t"%s": "%s",\n'
FOOTER_FORMAT = "}\n"


def get_mapping_from_line(line):
    unzipped = re.split(SPLIT_REGEX, line)
    key = unzipped[0]
    value = unzipped[1].strip().translate(
        {ord(i): None for i in REMOVED_CHARS}
    )
    return MAPPING_FORMAT % (key, value)


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
