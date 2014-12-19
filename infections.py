"""
Author: Rohan Varma

Contains User class which is the representation of a student/coach
   as a node in a graph.

Two methods:

	 self.total_infection(newVersion) - infects self node and all 
		linked as coach or students

	 User.limited_infection(numToInfect, newVersion, [error = 0]) - finds a subset
		of the graph where the size of the connected components is equal to
		the numToInfect up to a +- of error. Returns True if match was found and
		returns False otherwise
"""

# change this to modify the allowed error for the limited_infection
DEFAULT_ERROR_ALLOWED = 0

class User(object):

	nodes = []
	clusers = dict()

	def __init__(self, initVersion, stuid):
		self.version = initVersion
		self.id = stuid
		self.students = set()
		self.coaches = set()
		User.nodes.append(self)

	def __str__(self):
		return "(%d, %d)" % (self.id, self.version)

	def __repr__(self):
		return str(self)

	def getVersion(self):
		return self.version

	def updateVersion(self, newVersion):
		self.version = newVersion

	def getStudents(self):
		return self.students

	def addStudent(self, newStudent):
		self.students.add(newStudent)
		if self not in newStudent.getCoaches():
			newStudent.addCoach(self)

	def getCoaches(self):
		return self.coaches

	def addCoach(self, newCoach):
		self.coaches.add(newCoach)
		if self not in newCoach.getStudents():
			newCoach.addStudent(self)

	def total_infection(self, newVersion):
		self.updateVersion(newVersion)
		for coach in self.coaches:
			if coach.getVersion() != newVersion:
				coach.total_infection(newVersion)
		for student in self.students:
			if student.getVersion() != newVersion:
				student.total_infection(newVersion)

	def isCoach(self):
		return len(self.students) > 0

	@staticmethod
	def getClusters():
		visited = set()
		clusters = dict()
		for mainNode in User.nodes:
			if mainNode in visited:
				continue
			visitQ = [mainNode]
			clusters[mainNode] = 0
			while len(visitQ) > 0:
				node = visitQ.pop(0)
				if node in visited:
					continue
				else:
					clusters[mainNode] += 1
					visitQ.extend(list(node.getStudents()))
					visitQ.extend(list(node.getCoaches()))
					visited.add(node)
		User.clusters = clusters

	@staticmethod
	def getListFromMapping():
		numbers = []
		for node in User.clusters:
			numbers.append((node, User.clusters[node]))
		return numbers

	@staticmethod
	def sumSubset(subset):
		total = 0
		for (node, value) in subset:
			total += value
		return total

	@staticmethod
	def subsetSum(nums, goal, error = 0):
		answer = []
		upperBound, lowerBound = goal + error, goal - error
		def solve(nums, goal, i):
			if lowerBound <= User.sumSubset(answer) <= upperBound:
				return True
			elif i >= len(nums):
				return False
			elif not nums:
				return False
			else:
				answer.append(nums.pop(i))
				if solve(nums, goal, 0):
					return True
				nums.insert(i, answer.pop())
				if solve(nums, goal, i + 1):
					return True
				return False
		solve(nums, goal, 0)
		return answer

	@staticmethod
	def limitedInfection(goal, newVersion, error = DEFAULT_ERROR_ALLOWED):
		# exponential algorithm for subset sum
		# runtime gets pretty terrible pretty quickly without decent error allowance
		User.getClusters()
		numbers = User.getListFromMapping()
		answer = User.subsetSum(numbers, goal, error)
		for (node, value) in answer:
			node.total_infection(newVersion)
		return answer != []

	@staticmethod
	def clearGraph():
		User.nodes = []
		User.clusters = dict()

User(1, 0)

User.limitedInfection(1, 3, 1)