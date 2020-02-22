import argparse
import sys
from string import punctuation as puc
from nltk.stem import PorterStemmer

#this loads the dictionary into a set
def load_dictionary(dict,ps):
    try:
        fp = open(dict, mode="r")
        my_set = set(ps.stem(line.strip()) for line in fp)

    except FileNotFoundError:
        print("dictionary file not found")
        sys.exit(-1)

    fp.close()
    return my_set

#this function writes misspelled words into file
def write_misspelled(mylist):
    with open("misspelled.txt", "w") as fp:
        fp.write("Misspelled words are:\n")
        for word in mylist:
            fp.write("%s\n" % word)

#cleaning a sentence
def clean_data(line_to_clean):
    cleaned_line = line_to_clean.lower()
    cleaned_line = cleaned_line.translate(str.maketrans("", "", puc))
    cleaned_line = cleaned_line.translate(str.maketrans("", "", "1234567890"))
    return cleaned_line


def main(args):
    print("Please wait while building the dictionary")
    dict_name = "dictionary.txt"
    ps = PorterStemmer()
    my_set = load_dictionary(dict_name,ps)
    misspelled_list = []

    try:
        fp = open(args, "r")
        for line in fp.readlines():
            line = clean_data(line)
            for word in line.split():
                word_to_write=word
                word = ps.stem(word)
                if word not in my_set:  
                    misspelled_list.append(word_to_write)
        if len(misspelled_list) == 0:
            print("all words are correctly spelled!")
            sys.exit(0)
        else:
            print("%d Misspelled words are in misspelled.txt" % (len(misspelled_list)))

    except FileNotFoundError:
        print("file not found check again please")
        sys.exit(-1)

    fp.close()
    write_misspelled(misspelled_list)
    sys.exit(0)


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(
        description="Takes as input a txt file, returns misspelled words in misspelled.txt")
    my_parser.add_argument("input_file", help="your input file", action="store", type=str)
    args = my_parser.parse_args()
    main(args.input_file)
