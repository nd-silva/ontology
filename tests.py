import unittest
from model import Topic, Question
from main import OntologyMain


class TestParser(unittest.TestCase):
	
	def parse_and_test(self, tree):
		root = OntologyMain().build_ontology_from_string(tree)	
		output = str(root)
		errormessage="Model built from input should have the same string representation as input. Input: " + tree + ", output: " + output  
		self.assertTrue(str(root) == tree, errormessage)

	def test_childless(self):
		self.parse_and_test("animal")
	
	"""Tests for a simple ontology with only one level of sub topics"""
	def test_one_level_deep (self):
		self.parse_and_test("animal ( dog fish )")
	
	def test_full_tree (self) :
		tree = "Animals ( Sheep Reptiles ( Alligators Snakes ( Cobras Asps Rattlesnakes Vipers ) ) Birds ( Eagles Pigeons Crows ) Fish )"
		self.parse_and_test(tree)
	
	
if __name__ == '__main__':
    unittest.main()


