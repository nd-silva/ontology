import sys, fileinput, re
import pyparsing as pp
from model import Topic, Question

class OntologyMain:
	"""Main entry point for the Ontology challenge from Quora challenges
	This class is responsible for parsing the sample file and producing the desired output
	"""
	def __init__(self):
		 
		#the index is a convenience to quickly look up sub topics
		#can be optional and require tree traversal
		self._index = {} 
		self._root = None

	def add_question(self, line):
		""""add the question of the format <topic>: question text to the ontology
		"""
		parse_result = parse_question(line)
		if parse_result is not None:
			question = Question(parse_result[1])
			topic = parse_result[0]
			self._index[topic].add_question(question)
			
	def add_to_index(self, topic, topic_name):
		self._index[topic_name] = topic
	
	def check_sub_topics(self,query, topic):
		"""helper method to recursively check the Topic rooted at topic to see if any of them also match the query
		"""
		matching_questions = [q for q in topic.questions() if q.matches(query)]
		count = len(matching_questions)
		
		for sub_topic in topic.sub_topics():
			count += self.check_sub_topics(query, sub_topic)
		return count
		
	
	def answer_query(self, query):
		"""return the number of topics in the ontology that answer the given query of the form 'topic question'
		"""
		parse_result = parse_question(query)
		if parse_result is not None:
			question = parse_result[1]
			topic_name = parse_result[0]
			topic = self._index[topic_name]
			count = self.check_sub_topics(question, topic)
			return count

	def create_sub_tree(self, root, children):
		"""Add the list of child topics to root
		"""
		for next in children:		
			if not islist(next):
				child_topic = Topic(next, root)
				self.add_to_index(child_topic, next)
			else:
				self.create_sub_tree(child_topic, next)
	
	def build_ontology_from_string(self, topic_tree):
		#use partition to separate the root topic name from the rest of the tree
		partition = topic_tree.partition(" ")
		root_topic_name = partition[0]
		sub_tree_str = partition[2]
		self._root = Topic(root_topic_name, None)
		
		self.add_to_index(self._root, root_topic_name)
		##pyparsing does the parsing for us - returns a nested list of strings
		##if a topic in the list is immediately followed by a list,
		#then the list represents the subtree rooted at topic
		sub_list = pp.nestedExpr().parseString(sub_tree_str).asList()[0]
	
		for next_elem in sub_list:		
			if not islist(next_elem):
				child_topic = Topic(next_elem, self._root)
				self.add_to_index(child_topic, next_elem)
			else:
				self.create_sub_tree(child_topic, next_elem)
		return self._root
		
	def process_queries(self):
		"""main entry point - read the files from commandline/stdin and answer queries
		"""
		input = fileinput.FileInput()
		
		for line in input:
			line= line.strip()
			if input.isfirstline():
				topic_count = int(line)
				self._index.clear()
			else:
				currentline = input.filelineno()
				if currentline == 2:
					topic_tree = line
					root = self.build_ontology_from_string(topic_tree)
					if len(self._index) != topic_count:
						print("Error, for file %s, %d we should have created the same amount of topics %d " % (input.filename(),  topic_count))
						print("Input tree: ", topic_tree)
						print("generated tree: ", str(root))
						sys.exit(1)
				elif currentline == 3:
					question_count = int(line)
				
				elif currentline >= 4 and currentline < (question_count+4):
					self.add_question(line)
				elif currentline >= question_count+5: #queries start after all the questions
					query = line
					result = self.answer_query(query)
					print(result)
		
				



#precompiled regular expression used to parse questions and queries
QUESTION_REGEX = re.compile("(?P<topic>[A-Za-z]+)\:? (?P<question>.*)")

def parse_question(line):
	
	match = QUESTION_REGEX.match(line)
	if match is not None:
		groups = match.groupdict()
		question = groups["question"]
		topic = groups["topic"]
		return (topic, question)			
	return None


def islist(obj):
	return type(obj) == list
	
if __name__ == "__main__":
	controller = OntologyMain()
	controller.process_queries()
