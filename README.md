# Taxon Entity Recognizer
## REQUIREMENTS
- pandas
- pickle
- numpy
- random
- re
- spacy
- spacy trf

## DESCRIPTION
This project is for recognizing taxonomic entities in scientific text. It trains on a combination of
existing exerpts from scientific papers and synthetic data from combining taxonomies from a list and
handwritten sentences.  
The data currently is in the form of three pickle documents. Since the original, unprocessed dataset
exceeds 100mb, it cannot be uploaded to github.

## USAGE
The only interactable file is spacy_trainer.py. There are three supported command line arguments:
- train:   trains the model and saves it to the parent folder. This will take some time.
- test:   runs the model on a set of test data and displays accuracy parameters.
- demo sentence_here:   displays all taxonomies from a sentence. "sentence_here" can be as long as needed.  
Unfortunately, since the trained model exceeds 100mb, previously trained models cannot be uploaded to github.
If training with a GPU, edit the 2nd line of the spacy_trainer.py file and un-comment "require.gpu()".
