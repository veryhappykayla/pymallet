#!/usr/bin/python
import csv
import os
import json
import tempfile
import subprocess
import os

"""
TODOS: 

- not hardcode mallet path
- upload it to PIP
- clean up folder paths to work on windows
- import it in another application and get the returned values
- update the readme (with a mini-tutorial)
- world peace.
- achieve fame and riches. (through world peace)


"""

# import ipdb

from pprint import pprint

PRINT_OUTPUT = False

### PYMALLET

class pymallet(object):
    """class documentation string"""
    
    _id_file_map = {}
    # matrix = None

    def __init__(self):
        print "Welcome to pymallet"
        pass

    ### POSSIBLY INCLUDE A FUNCTION TO DO BASIC PRE-PROCESSING LIKE REMOVING 
    ### STOPWORDS AND STEMMING

    ### INPUT A CSV FILE AND RETURN A TEMPORARY DIRECTORY OF 
    ### OF INDIVIDUAL DOCUMENTS

    def import_documents(self, input_csv_filename="data/test.csv"):
        """Headers is a 2-element list, text, where the first element is the column name
        for the document id, and the 2nd element is the column name for the document text"""

        _matrix = None

        id_idx = 0
        document_idx = 1

        temp_directory = tempfile.mkdtemp()
        out_directory = tempfile.mkdtemp()
        with open(input_csv_filename, "rU") as input_csv_file:
            input_reader = csv.reader(
                input_csv_file, delimiter=',', quotechar='"', escapechar='\\')

            for row in input_reader:
                item_id, text = row[id_idx], row[document_idx]
                print 'id: %s, text: %s' % (row[id_idx], row[document_idx])
                f = tempfile.NamedTemporaryFile(
                    delete=False, dir=temp_directory, suffix='.txt')
                self._id_file_map[f.name] = item_id
                f.write(text)
                f.close()

        pprint(self._id_file_map)

        print temp_directory

        my_env = os.environ.copy()
        # subprocess.call("mallet", env=my_env)
        # return

        MALLET_PATH = "mallet"
        NUM_TOPICS = 5
        OPT_INTERVAL = 10

        # run mallet on this directory
        # TODO: consider renaming mymodel for clarity?
        subprocess.call(
            [MALLET_PATH, "import-dir", "--input", temp_directory, "--output",
             out_directory + "/mymodel.mallet", "--keep-sequence", "--remove-stopwords"], env=my_env)
        subprocess.call(
            [MALLET_PATH, "train-topics", "--input", out_directory + "/mymodel.mallet", "--num-topics", str(NUM_TOPICS), "--optimize-interval", str(OPT_INTERVAL), "--output-state",
             out_directory + '/mymodel_T5.gz', "--output-topic-keys", out_directory + "/mymodel_T5-ke ys.txt", "--output-doc-topics", out_directory + "/td_T5-composition.txt"], env=my_env)
        subprocess.call(["ls", temp_directory])
        subprocess.call(["ls", out_directory])

        tc_dict = self.convert_topic_composition_to_dict(out_directory + "/td_T5-composition.txt", NUM_TOPICS)
        matrix = self.create_topic_document_matrix(topic_composition_dict=tc_dict)

        # pprint(matrix)

        #...
        # data = my_topic_model
        # id,t1,t2,t3
        # 1,0.1,.5,.4 -> [[1,.1,.5,.4],[2,.1.]

        # id, t0 (or the topic definition), t1, ...
        # [6 : [.1,.5,.4]), 4 : ,[.1.])]

        # TODO: un-gzip super file and allow user to view it? useful at all or no?

        # after creating output files, create what user interacts with
        #   - document_id / topics matrix
        #   - topic / ordered-list of documents (by proportion)
        #   - topic definitions

        # cleanup
        for f in self._id_file_map:
            print f
            os.unlink(f)
            print os.path.exists(f)
            
        self.matrix = matrix

        return {
            "matrix": matrix,
            "topic_lists": None,
            "topic_definitions": None,
        }

    def convert_topic_composition_to_dict(self, input_csv_filename='', topic_count=0):
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
                print row
                row.remove('')
                print row

                probabilities_from_csv = row[2:]

                # topic_count = len(probabilities_from_csv) / 2

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
                    'file_path': row[1].strip('file:'),
                    # 'file_id' : file_id,
                    'topic_probabilities': topic_probabilities
                }
                output[file_id] = d
                # pprint(d)

            if PRINT_OUTPUT:
                print json.dumps(output, indent=4, sort_keys=True)

            return output


    def create_topic_document_matrix(self, outfile='', topic_composition_dict={}):
        """Creates a single file which is a topic-document matrix.
        Rows are the documents, columns are the topics, values are the score for the topic in the document."""

        # global self._id_file_map

        matrix = []

        for k in topic_composition_dict:
            row_values = []
            row_values.append(self._id_file_map[ topic_composition_dict[k]['file_path'] ])
            row_values.extend(topic_composition_dict[k]['topic_probabilities'])

            matrix.append(row_values)

        if outfile:
            with open(outfile, 'wb') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"')
                writer.writerows(matrix)

        if PRINT_OUTPUT:
            pprint(matrix)

        return matrix

    ### PASS DIRECTORY OF DOCUMENTS TO MALLET/TERMINAL 

    def train_topics(topicnumber, optimize_interval, output_state):
        pass


if __name__ == "__main__":
    p = pymallet()
    p.import_documents()