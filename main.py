import sys, fileinput
from model import Topic, Question

"""Main entry point for the Ontology challenge from Quora challenges
	This class is responsible for parsing the sample file and producing the desired output"""
class OntologyMain:
	"""Parses the flattened topic tree to build the ontology, and returns the root topic """
	def __init__(self):
		self._index = {}
		self._root = None
	
	"""Checks the ontology for topics that match the
	query text and returns a QueryResult describing the number of matched questions"""
	def answer_query(self, query):
		return QueryResult(query)
 
	"""Continues building the ontology using the given string, starting at the topic named root.
	 	Returns the remainder of the tree_str that has not been parsed once the entire sub tree rooted at root has been created.
	"""
	def create_recursive(self, tree_str, root):
		#this part uses the partition function to scan the string from left to right.
		#basic algortihim:
		#divide the flattened tree into 2 - the left being the first word before a space, and the rest what we call the "remainder"
		#the first word before a space is always a topic name,  thus this is a subtopic of root, since this method is only called when an opening bracket is encountered
		#after creating a topic, check the remainder. one of 3 things is possible:
		#1) remainder starts with another word, (meaning another child of root)
		#2) remainder starts with an opening bracket (meaning the child we just created also has children)
		#3) remainder starts with a closing bracket meaning there are no more children of root
		
		partitions = tree_str.lstrip().partition(" ")

		while True: 
			left = partitions[0]
			remainder = partitions[2]
			#in the case of multiple closing brackets in a sequence, e.g. " ) ) )", the left side of the partition is also a bracket
			if not left or left.lstrip().startswith(")"): 
				print("current node " + root._name + " " + str(partitions) )
				#there are no more spaces, meaning there is no more data for this topic
				return remainder #let the parent continue processing the rest of the tree
			else:
				child = Topic(name=left, parent=root) 
			self._index[child_topic_name] = child #add to index
			if remainder.startswith(")"): 
				return remainder[1:]
			elif remainder.startswith("("):
				#the newly created child topic also has sub topics
				remainder = remainder[2:] #remove the opening bracket and the space
				remainder = self.create_recursive(remainder, child).lstrip()
			partitions = remainder.lstrip().partition(" ")
			
			

	def build_ontology_from_string(self, topic_tree):
		partition = topic_tree.partition(" ")
		root_topic_name = partition[0]
		self._root = Topic(root_topic_name, None)
		self._index[root_topic_name] = self._root
		remainder = partition[2]
		self.create_recursive(remainder[2:], self._root) #remove the bracket and the first space
		return self._root
		
	def process_input_file(self, file):
		print("processing file " + file)


if __name__ == "__main__":
	file = sys.argv[1]
	controller = OntologyMain()
	controller.process_input_file(file)
