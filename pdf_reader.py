import sys
import warnings
warnings.filterwarnings("ignore")
import PyPDF2
from taxonerd import TaxoNERD


def pdf_to_str(pdf_path):
    """
    Converts a pdf document to one large string.
    """
    pdf = open(pdf_path, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdf)
    x = pdfreader.numPages
    text = " "
    for i in range(x):
        text += pdfreader.getPage(i).extractText()
    myList = text.split("\n")
    text = " ".join(myList)
    return text


def get_taxons(document):
    """
    Gets all taxonomic mentions from a string.
    """
    ner = TaxoNERD(model="en_ner_eco_biobert", prefer_gpu=False, with_abbrev=False)
    table = ner.find_in_text(document)
    output = []
    for col in table['text']:
        output.append(str(col))
    return output


def get_most_common_taxons(taxons):
    """
    Returns the (up to) three most common taxons from a list.
    """
    taxon_dict = {}
    for taxon in taxons:
        if taxon not in taxon_dict:
            taxon_dict[taxon] = 1
        else:
            taxon_dict[taxon] += 1
    items = list(taxon_dict.items())
    items = sorted(items, key=lambda item: item[1])
    return [item[0] for item in items[0:3]]


def detailUsage():
    """
    Displays usage of document in the command line.
    """
    print("Usage:")
    print("python pdf_taxon_extractor.py <PATH TO PDF DOC>")


def main(argv):
    """
    Main method.
    """
    if len(argv) != 1:
        print("Illegal number of arguments.")
        detailUsage()
    document = pdf_to_str(argv[0])
    taxons = get_taxons(document)
    most_common = get_most_common_taxons(taxons)
    print("Most common taxonomic mentions: ", most_common)


# Main method run!
if __name__ == "__main__":
    main(sys.argv[1:])