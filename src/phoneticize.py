import re


class Phoneticizer:

    def __init__(self, word_to_ipa, one_char_keys, two_char_keys,
                 max_line_length=100, stoppers=".!?", specials=",;\"",
                 ):
        self.word_to_ipa = word_to_ipa
        self.one_char_keys = one_char_keys
        self.two_char_keys = two_char_keys

        self.max_line_length = max_line_length
        self.stoppers = stoppers
        self.specials = specials
        self.punctuation = stoppers + specials
        self.split_regex = r"[\w']+|[" + self.punctuation + "]"

    def update_maps(self, *_,
                    word_to_ipa=None,
                    one_char_keys=None,
                    two_char_keys=None
                    ):
        self.word_to_ipa = self.word_to_ipa if word_to_ipa is None else word_to_ipa
        self.one_char_keys = self.one_char_keys if one_char_keys is None else one_char_keys
        self.two_char_keys = self.two_char_keys if two_char_keys is None else two_char_keys

    def update_formatting(self, *_,
                          max_line_length=None
                          ):
        self.max_line_length = self.max_line_length if max_line_length is None else max_line_length

    def phoneticize(self, *files, file_in=None, file_out=None, from_pdf=False, to_pdf=False):
        if files:
            for file in files:
                self._phoneticize_file(file, file, from_pdf, to_pdf)

        elif file_in is not None and file_out is not None:
            self._phoneticize_file(file_in, file_out, from_pdf, to_pdf)

    def _phoneticize_file(self, input_path, output_path, from_pdf=False, to_pdf=False):
        read = self._read_pdf if from_pdf else self._read_txt
        write = self._write_pdf if to_pdf else self._write_txt
        unprocessed = read(input_path)
        processed = self._process_text(unprocessed)
        write(output_path, processed)

    @staticmethod
    def _read_txt(file):
        output = ""
        with open(file, "r") as opened:
            for line in opened.readlines():
                output += line.replace("\n", " ")
        return output

    @staticmethod
    def _write_txt(file, text):
        with open(file, "w") as opened:
            opened.write(text)

    @staticmethod
    def _read_pdf(file):
        return ""

    def _write_pdf(self, file, text):
        pass

    def _process_text(self, text):
        phoneticized = self._phoneticize_text(text)
        formatted = self._format_words(phoneticized)
        return formatted

    def _phoneticize_text(self, text):
        words = [word.lower() for word in re.findall(self.split_regex, text)]
        output = []
        for word in words:
            phoneticized = self._phoneticize_word(word)
            output.append(phoneticized)
        return output

    def _format_words(self, words):
        line_length = 0
        output = ""
        last = ""
        for word in words:
            if last == "" or last in self.stoppers:
                word = word.capitalize()
            if line_length >= self.max_line_length and last not in self.punctuation and word not in self.punctuation:
                output += "\n"
                line_length = 0
            elif word not in self.punctuation:
                word = " " + word
            output += word
            line_length += len(word)
            last = word
        return output.strip()

    def _phoneticize_word(self, word):
        if word not in self.word_to_ipa.keys():
            return word

        ipa = self.word_to_ipa[word]
        phoneticized = ""
        index = 0
        length = len(ipa)
        while index + 1 < length:
            first = ipa[index]
            second = ipa[index + 1]
            combined = first + second
            if combined in self.two_char_keys.keys():
                phoneticized += self.two_char_keys[combined]
                index += 2
            else:
                phoneticized += self.one_char_keys.setdefault(first, first)
                index += 1

        if index < length:
            final = ipa[index]
            phoneticized += self.one_char_keys.setdefault(final, final)

        return phoneticized
