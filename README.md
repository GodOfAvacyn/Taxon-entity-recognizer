# Taxon Entity Recognizer

## DESCRIPTION
This project is for recognizing taxonomic entities in scientific text. It currently uses the TaxoNERD library as its internal named entity recognizer. The main file inside is pdf_reader.py, which takes in a path to a pdf document and spits out the most commonly mentioned taxonomic names inside the docuemnt.

## USAGE
The file pdf_reader.py is used like this:
- python pdf_reader.py <PATH TO PDF DOCUMENT>
The output will be a printed message inside the terminal of the most commonly referenced taxonomies.
