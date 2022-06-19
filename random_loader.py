""" ============================================================================
Random Loader
This is a class file which loads data from the corpus-species databank and
turns it into data that is right for SpaCy to use - meaning data of the form
(text, {entities: [ (start,end,label) ]})

The data is built from 15 handwritten sentences, as well as a database of over
900 unique taxonomies. The RANDOM_LOADER class builds dataframes by randomly
selecting taxonomies and filling in <TAXON> tags in the 15 handwritten
sentences.

Usage: none on its own.
============================================================================ """

import pandas as pd
import pickle
import numpy as np
import random
import re

PICK = "../data/pickle/random.pickle"

def load_taxons(file_name, taxon_col_name):
    """
    Fetches taxonomy names from data
    INPUTS: File_name (name of a file), taxon_col_name (name of taxonomy column)
    OUTPUTS: list of taxonomy names.
    """

    data = pd.read_csv(file_name)
    return data[taxon_col_name].to_list()


def load_sentences(file_name):
    """
    Retrievs dummy example sentences from a text file.
    """
    lines = []
    with open(file_name) as f:
        lines = f.readlines()
    stripped = []
    for line in lines:
        if (line == 'EOF'): break
        stripped.append(line.strip())
    return stripped


def remove_duplicates(taxons):
    """
    Clears a list of duplicate elements.
    """

    dummy_dict = {}
    for name in taxons:
        if name not in dummy_dict:
            dummy_dict[name] = 0
    return [item[0] for item in dummy_dict.items()]


def get_better_taxons(taxons):
    """
    Abbreviates the first word of the taxons.
    """

    new_taxons = []
    for taxon in taxons:
        new_taxon = taxon.split()
        if len(new_taxon) == 2:
            new_taxon[0] = str(new_taxon[0][0]) + "."
            new_taxons.append(" ".join(new_taxon))
    return new_taxons


def create_data_from_sentence(text, bag):
    """
    Takes in a sentence and outputs: (text, {"entities": [(start, end, label)]})
    for EACH taxon inside the bag.
    """

    token = "<TAXON>"
    label = "TAXON"
    datapoints = []

    match = re.search(token, text)
    start = match.span()[0]
    for word in bag:
        end = match.span()[1] - len(token) + len(word)
        sent = re.sub(token, word, text, count=1)
        datapoints.append( (sent, {"entities": [(start,end,label)]}) )

    return datapoints


def create_dataset(taxon_file="../data/gene_result.csv", col_name='Org_name', sentence_file="../data/sentences.txt"):
    """
    Creates a list of training data of the form:
    [ (text, {"entities": [(start, end, label)]}) ]
    """

    taxons = remove_duplicates( load_taxons(taxon_file, col_name) )
    taxons.extend( get_better_taxons(taxons) )
    sentences = load_sentences(sentence_file)
    train_data = []

    for sent in sentences:
        train_data.extend( create_data_from_sentence(sent, taxons) )

    return(train_data)