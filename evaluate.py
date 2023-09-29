
import os
import argparse
import json
from difflib import SequenceMatcher
import re

parser = argparse.ArgumentParser(description='Generate a prompt for a given paper and table.')
parser.add_argument('--true_json', type=str, help='Path to the prompt file.')
parser.add_argument('--pred_json', type=str, help='Path to the paper file.')
parser.add_argument('--paper_folder', type=str, help='Path to the paper file.', default="/usr/project/xtmp/gk126/nlp-for-materials/nlp-for-materials/data_processing/splitted_papers")
args = parser.parse_args()

def scores(correct, false_positive, false_negative):
    print("Correct: ", correct)
    print("False Positive: ", false_positive)
    print("False Negative: ", false_negative)
    
    # compute f1
    if correct + false_positive == 0:
        precision = 0
    else:
        precision = correct / (correct + false_positive)
    if correct + false_negative == 0:
        recall = 0
    else:
        recall = correct / (correct + false_negative)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return f1, precision, recall

def eval(true_json, pred_json):

    false_positive = 0
    false_negative = 0
    correct = 0
    bad_table = False
    
    true_json = json.load(open(true_json))
    try:
        pred_json = json.load(open(pred_json))
        # catch any errors
    except json.decoder.JSONDecodeError:
        bad_table = True
        return None, None, None, bad_table
    
    true_matrix = true_json["matrix_chemical"]
    try:
        pred_matrix = pred_json["Matrix Chemical Name"]
    except KeyError:
        bad_table = True
        return None, None, None, bad_table
    

    true_matrix = true_matrix.lower()
    true_matrix = re.sub(r'[^a-z]', '', true_matrix)
    pred_matrix = pred_matrix.lower()
    pred_matrix = re.sub(r'[^a-z]', '', pred_matrix)
    true_matrix = true_matrix.replace(" ", "")
    pred_matrix = pred_matrix.replace(" ", "")

    # if true_matrix and pred_matrix are match more than 80% then it is correct
    if SequenceMatcher(None, true_matrix, pred_matrix).ratio() > 0.8:
        correct += 1
    else:
        false_negative += 1
        false_positive += 1
    
    true_processing = true_json["processing_method"]
    try:
        pred_processing = pred_json["Processing Method"]
    except KeyError:
        bad_table = True
        return None, None, None, bad_table

    true_processing = true_processing.lower()
    true_processing = re.sub(r'[^a-z]', '', true_processing)
    pred_processing = pred_processing.lower()
    pred_processing = re.sub(r'[^a-z]', '', pred_processing)
    true_processing = true_processing.replace(" ", "")
    pred_processing = pred_processing.replace(" ", "")

    if true_processing == pred_processing:
        correct += 1
    else:
        false_negative += 1
        false_positive += 1
    
    true_char = true_json["char_section"]
    try:
        pred_char = pred_json["Characterization"]
    except KeyError:
        bad_table = True
        return None, None, None, bad_table
    
    true_char = true_char.lower()
    true_char = re.sub(r'[^a-z]', '', true_char)
    pred_char = pred_char.lower()
    pred_char = re.sub(r'[^a-z]', '', pred_char)
    true_char = true_char.replace(" ", "")
    pred_char = pred_char.replace(" ", "")

    if true_char in pred_char:
        correct += 1
    else:
        false_negative += 1
        false_positive += 1

    return correct, false_negative, false_positive, bad_table

if __name__ == "__main__":
    
    # go through the true_json folder
    # for each file, find the corresponding file in the pred_json folder
    # compute the f1 score
    # print the f1 score
    false_positives = 0
    false_negatives = 0
    corrects = 0
    bad_tables = 0
    total = 0
    true_jsons = os.listdir(args.true_json)
    pred_jsons = os.listdir(args.pred_json)
    already_processed = []
    for file in true_jsons:
        # print(file)
        # get the first 4 characters of the file name
        whole_file = file
        file = file[:4]

        if f"{file}_whole.txt" in pred_jsons:
            
            total += 1
            # get the corresponding file in the pred_jsons
            pred = [f for f in pred_jsons if file in f][0]
            correct, false_negative, false_positive, bad_table = eval(f"{args.true_json}/{whole_file}", f"{args.pred_json}/{pred}")
            if bad_table:
                bad_tables += 1
                continue
            else:
                corrects += correct
                false_negatives += false_negative
                false_positives += false_positive
          
        else:
            continue

    f1, precision, recall = scores(corrects, false_positives, false_negatives)
    print("Bad Tables: ", bad_tables/total)
    print("F1: ", f1)
    print("Precision: ", precision)
    print("Recall: ", recall)


    

