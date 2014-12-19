import sys
from visualization import GraphVisualization
from tests import runTests


def main(argv):
	if len(argv) < 1:
		print "options:\n	python main.py test			# will run tests\n	python main.py visualize 	# will run visualizer"
	elif argv[0] == "visualize":
		graph = GraphVisualization()
		graph.run()
	elif argv[0] == "test":
		runTests()
	else:
		print "options:\n	python main.py test 		# will run tests\n	python main.py visualize 	# will run visualizer"

main(sys.argv[1:])