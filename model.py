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
	
	def add_question(self, question):
		self._questions.append(question)
		
	def add_sub_topic(self, child):
		self._sub_topics.append(child)
	
	def sub_topics(self):
		return self._sub_topics

