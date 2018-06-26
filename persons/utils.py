class BlankDict(dict):
	def __missing__(self, key):
		return ''