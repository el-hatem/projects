# classes
class MapReducer:
	def __init__(self, filepath, *args, **kwargs):
		# initial arguments
		self.batches = kwargs.get('batches', 1)
		self.operation = kwargs.get('operation', 'count')
		# initial data
		self.input = self.readfile(filepath)
		self.length = len(self.input)
		self.max_word = max([len(word) for word in self.input])
		# start functions
		self.groups = self.grouper()
		self.result = self.reducer(self.operation)

	# main function
	def mapper(self, batches=1):
		# helper function
		def batching():
			for i in range(0, self.length, self.length//batches):
				yield self.input[i:i+self.length//batches]

		mappings = []
		# make mapper file
		for batch in batching():
			for word in batch:
				mappings.append(f'{len(word)}:{word}')
		yield mappings


	
	def grouper(self):
		groupers = dict()
		# add each word to its group
		for mapper in self.mapper(self.batches):
			for word in mapper:
				splitter = word.split(':')
				if groupers.get(splitter[0], None):
					groupers[splitter[0]].append(splitter[1])
				else :
					groupers[splitter[0]] = [splitter[1]]
		return groupers


	def reducer(self, operation='count'):
		if operation == 'count':
			return {k: len(v) for k, v in self.groups.items()}
		elif operation == 'max':
			max_ = max([len(v) for v in self.groups.values()])
			return {k: len(v) for k, v in self.groups.items() if len(v) == max_}
		elif operation == 'min':
			min_ = min([len(v) for v in self.groups.values()])
			return {k: len(v) for k, v in self.groups.items() if len(v) == min_}

		return None


	# helper functions
	def readfile(self, filepath):
		with open(filepath, encoding="utf8") as file:
			lines =  "".join(file.read().splitlines())
		return lines.split(' ')


	# Getters & setters
	def get(self, arg='all'):
		if arg == 'all':
			return self.input
		elif arg == 'result':
			return self.result
		elif arg == 'groups':
			return self.groups

	def get_result(self):
		return self.result
	def get_groups(self):
		return self.groups

	def set(self, lines):
		self.input = lines


	def __str__(self):
		return f"result: {self.result}"
