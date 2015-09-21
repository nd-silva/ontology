import unittest
from model import Topic, Question
from main import OntologyMain


class TestParser(unittest.TestCase):
	
	def parse_and_test(self, tree):
		root = OntologyMain().build_ontology_from_string(tree)	
		output = str(root)
		errormessage="Model built from input should have the same string representation as input. Input: " + tree + ", output: " + output  
		self.assertTrue(str(root) == tree, errormessage)

	
	"""Tests for a simple ontology with only one level of sub topics"""
	def test_one_level_deep (self):
		self.parse_and_test("animal ( dog fish )")
	
	def test_full_tree (self) :
		tree = "Animals ( Sheep Reptiles ( Alligators Snakes ( Cobras Asps Rattlesnakes Vipers ) ) Birds ( Eagles Pigeons Crows ) Fish )"
		self.parse_and_test(tree)

	
		
class TestQueries(unittest.TestCase):
	
	def setUp(self):
		self.controller = OntologyMain()
		self.root = self.controller.build_ontology_from_string("Animals ( Dogs Cats )")
		self.questions = ["Animals: How many animals are in the world?", "Dogs: How do dogs seet?", "Cats: Are cats safe to pet?"]
		for q in self.questions:
			self.controller.add_question(q);
	
	def test_failed_query (self):
		result = self.controller.answer_query("Dogs: Are ") 
		self.assertTrue(result == 0, "There should be no match")
	
	def test_topic_specific_query (self):
		#even though there;s a potential match for animals the target topic is dogs
		result = self.controller.answer_query("Dogs: How ") 
		self.assertTrue(result == 1, "There should be 1 match")
	
	
	def test_query_over_entire_tree (self):
		result = self.controller.answer_query("Animals: Are ") 
		self.assertTrue(result == 1, "There should be 1 match")
	
	def test_adding_one_question(self):
		for topic in self.root.sub_topics():
			self.assertTrue(len(topic.questions()) == 1, "Each topic should only have one question")
		self.assertTrue(len(self.root.questions()) == 1)

if __name__ == '__main__':
	unittest.main()


