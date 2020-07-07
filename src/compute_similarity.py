#!/usr/bin/env python3
import math
import csv
import statistics
import string
from threading import Thread
import sys
import os
from zipfile import ZipFile

T = 0.6
EXTENSION_FOR_ANALYSIS = ['.html','.js','.vbs','.xls','.xlsm','.doc','.docm', '.ps1','.bat','.psm1', '.psd1','.psh','.sh']
OUTPUT_FILE =  'stats/similarity.csv'
RAW_FOLDER = 'raw/'
TEMP_FOLDER = '/tmp/tt'

# Walk a specific path and returns all the zip files
def walkAndGetExtensionPath(path, extension=".zip"):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith(extension):
                yield os.path.join(dirpath, filename)

# Extracts Zip files based on EXTENSION_FOR_ANALYSIS. It returns the etire file
# path for future works
def extractZipAndReturnsIntereistingFiles(file_to_extract):
    interesting_files = []
    n_interesting_files = []
    try:
        with ZipFile(file_to_extract, 'r') as zipObj:
            listOfFileNames = zipObj.namelist()
            for fileName in listOfFileNames:
                for ext in EXTENSION_FOR_ANALYSIS:
                    if fileName.endswith(ext):
                        try:
                            zipObj.extract(fileName, TEMP_FOLDER)
                            interesting_files.append(os.path.join(TEMP_FOLDER, fileName))
                        except Exception as e:
                            continue
                    else:
                        n_interesting_files.append(os.path.join(TEMP_FOLDER, fileName))
    except Exception as e :
        return interesting_files
    return interesting_files

# This is the interface function for calculating a simple code similarity.
# Code similarity rif: https://www.geeksforgeeks.org/measuring-the-document-similarity-in-python/
def documentSimilarity(filename_1, filename_2, score):
    def read_file(filename):
        try:
            with open(filename, 'r') as f:
                data = f.read()
            return data
        except IOError:
            print("Error opening or reading input file: ", filename)
            sys.exit()

    translation_table = str.maketrans(string.punctuation+string.ascii_uppercase,
                                         " "*len(string.punctuation)+string.ascii_lowercase)
    def get_words_from_line_list(text):

        text = text.translate(translation_table)
        word_list = text.split()

        return word_list
    def count_frequency(word_list):

        D = {}

        for new_word in word_list:

            if new_word in D:
                D[new_word] = D[new_word] + 1

            else:
                D[new_word] = 1

        return D
    def word_frequencies_for_file(filename):

        line_list = read_file(filename)
        word_list = get_words_from_line_list(line_list)
        freq_mapping = count_frequency(word_list)

        #print("File", filename, ":", )
        #print(len(line_list), "lines, ", )
        #print(len(word_list), "words, ", )
        #print(len(freq_mapping), "distinct words")

        return freq_mapping
    def dotProduct(D1, D2):
        Sum = 0.0

        for key in D1:

            if key in D2:
                Sum += (D1[key] * D2[key])

        return Sum
    def vector_angle(D1, D2):
        numerator = dotProduct(D1, D2)
        denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2))
        try:
            r = math.acos(numerator / denominator)
            return r
        except Exception as e:
            return None


    sorted_word_list_1 = word_frequencies_for_file(filename_1)
    sorted_word_list_2 = word_frequencies_for_file(filename_2)
    distance = vector_angle(sorted_word_list_1, sorted_word_list_2)
    if distance:
        score.append(distance)
    return True

# Saving the result_array into a Comma Separated Virgula file for better
# analyses (ie. importing on a spreadsheet)
def saveToCSV(result_array):
    with open(OUTPUT_FILE, 'w', newline="") as r:
        wr = csv.writer(r)
        wr.writerows(result_array)



# Main activation and initial steps begin here
analysis_list = []
results = []

# It's the simple CSV header.
results.append(['FileA', 'FileB', 'SimilarityAVG', 'SimilarityMin', 'SimilarityMax'])

# For for analyzing ZIP files
for f_to_analyze in walkAndGetExtensionPath(RAW_FOLDER, ".zip"):
    print("[*] Working on: %s" % f_to_analyze)
    i_f = extractZipAndReturnsIntereistingFiles(f_to_analyze)
    analysis_list.append({'file_name':str(f_to_analyze), 'VIF': i_f})

#TODO: analyzing RAR, GZ and TAR archives
# Still to implement it
# ......

print("[*] Starting Comparing Archives")
# Comparing Archives by a super stuping o(MXN) cicle. It actually takes
# forever, need to be upgraded
for a in analysis_list:
   for b in analysis_list:
        if a['file_name'] == b['file_name']:
            continue
        else:
            score = []
            ts = []
            print("[*] Comparing %s to %s" % (a['file_name'], b['file_name']))
            for vif_a in a['VIF']:
                for vif_b in b['VIF']:
                    try:
                        # Let's threadize the internal similarity checks
                        t = Thread(target=documentSimilarity, args=[vif_a, vif_b, score])
                        t.start()
                        ts.append(t)
                    except Exception as r:
                        continue
        print("[+] Waiting for %s processes" % len(ts))
        # For each archive comparison, let's parallelize similarity checks, but
        # before get into another file wait the first finishes.
        for t in ts:
            t.join()

        if len(score) > 0:
            results.append([a['file_name'], b['file_name'], statistics.mean(score), min(score), max(score)])
            print("[!] %s - %s: average( %s )" % (a['file_name'], b['file_name'], statistics.mean(score)))
            print("[!] %s - %s: min( %s )" % (a['file_name'], b['file_name'], min(score)))
            print("[!] %s - %s: max( %s )" % (a['file_name'], b['file_name'], max(score)))
        else:
            print("[!] %s - %s: average( NaN )" % (a['file_name'], b['file_name']))

saveToCSV(results)
print("Similarities saved to: " + OUTPUT_FILE )
print("Bye !")
