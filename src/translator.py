# Orthographic Translator - A program that converts texts between writing systems while maintaining word pronunciation.
# Copyright 2022 Xavier Mercerweiss, xavifmw@gmail.com. Licensed under the MIT License.

import pdfplumber
import re


class Translator:
    """
    Replaces each word within a piece of text with a word mapped to it, then formats the output.

    :param mapping: A dictionary mapping a series of words with their replacements.
    :param capitalize: Whether the first character of each sentence will be capitalized.
    :param break_lines: Whether the output will be broken into several lines if the maximum line length is exceeded.
    :param max_line_length: The maximum line length of the output.
    :param delimiter: The character inserted between each word of the output.
    :param stoppers: The text characters recognized as sentence stoppers within the output, formatted as a regex string.
    :param specials: The text characters recognized as punctuation marks but not sentence stoppers within the output,
        formatted as a regex string.
    """

    def __init__(self, mapping,
                 capitalize=True,
                 break_lines=True,
                 max_line_length=100,
                 delimiter=" ",
                 stoppers=".!\?\n",
                 specials="~@#\$%\^&\*/:;-_=\+"
                 ):
        self.mapping = mapping
        self.capitalize = capitalize
        self.break_lines = break_lines
        self.max_line_length = max_line_length
        self.delimiter = delimiter
        self.stoppers = stoppers
        self.specials = specials
        self.__punctuation = stoppers + specials
        self.__kept_regex = r"[\w']+|[" + self.__punctuation + "]"

    def __getattr__(self, item):
        if item == "stoppers" or item == "specials":
            return ""
        msg = f"{repr(type(self).__name__)} has no attribute {repr(item)}"
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "stoppers" or name == "specials":
            self.__punctuation = self.stoppers + self.specials
            self.__kept_regex = r"[\w']+|[" + self.__punctuation + "]"

    def translate(self, text):
        """
        Replaces each word within the given text with its mapped counterpart and formats the output.

        :param text: The text to be translated.
        :return: The translated text.
        """
        return self._process_text(text)

    def translate_file(self, input_path, output_path=None, from_pdf=False):
        """
        Replaces each word within the text from a given TXT or PDF file with its mapped counterpart, formats the
        output, and saves it to a given TXT file.

        :param input_path: The path to a TXT or PDF file containing the text to be converted.
        :param output_path: The path to a TXT file to which the output will be saved.
        :param from_pdf: Whether the input file is a PDF file.
        :return: If no output path is provided, the processed text will be directly returned.
        """
        read = self._read_pdf if from_pdf else self._read_txt
        unprocessed = read(input_path)
        processed = self._process_text(unprocessed)
        if output_path is None:
            return processed
        self._write_txt(output_path, processed)

    @staticmethod
    def _read_txt(file):
        """
        Reads the text of a given TXT file.

        :param file: The path of the file.
        :return: The text of the file.
        """
        output = ""
        with open(file, "r") as opened:
            for line in opened.readlines():
                output += line
        return output

    @staticmethod
    def _write_txt(file, text):
        """
        Overwrites the contents of a given TXT file.

        :param file: The path of the file.
        :param text: The text to be written.
        """
        with open(file, "w") as opened:
            opened.write(text)

    @staticmethod
    def _read_pdf(file):
        """
        Reads the text of a given PDF file.

        :param file: The path of the file.
        :return: The text of the file.
        """
        output = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                output += page.extract_text() + "\n\n"
        return output

    def _process_text(self, text):
        """
        Replaces each word within the text from a given TXT or PDF file with its mapped counterpart, then formats and
        returns the output.

        :param text: The text to be processed and formatted.
        :return: The processed and formatted text.
        """
        output = ""
        previous = ""
        line_length = 0
        for word in (word.lower() for word in re.findall(self.__kept_regex, text)):
            phonetic = self._get_mapped_word(word)
            formatted = self._format_word(phonetic, previous, line_length)
            if formatted[0] == "\n":
                line_length = -1
            line_length += len(formatted)
            output += formatted
            previous = formatted
        return output.strip()

    def _get_mapped_word(self, word):
        """
        Returns the word mapped to the given word if such a mapping exists. Otherwise, returns the given word.

        :param word: The word to have its mapping returned.
        :return: The word mapped to the given word.
        """
        return self.mapping.setdefault(word, word)

    def _format_word(self, word, previous, line_length):
        """
        Formats a given word according to both the context of the text around it and the given formatting rules.

        :param word: The word to be formatted.
        :param previous: The word preceding the given word within the text.
        :param line_length: The length of the current line within the output.
        :return: The formatted word.
        """
        output = word
        if self.capitalize and previous == "" or previous in self.stoppers:
            output = output.capitalize()
        if previous not in self.specials and word not in self.__punctuation:
            if self.break_lines and line_length >= self.max_line_length:
                output = "\n" + output
            elif line_length > 0:
                output = self.delimiter + output
        return output
