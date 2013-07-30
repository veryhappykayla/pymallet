# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import csv
import os
import json
import errno
from pprint import pprint

from collections import *

PRINT_OUTPUT = False

################################################################################

def main():
    infile = 'data/td_T5-composition.txt'
    d = convert_topic_composition_to_dict(infile)
    outfile = 'data/td_T5-topic_document_matrix.csv'
    create_topic_document_matrix(outfile, d)

################################################################################

def convert_topic_composition_to_dict(input_csv_filename=''):
    """Takes a topic composition tab-separted file. Converts it into a dict.
    Each item's key is the file_id (<id>.txt) and value is a dict of mallet_id, file_path, 
    and topic_probabilities [list of length n, ordered by topic id 0-to-n]"""

    output = {}
    with open(input_csv_filename, "rU") as input_csv_file:
        input_reader = csv.reader(
            input_csv_file, delimiter='\t', quotechar='"')

        # Skip the headers
        next(input_reader, None)

        for row in input_reader:

            # convert topic probabilities to a list, ordered by topic id (note:
            # we lose probability ordering)
            probabilities_from_csv = row[2:]
            probabilities_from_csv.remove('')
            topic_count = len(probabilities_from_csv) / 2

            isTopicId = True
            topicId = 0
            topic_probabilities = [0] * topic_count
            for p in probabilities_from_csv:
                if isTopicId:
                    topicId = int(p)
                else:  # topic probability
                    topic_probabilities[topicId] = float(p)

                isTopicId = not isTopicId

            # print topic_probabilities
            # return

            # sort on topic id
            file_name, file_extension = os.path.splitext(row[1])
            file_id = os.path.basename(file_name).strip(file_extension)
            d = {
                'mallet_id': row[0],
                'file_path': row[1],
                # 'file_id' : file_id,
                'topic_probabilities': topic_probabilities
            }
            output[file_id] = d
            # pprint(d)

        if PRINT_OUTPUT:
            print json.dumps(output, indent=4, sort_keys=True)

        return output
        
################################################################################

def create_topic_document_matrix(outfile='', topic_composition_dict={}):
    """Creates a single file which is a topic-document matrix.
    Rows are the documents, columns are the topics, values are the score for the topic in the document."""

    matrix = []

    for k in topic_composition_dict:
        row_values = []
        row_values.append(topic_composition_dict[k]['mallet_id'])
        row_values.extend(topic_composition_dict[k]['topic_probabilities'])

        matrix.append(row_values)

    if outfile:
        with open(outfile, 'wb') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"')
            writer.writerows(matrix)

    if PRINT_OUTPUT:
        pprint(matrix)

    return matrix

################################################################################

def unigram_topics(input_topic_state_filename, output_unigrams_filename, **kwargs):
'''
Assumes a topic model has been trained.
Outputs a file of unigrams with their topics and scores.
'''
    # Set frequency and topic threshold values (optional parameters)
    # Note a threshold of 0 is equivalent to no threshold
    
    # Frequency threshold
    if "freq_threshold" in kwargs:
        freq_threshold = kwargs["freq_threshold"]
    else:
        freq_threshold = 0
    
    # Topic threshold
    if "topic_threshold" in kwargs:
        topic_threshold = kwargs["topic_threshold"]
    else:
        topic_threshold = 0
    
    #-------------------------------------------------------------------------------    
    # Process tokens in topic state
    
    input_topic_state_file = open(input_topic_state_filename, "rb")
    
    # Skip first three lines of MALLET topic state file which has ignorable info
    input_topic_state_file.readline()
    input_topic_state_file.readline()
    input_topic_state_file.readline()
    
    counts = defaultdict(lambda: defaultdict(int))
    
    for line in input_topic_state_file:
        data = line.rstrip().split()
        counts[data[-2]][data[-1]] +=1
    
    input_topic_state_file.close()
    
    #-------------------------------------------------------------------------------    
    # Consolidating topics and printing to output unigrams file
    
    # Open ouput unigrams file
    output_unigrams_file = open(output_unigrams_filename, "wb")
        
    # Print header for output:
    header = "unigram" + "\t" + "count" + "\t" + "topics_list_with_scores"
    print >> output_unigrams_file, header

    for word in counts:
    
        t_total = sum(counts[word].values())
        
        if t_total >= freq_threshold:
        
            w_t = defaultdict(float)
            for t in counts[word]:
                if float(counts[word][t])/t_total >= topic_threshold:
                    w_t[t] = float(counts[word][t])/t_total
                    
            ml = sorted([(value,int(item)) for item,value in w_t.iteritems()], reverse = True)
        
            toPrint =  word + "\t" + str(t_total) + "\t" + str(ml)
        
            if debugMode: print toPrint
            print >> output_unigrams_file, toPrint
    
    # Close output unigrams file
    output_unigrams_file.close()

################################################################################

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

################################################################################

def topic_docs(input_topic_state_filename, output_directory, num_topics):
'''
Assumes a topic model has been trained.

In a "topicDocs" subdirectory, makes a txt file per topic (named for the topic's number)
  which lists all the documents in the model and their proportion for that topic.

Note: Python can't have more than about 500 files opened simultaneously,
so keeps first 500 topics' files open and then does on-demand opening/closing of higher-numbered topics
(Opening/closing files is time-consuming so for smaller numbers of topics,
try to do the keep-everything-open method.)

'''
    # If output_directory doesn't already exist, create it
    # Open files for the topics (or the first 500 thereof, if #topics > 500)
    make_sure_path_exists(output_directory)    
    output_fileDict = {}
    for i in range(0, num_topics):
        if i<=500:    
            output_fileDict[i] = open(output_directory + "topic" + str(i) + ".txt", "wb")
            print >> output_fileDict[i], "doc" + "\t" + "topic_proportion"
        if i>500:
            output_file = open(output_directory + "topic" + str(i) + ".txt", "wb")
            print >> output_file, "doc" + "\t" + "topic_proportion"
            output_file.close()
    
    #-------------------------------------------------------------------------------    
    
    print "Processing MALLET composition file..."
        
    # Open input topic state file
    input_topic_state_file = open(input_topic_state_filename, "rb")
        
    # Skip first header line
    input_topic_state_file.readline()
    
    topicDict = {t: [] for t in range(0, num_topics)}
    
    for row in input_topic_state_file:
        
        row = row.strip()
        docID, filename, topicProps = row.split("\t", 2)

        topicPropsList = topicProps.split("\t")
        for i in range(0, len(topicPropsList)-1, 2):
            topic = topicPropsList[i]
            prop = topicPropsList[i+1]
         
            if int(topic) <= 500: 
                print >> output_fileDict[int(topic)], docID + "\t" + prop
            else:
                output_file = open(output_dir + str(topic) + ".txt", "ab")  # "ab" mode appends rather than rewriting
                print >> output_file, docID + "\t" + prop
                output_file.close()
            
    #-------------------------------------------------------------------------------    
    
    # Close files
    
    input_topic_state_file.close()
    
    for output_file in output_fileDict.values():
        output_file.close()

################################################################################

if __name__ == "__main__":
    main()
