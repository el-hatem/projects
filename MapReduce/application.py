def run():
	try:
		mapreducer = MapReducer('./input-sm.txt', batches=500, operation='count')
		print(mapreducer)
	except Exception as e:
		print(e) 


# main script
if __name__ == '__main__':
	from mapreduce import MapReducer
	# run applicaton
	run()

	