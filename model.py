class QueryResult:
	def __init__(self, query):
		self._query = query
		self._matches = 0
	def increment_matches(self, count):
		self._matches = self._matches + count
	def matches(self):
		return self._matches

class Question:
	def __init__(self, question):
		self._question_text = question
	def matches(self, query):
		return self._question_text.startswith(query)
	def __str__(self):
		return self._question_text

class Topic:
	def __init__(self, name, parent):
		self._parent = parent
		self._name = name
		self._sub_topics = []
		self._questions = []
		print("mi nombre es " + name)
		if (self._parent is not None):
			self._parent.add_sub_topic(self)
	def __str__(self):
		if self._sub_topics:
			children = " ".join(str(topic) for topic in self._sub_topics)
			return self._name + " ( " + children + " )"
		else:
			return self._name
			
	def questions(self):
		return self._questions
	
	def add_sub_topic(self, child):
		self._sub_topics.append(child)

