"""
Author: Rohan Varma

Unit Tests for the graph backend
"""

from infections import User

def graphSetup1():
	return [User(1, 0)]

def graphSetup2():
	users = [User(1, i) for i in xrange(10)]
	for i in xrange(6,10):
		users[0].addStudent(users[i])
	for i in xrange(3,6):
		users[2].addStudent(users[i])
	return users

def graphSetup3():
	users = [User(1, i) for i in xrange(10)]
	return users


def cleanup():
	User.clearGraph()

def testTotalInfectionOnOne():
	users = graphSetup1()
	print "Testing total_infection on single node...",
	assert(users[0].getVersion() == 1)
	users[0].total_infection(2)
	assert(users[0].getVersion() == 2)
	users[0].total_infection(4)
	assert(users[0].getVersion() == 4)
	print ".. passed!"
	cleanup()

def testTotalInfectionOnAll():
	users = graphSetup3()
	print "Testing total_infection on all nodes...",
	for user in users:
		user.total_infection(2)
	for user in users:
		assert(user.getVersion() == 2)
	print ".. passed!"
	cleanup()

def testTotalInfectionOnSubset():
	users = graphSetup2()
	print "Testing total_infection on subset of nodes...",
	users[0].total_infection(2)
	# check all nodes in component increased to version 2 if coach infected
	assert(users[0].getVersion() == 2)
	for i in xrange(6,10):
		assert(users[i].getVersion() == 2)
	# ensure no other notes were modified
	for i in xrange(1, 6):
		assert(users[i].getVersion() == 1)
	users[4].total_infection(2)
	# ensure all nodes in component increased to version 2 if student infected
	assert(users[2].getVersion() == 2)
	for i in xrange(3,6):
		assert(users[i].getVersion() == 2)

	print ".. passed!"
	cleanup()

def testTotalInfection():
	testTotalInfectionOnOne()
	testTotalInfectionOnAll()
	testTotalInfectionOnSubset()

def numberOfNodesAtVersion(version):
	total = 0
	for representative in User.clusters:
		if representative.getVersion() == version:
			total += User.clusters[representative]
	return total


def testLimitedInfectionOnOne():
	users = graphSetup1()
	print "Testing limited_infection on single node...",
	# infect to next version
	assert(User.limitedInfection(1, 2, 0))
	assert(numberOfNodesAtVersion(2) == 1)
	# attempt to infect 2 with no error, shouldnt work
	assert(User.limitedInfection(2, 3, 0) == False)
	assert(numberOfNodesAtVersion(2) == 1)
	# attempt to infect 2 with error of 1, should work
	assert(User.limitedInfection(2, 3, 1))
	assert(numberOfNodesAtVersion(3) == 1)
	print ".. passed!"
	cleanup()

def testLimitedInfectionOnAll():
	users = graphSetup3()
	print "Testing limited_infection on lots of single node...",
	assert(User.limitedInfection(4, 2, 0))
	assert(numberOfNodesAtVersion(2) == 4)
	assert(User.limitedInfection(12, 3, 2))
	assert(User.limitedInfection(6, 4, 0) == True)
	assert(numberOfNodesAtVersion(4) == 6)
	assert(User.limitedInfection(12, 4, 4))
	print "..passed!"
	cleanup()

def testLimitedInfection():
	testLimitedInfectionOnOne()
	testLimitedInfectionOnAll()

def runTests():
	testTotalInfection()
	testLimitedInfection()
