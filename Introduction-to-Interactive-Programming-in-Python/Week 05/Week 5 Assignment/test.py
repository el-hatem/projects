from simpletest import *

from module import function



def test_function(testting_function):
	tester = TestSuite('timeformat')

	tester.run_test(testting_function('input'), 'output', 'test_case_#1')

	tester.report_results()




def test():
	test_function('testting_function')

if __name__ == '__main__':
	test()