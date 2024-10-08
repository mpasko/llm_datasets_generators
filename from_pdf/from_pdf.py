from functools import reduce
import fitz
import argparse
import sys
import os

from os import listdir
from os.path import isfile, isdir, join

duplicates = set()

def cut_references(page_lines):
    references_index = page_lines.lower().rfind("references")
    cut_refs = page_lines[0: references_index]
    return cut_refs

def contains_banned_words(line, *args):
    for word in args:
        if line.lower().find(word.lower()) >= 0:
            return True
    return False

def line_filter(line):
    length_satisfied = len(line) >= 40
    not_encoded = line.find(" ") > 1
    not_banned = not contains_banned_words(line, "{{", "}}", "arxiv", "conference", "pages", "url")
    text_to_coma_rate = len(line) / (line.count(",") + line.count(".") + 1)
    coma_rate_satisfied = text_to_coma_rate >= 20
    not_in_duplicates = not line in duplicates
    duplicates.add(line)
    return length_satisfied and not_encoded and not_banned and coma_rate_satisfied and not_in_duplicates

def clean_each_line(cut_refs):
    page_lines = cut_refs.splitlines()
    clean_lines = (line.strip() for line in page_lines)
    filter_lines = (line for line in clean_lines if line_filter(line))
    clean_text = "\n".join(filter_lines)
    return clean_text

def clean_lines(text):
    cut_refs = cut_references(text)
    clean_text = clean_each_line(cut_refs)
    return clean_text

def load_page(pdf, page_number):
    page = pdf[page_number]
    page_lines = page.get_text()
    page_text = clean_lines(page_lines)
    return page_text

def parse_arguments():
    parser = argparse.ArgumentParser(description="A Python script to extract text from PDF documents.")
    parser.add_argument("base", help="Base directory")
    args = parser.parse_args()
    base_path = args.base
    return base_path

def load_text_from_pdf(load_page, pdf):
    pages = (load_page(pdf, page_number) for page_number in range(pdf.page_count))
    pdf_text = "\n".join(pages)
    return pdf_text

def traverse(base_path):
    absolute_paths = [join(base_path, file) for file in listdir(base_path)]
    yield from (path for path in absolute_paths if isfile(path) and path.find('.pdf') >= 0)
    subdir_generatorss = (traverse(path) for path in absolute_paths if isdir(path))
    subfiles = [file for files in subdir_generatorss for file in files]
    yield from subfiles

base_path = parse_arguments()
onlyfiles = list(traverse(base_path))
pdfs = (fitz.open(input_file) for input_file in onlyfiles)
texts = (load_text_from_pdf(load_page, pdf) for pdf in pdfs)

for text in texts:
    print("")
    print("----------------------")
    print(text)
