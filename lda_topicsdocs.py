# -*- coding: UTF-8 -*-
#!/usr/bin/env python

################################################################################

'''
LDA Score Calculator - Topic Documents
Kayla Jacobs

Assumes a topic model has been trained.

In a "topicDocs" subdirectory, makes a txt file per topic (named for the topic's number)
  which lists all the documents in the model and their proportion for that topic.

Note: Python can't have more than about 500 files opened simultaneously,
so keeps first 500 topics' files open and then does on-demand opening/closing of higher-numbered topics
(Opening/closing files is time-consuming so for smaller numbers of topics,
try to do the keep-everything-open method.)

'''

################################################################################

debugMode = False
testMode = False

################################################################################

print "lda_topicsdocs"
print
print "Initializing..."
print

output_base_dir = r"C:\mallet\dssg\uchaguzi\\"
input_filename = r"C:\mallet\dssg\uchaguzi\td_T50-composition.txt"

numTopicsList = [50]

#-------------------------------------------------------------------------------    

for numTopics in numTopicsList:

    print "numTopics = " + str(numTopics)

    input_file = open(input_filename, "rb")
    output_dir = output_base_dir  + "td" + "_T" + str(numTopics) + "_topicDocs\\"


#    output_file = open(output_filename, "wb")
    
    output_fileDict = {}
    for i in range(0, numTopics):
        if i<=500:    
            output_fileDict[i] = open(output_dir + str(i) + ".txt", "wb")
            print >> output_fileDict[i], "doc" + "\t" + "topic_proportion"
        if i>500:
            output_file = open(output_dir + str(i) + ".txt", "wb")
            print >> output_file, "doc" + "\t" + "topic_proportion"
            output_file.close()
    
    print "Input:"
    print input_filename
    print 
    print "Output:"
#    print output_filename
    print output_dir
    #print output_filenames_filename
    print
    
    #-------------------------------------------------------------------------------    
    
    print "Processing MALLET composition file..."
        
    # Skip first header line
    input_file.readline()
    
    topicDict = {t: [] for t in range(0, numTopics)}
    
    for row in input_file:
        row = row.strip()
        docID, filename, topicProps = row.split("\t", 2)

        if debugMode:
            if int(docID)%10000 == 0:
                print str(docID)
        
        # Modify filename
        #filename = convertMalletFilename(filename)
            
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
    
    input_file.close()
    
    for output_file in output_fileDict.values():
        output_file.close()

#-------------------------------------------------------------------------------    

print "Finished! :)"