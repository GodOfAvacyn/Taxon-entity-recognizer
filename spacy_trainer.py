""" ============================================================================
SpaCy Trainer
This is an executable script which trains a fresh spacy model for named entity
recognition. The model is saved to the parent directory in a folder called
taxon_ner_model. The saved model can be run elsewhere. There is also a built-in
function here for evaluation.

Methods:
    train           Trains an NER model for a given number of iterations. Saves
                    the model to a folder 'taxon_ner_model'
    test            Tests our pretrained 'taxon_ner_model' and gives us
                    accuracy, precision, and recall scores.
    demo            Prints out some example named entities in some sentences.

Usage:
The train_spacy method should be run if someone wants to train a fresh
NER model for themselves, to get a feel for the training process.

The test method should be used if someone wants to test the preexisting model
(or one they have just trained) to see the precision, recall, etc.

The demo method can be edited to tag any sentence someone wants to see tagged.
Simply edit the string called 'text' to be any sentence!

The model is saved as 'taxon_ner_model'.
============================================================================ """
import spacy
import sys, getopt
# spacy.require_gpu()
from spacy.lang.en import English
from spacy.training import Example
from spacy.pipeline import EntityRuler
from spacy.util import minibatch, compounding
from spacy.scorer import Scorer

import pandas as pd
import re
import random
import warnings
from os import listdir
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# from copious_loader import create_dataset as cop_create
# from tsv_loader import TSV_LOADER
# from random_loader import create_dataset as rdm_create
from pickle_dump import rand_load
from pickle_dump import cop_load
from pickle_dump import cop_test_load

def train(iterations):
    """
    Defines our spacy loop and spits out a freshly trained model!
    """
    # nlp = spacy.blank("en")
    # nlp = spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_lg')
    # nlp = spacy.load('en_core_web_trf')

    print(nlp.pipe_names)
    if "ner" not in nlp.pipe_names:
        nlp.add_pipe("ner", last=True)

    ner = nlp.get_pipe("ner")
    ner.add_label("TAXON")

    pipe_exceptions = ["ner", "transformer"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    cop_data = cop_load()
    rdm_data = rand_load()
    TRAIN_DATA = cop_data + rdm_data

    with nlp.disable_pipes(*other_pipes):
        # optimizer = nlp.begin_training()
        for itn in range(iterations):
            random.shuffle(TRAIN_DATA)

            print("Starting iteration " + str(itn))
            losses = {}
            i = 0

            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                nlp.update(
                    examples,
                    drop=0.4,
                    # sgd=optimizer,
                    losses=losses
                )
            print(losses)
        nlp.to_disk("../spacy_model")
        return nlp

def test():
    """
    Runs the trained model on a test set of data to check performance.
    """
    # nlp = train_spacy(40)
    # nlp.to_disk("taxon_ner_model")

    nlp = spacy.load("../spacy_model")

    true_pos = 0
    false_pos = 0
    false_neg = 0

    test_data = cop_test_load()

    for text, annotations in test_data:
        pred_ents = [ent.text for ent in nlp(text).ents]
        actual_ents = [ text[ent[0]:ent[1]] for ent in annotations['entities'] ]

        for ent in pred_ents:
            if ent in actual_ents:
                true_pos += 1
            else:
                false_pos += 1
        for ent in actual_ents:
            if ent not in pred_ents:
                false_neg += 1

    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    f_score = 2 * (precision*recall)/(precision+recall)
    print(precision)
    print(recall)
    print(f_score)

    # Current best is 0.85, 0.79, 0.80
    # 483 / 85


def demo(text):
    """
    Provides all taxonomies in a given text
    """
    nlp = spacy.load("../spacy_model")

    pred_ents = [ent.text for ent in nlp(text).ents]
    print(pred_ents)


def detailUsage():
    """
    Details how spacy_trainer needs to be used
    """
    print("Accepted arguments:")
    print("train:   begins the training loop to create a new spacy model.")
    print("test:   runs the trained spacy model on the test data.")
    print("demo sentence_here:   Displays all taxonomies present in a sentence.")
    

def main(argv):
    """
    Main method for the spacy trainer file
    """

    if len(argv) < 1:
        print("At least one command line arg must be supplied.")
        detailUsage()
        return

    if argv[0] == "train":
        train(33)
        return

    if argv[0] == "test":
        test()
        return

    if argv[0] == "demo":
        sent = " ".join(argv[1:])
        demo(sent)
        return

    print("invalid command line args.")
    detailUsage()
    return


# Main method run!
if __name__ == "__main__":
    main(sys.argv[1:])


# train(33)
# test()
# demo()
