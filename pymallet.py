#!/usr/bin/python
import subprocess

### PYMALLET

class pymallet(object):
	"""class documentation string"""


	def __init__(self):
		print "Welcome to pymallet"
		pass


	### POSSIBLY INCLUDE A FUNCTION TO DO BASIC PRE-PROCESSING LIKE REMOVING 
	### STOPWORDS AND STEMMING

	### INPUT A CSV FILE AND RETURN A TEMPORARY DIRECTORY OF 
	### OF INDIVIDUAL DOCUMENTS
	
	def import_documents(self, input_csv_filename):

		id_file_map = {}

		temp_directory = tempfile.mkdtemp()
		out_directory = tempfile.mkdtemp()
		with open(input_csv_filename, "rU") as input_csv_file:
			input_reader = csv.reader(
				input_csv_file, delimiter=',', quotechar='"', escapechar='\\')

			for row in input_reader:
				item_id, text = row[0], row[1]
				print 'id: %s, text: %s' % (row[0], row[1])
				f = tempfile.NamedTemporaryFile(
                	delete=False, dir=temp_directory, suffix='.txt')
            	id_file_map[item_id] = f
            	f.write(text)
            	f.close()

    	pprint(id_file_map)
		print temp_directory

		# my_env = os.environ.copy()
		# subprocess.call("mallet", env=my_env)
		MALLET_PATH = "/Users/paulmeinshausen/mallet-2.0.7/bin/mallet"
		NUM_TOPICS = 5
		OPT_INTERVAL = 10

		# run mallet on this directory
		# TODO: consider renaming mymodel for clarity?

		subprocess.call(
			[MALLET_PATH, "import-dir", "--input", temp_directory, "--output", \
			out_directory + "/mymodel.mallet", "--keep-sequence", "--remove-stopwords"])
		subprocess.call(
			[MALLET_PATH, "train-topics", "--input", out_directory + "/mymodel.mallet", \
			 "--num-topics", str(NUM_TOPICS), "--optimize-interval", str(OPT_INTERVAL), \
			 "--output-state", \
			 	 out_directory + '/mymodel_T5.gz', "--output-topic-keys", \
			 	 out_directory + "/mymodel_T5-keys.txt", "--output-doc-topics", \
			 	 out_directory + "/td_T5-composition.txt"])
		subprocess.call(["ls", temp_directory])
		subprocess.call(["ls", out_directory])

        #...
    # data = my_topic_model
    # id,t1,t2,t3
    # 1,0.1,.5,.4 -> [[1,.1,.5,.4],[2,.1.]

    # id, t0 (or the topic definition), t1, ...
    # [6 : [.1,.5,.4]), 4 : ,[.1.])]

    # ungzip and turn it into python stuff
    # bin\mallet import-dir --input INPUTDIRECTORYPATH --output OUTPUTDIRECTORYPATH\mymodel.mallet --keep-sequence --remove-stopwords
    # bin\mallet train-topics --input OUTPUTDIRECTORYPATH\mymodel.mallet
    # --num-topics 5 --optimize-interval 10 --output-state
    # OUTPUTDIRECTORYPATH\mymodel_T5.gz --output-topic-keys
    # OUTPUTDIRECTORYPATH\mymodel_T5-keys.txt --output-doc-topics
    # OUTPUTDIRECTORYPATH\td_T5-composition.txt

    # after creating output files, create what user interacts with
    #  - document_id / topics matrix
    #  - topic / ordered-list of documents (by proportion)
    #  - topic definitions

    return {
        "matrix": None,
        "topic_lists": None,
        "topic_definitions": None,
    }

    # cleanup
    for f in id_file_map.values():
        print f
        os.unlink(f.name)
        print os.path.exists(f.name)

    pass


		#subprocess.call(["/Users/paulmeinshausen/mallet-2.0.7/bin/mallet"])
		# def import_documents(inputdirectorypath,outputdirectorypath):
		# 	subprocess.call(["/Users/paulmeinshausen/mallet-2.0.7", "import-dir", "--input", "inputdirectorypath", \
		# 		"--output", "outputdirectorypath" + "/mymodel.mallet", "--keep-sequence", \
		# 		"--remove-stopwords"])
		# 	pass



		### PASS DIRECTORY OF DOCUMENTS TO MALLET/TERMINAL 

	def train_topics(topicnumber, optimize_interval, output_state):
		pass