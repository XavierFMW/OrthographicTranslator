import pdfplumber
import re


class Phoneticizer:

    FILE_ERROR = ValueError("Invalid arguments provided to Phoneticizer.phoneticize()")

    def __init__(self, word_to_phonetic,
                 max_line_length=100,
                 stoppers=".!\?\n",
                 specials="~@#\$%\^&\*/:;-_=\+"
                 ):
        self.word_to_phonetic = word_to_phonetic

        self.max_line_length = max_line_length
        self.stoppers = stoppers
        self.punctuation = stoppers + specials
        self.split_regex = r"[\w']+|[" + self.punctuation + "]"

    def phoneticize(self, *files, file_in=None, file_out=None, from_pdf=False):
        if files:
            for file in files:
                self._phoneticize_file(file, file, from_pdf)

        elif file_in is not None and file_out is not None:
            self._phoneticize_file(file_in, file_out, from_pdf)

        else:
            raise self.FILE_ERROR

    def _phoneticize_file(self, input_path, output_path, from_pdf=False):
        read = self._read_pdf if from_pdf else self._read_txt
        unprocessed = read(input_path)
        processed = self._process_text(unprocessed)
        self._write_txt(output_path, processed)

    @staticmethod
    def _read_txt(file):
        output = ""
        with open(file, "r") as opened:
            for line in opened.readlines():
                output += line
        return output

    @staticmethod
    def _write_txt(file, text):
        with open(file, "w") as opened:
            opened.write(text)

    @staticmethod
    def _read_pdf(file):
        output = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                output += page.extract_text() + "\n\n"
        return output

    def _process_text(self, text):
        output = ""
        previous = ""
        line_length = 0
        for word in (word.lower() for word in re.findall(self.split_regex, text)):
            phonetic = self._get_phonetic_word(word)
            formatted = self._format_word(phonetic, previous, line_length)
            if formatted[0] == "\n":
                line_length = -1
            line_length += len(formatted)
            output += formatted
            previous = formatted
        return output.strip()

    def _get_phonetic_word(self, word):
        return self.word_to_phonetic.setdefault(word, word)

    def _format_word(self, word, previous, line_length):
        output = word
        if previous == "" or previous in self.stoppers:
            output = output.capitalize()
        if previous not in self.punctuation and word not in self.punctuation:
            if line_length >= self.max_line_length:
                output = "\n" + output
            elif line_length > 0:
                output = " " + output
        return output
