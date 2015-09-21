import sys, fileinput
from utils import *
from model import Topic, Question




"""Main entry point for the Ontology challenge from Quora challenges
	This class is responsible for parsing the sample file and producing the desired output
	"""
class OntologyMain:
	
	"""Parses the flattened topic tree to build the ontology, and returns the root topic """
	def __init__(self):
		self._index = {}
		self._root = None


	"""Continues building the ontology using the given string, starting at the topic named root.
	 	Returns the remainder of the tree_str that has not been parsed once the entire sub tree rooted at root has been created.
	"""
	def create_recursive(self, tree_str, root):
		"""this part uses the partition function to scan the string from left to right.
		basic algortihim:
		divide the flattened tree into 2 - the left being the first word before a space, and the rest what we call the "remainder"
		the first word before a space is always a topic name,  thus this is a subtopic of root, since this method is only called when an opening bracket is encountered
		after creating a topic, check the remainder. one of 3 things is possible:
		1) remainder starts with another word, (meaning another child of root)
		2) remainder starts with an opening bracket (meaning the child we just created also has children)
		3) remainder starts with a closing bracket meaning there are no more children of root"""
		
		partitions = tree_str.lstrip().partition(" ")
		while True: 
			left_portion = partitions[0]
			remainder = partitions[2]
			#in the case of multiple closing brackets in a sequence, e.g. " ) ) )", the left side of the partition is also a bracket
			if not left_portion or re.match("^\s*\)",left_portion): 
				#there are no more spaces, meaning there is no more data for this topic
				#return remainder #let the parent continue processing the rest of the tree
				if root is None:
					break
				else:
					root = root._parent
					#need to split again
			else:
				topic_name=left_portion
				child = Topic(topic_name, root) 
				self.add_to_index(child, topic_name) #add to index
				if re.match("^\s*\)", remainder): 
					root = root._parent 
					remainder = remainder[1:]
				elif re.match("^\s*\(",remainder): #startswith("("):
					root = child
					#the newly created child topic also has sub topics
					remainder = remainder[2:] #remove the opening bracket and the space
					#remainder = self.create_recursive(remainder, child).lstrip()
			partitions = remainder.lstrip().partition(" ")
	

		
		
	def add_question(self, line):
		parse_result = parse_question(line)
		if parse_result is not None:
			question = Question(parse_result[1])
			topic = parse_result[0]
			self._index[topic].add_question(question)
			
	def add_to_index(self, topic, topic_name):
		self._index[topic_name] = topic
	
	def check_sub_topics(self,query, topic):
		#check each question to see if it matches the query
		matching_questions = [q for q in topic.questions() if q.matches(query)]
		count = len(matching_questions)
		
		for sub_topic in topic.sub_topics():
			count += self.check_sub_topics(query, sub_topic)
		return count
		
		
	def answer_query(self, query):
		parse_result = parse_question(query)
		if parse_result is not None:
			question = parse_result[1]
			topic_name = parse_result[0]
			topic = self._index[topic_name]
			count = self.check_sub_topics(question, topic)
		return count

	def build_ontology_from_string(self, topic_tree):
		#manually parsing the text is one option, another was to use pyparsing, 
		#but the dev env on hackerrank don't include it so I wanted to stick to the restrictions
		partition = topic_tree.partition(" ")
		root_topic_name = partition[0]
		self._root = Topic(root_topic_name, None)
		self.add_to_index(self._root, root_topic_name)
		remainder = partition[2]
		self.create_recursive(remainder[2:], self._root) #remove the bracket and the first space
		return self._root
		
	def process_queries(self):
		with fileinput.input() as input:
			topic_count = int(readline_strip(input))
			topic_tree = readline_strip(input)
			question_count = int(readline_strip(input))
			root = self.build_ontology_from_string(topic_tree.strip())
			if len(self._index) != topic_count:
				print("Error...we should have created the same amount of topics")
				print("Input tree: ", topic_tree)
				print("generated tree: ", str(root))
				sys.exit(1)

			#now read questions
			for count in range (0, question_count):
				line = readline_strip(input)
				self.add_question(line)
			query_count =int(readline_strip(input))
			for count in range(0, query_count):
				query = readline_strip(input)
				result = self.answer_query(query)
				print(result)


if __name__ == "__main__":
	controller = OntologyMain()
	controller.process_queries()
