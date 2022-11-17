# PhoneticEnglish
This program allows any piece of English text into a custom made fully phonetic English writing system. All words are pronounced exactly the same, they are merely written in a way which fully reflects their pronunciation.

## Implementation
 
### Dictgen
Dictgen, a script residing within the `phonetics` directory, will convert any text file containing tab-delimited IPA data into a Python dictionary mapping every lowercase English word with its equivalent within the phonetic writing system, with the phoneticized version based on the IPA data provided. The IPA data for US English is provided with this program, as well as a dictionary of phoneticized words based on that data. This data was sourced from <https://github.com/open-dict-data/ipa-dict>, and many thanks are given to that project's contributors.

### Phoneticizer
The Phoneticizer class, provided with a mapping between English words and their phonetic counterparts, will convert text from a provided TXT or PDF file into the phonetic English writing system, automatically format the output, and save the output to a TXT file. Formatting may not be perfect, however formatting settings, such as maximum line length, capitalization, sentence stoppers, and special characters, may be altered at the disgression of the user.

## The Phonetic Writing System
The phonetic English writing system described above attempts to map every sound, as present in American English, to a single letter with which that sound may be written. This writing system aims to reduce the ambiguity present in English pronunciation and streamline the writing process. 

NOTE: This writing system was created by an American living in Colorado, and therefore will reflect the accent present in that region. Many sounds which may be distinct in other accents, especially vowels, have been deliberately condensed such that they reflect the accent of the creator. The phonology and orthogrophy of this writing system may need to be drastically altered to match your speech!

This writing system utilizes the following orthogrophy.

### Vowels

| Letter | US IPA Symbol | Sound |
|:---:|:---:|:---:|

 
## Changelog
# Version 1.0
- Project released.
