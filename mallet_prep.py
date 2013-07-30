# -*- coding: UTF-8 -*-
#!/usr/bin/env python

################################################################################

'''
MALLET prep

Takes a CSV file that includes (among others) the text ID and the text itself,
    and creates a new txt file of the text, with filename equal to the text ID.

Afterwards, this is what you run from the command line (with 5 topics -- edit if desired):
    
bin\mallet import-dir --input INPUTDIRECTORYPATH --output OUTPUTDIRECTORYPATH\mymodel.mallet --keep-sequence --remove-stopwords
bin\mallet train-topics --input OUTPUTDIRECTORYPATH\mymodel.mallet --num-topics 5 --optimize-interval 10 --output-state OUTPUTDIRECTORYPATH\mymodel_T5.gz --output-topic-keys OUTPUTDIRECTORYPATH\mymodel_T5-keys.txt --output-doc-topics OUTPUTDIRECTORYPATH\td_T5-composition.txt

Kayla Jacobs

'''
################################################################################

try:
    import csv
except:
    print "Error in importing for this script"

################################################################################

debugMode = False    # Whether to print extra "debug" messages
testMode = True     # Whether to use full corpus, or just a small subset for testing
testNum = 100        # If in testMode, how large the testing subset is

################################################################################

# Settings:

input_base_dir = r"INPUTDIRECTORY"
#input_base_dir = r"C:\Dropbox\dssg\topics\\"
input_csv_filename = input_base_dir + "FILENAME.csv"
#input_csv_filename = input_base_dir + "uchaguzi_new.csv"
output_base_dir = input_base_dir + "mallet_files\\"
#output_base_dir = input_base_dir + "mallet_files\\"

# Note that script assumes that in the input_base_dir directory,
#    there is a subdirectory called mallet_files. Modify above if desired.

input_csv_delimiter = ','
input_csv_quotechar = '"'

header_col_id = "id"
#header_col_id = "incident_id"
header_col_text = "text"
#header_col_text = "incident_description"

# Note this script assumes that the very first line of the input csv file is
#    a header row, and that the relevant column names in this header row are
#    "id" and "text" respectively. Modify above if desired.

################################################################################

print "MALLET prep script"
print
print "Input filename: " + input_csv_filename
print "Output directory: " + output_base_dir
print

counter = 0

with open(input_csv_filename, "rbU") as input_csv_file:        

    input_reader = csv.reader(input_csv_file, delimiter = input_csv_delimiter, quotechar = input_csv_quotechar)
    
    headerList = input_reader.next()
    print "Input CSV header: " + str(headerList)
    print "ID field called: " + header_col_id
    print "Text field called: " + header_col_text
    print 
    
    for row_entries in input_reader:

        if not testMode or (testMode and counter < testNum):

            counter += 1

            if debugMode:
                print counter
                print str(row_entries)
                print "ID: " + row_entries[headerList.index(header_col_id)]
                print "Text: " + row_entries[headerList.index(header_col_text)]
                print "------"

            # Create text file named after the ID
            output_file = open(output_base_dir + row_entries[headerList.index(header_col_id)] + ".txt", "wb")
            
            # Print the text contents to this file
            print >> output_file, row_entries[headerList.index(header_col_text)]
            
            # Close file
            output_file.close()


# Finish up
print "Number of rows processed: " + str(counter)
print
print "Finished! :)"