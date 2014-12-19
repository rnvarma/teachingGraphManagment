"""
Author: Rohan Varma

Contains DrawableUser and GraphVisualization classes.

DrawableUser - extends User from infections.py and adds functionality
	to maintain data and draw self as a node on a graph

GraphVisualization - extends eventBasedAnimationClass and visualizes
	the graph manintained by User class
"""
from Tkinter import *
import random
from infections import User
from eventBasedAnimationClass import EventBasedAnimationClass

class DrawableUser(User):

	def __init__(self, initVersion, stuid, x, y):
		super(DrawableUser, self).__init__(initVersion, stuid)
		self.x = x
		self.y = y
		self.baseRadius = 15
		self.radius = self.baseRadius
		self.color = "red"
		self.selected = False
		self.getNewWiggleDiffs()

	def rgbString(self, red, green, blue):
		return "#%02x%02x%02x" % (red, green, blue)

	def getNodeColor(self):
		red = 255 - 20 * self.version if 255 - 20 * self.version>0 else 0
		blue = 20 * self.version if 20 * self.version < 255 else 255
		return self.rgbString(255 - 20 * self.version, 20 * self.version, 0)

	def getTextColor(self):
		# return self.rgbString(128 + 5 * self.version, 255, 255)
		return "white"

	def addStudent(self, node):
		if (node != self):
			super(DrawableUser, self).addStudent(node)
			self.radius = self.baseRadius + (2 * len(self.getStudents()))

	def updateXY(self, newX, newY):
		self.x = newX
		self.y = newY

	def updateRadius(self, newR):
		self.radius = newR

	def drawCircle(self, canvas):
		(cx, cy, r) = (self.x, self.y, self.radius)
		color = "blue" if self.selected else self.getNodeColor()
		canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = color, width = 0)
		canvas.create_text(cx, cy, text = str(self.version), font = "Courier 20 bold",
			fill = self.getTextColor())
	
	def drawConnections(self, canvas):
		(cx, cy, r) = (self.x, self.y, self.radius)
		for student in self.getStudents():
			(sx, sy, sr) = student.x, student.y, student.radius
			canvas.create_line(sx, sy, cx, cy, width = 5)

	def wasClicked(self, x, y):
		(cx, cy) = (self.x, self.y)
		distance = ((cx - x)**2 + (cy - y)**2)**0.5
		return distance <= self.radius

	def select(self):
		self.selected = True

	def unselect(self):
		self.selected = False

	def wiggle(self):
		if random.random() < 0.10:
			self.getNewWiggleDiffs()
		self.x += self.wiggleX
		self.y += self.wiggleY

	def getNewWiggleDiffs(self):
		self.wiggleX = random.random() * random.choice([1,-1])
		self.wiggleY = random.random() * random.choice([1,-1])


class GraphVisualization(EventBasedAnimationClass):
	
	def __init__(self):
		self.width = 800
		self.height = 600
		self.graphW = 600
		self.graphH = self.height
		self.timerDelay = 250
		self.nodes = []
		self.nodeCount = 0
		self.initVersion = 1
		self.coachSelection = None
		self.mouseDown = False
		self.font = "Courier 15 bold"
		self.limitedFocus = False
		self.limitedText = ""
		self.limitedVersionFocus = False
		self.limitedVersionText = ""
		self.textTickerDisplayCounter = 0
		self.doWiggle = False

	def onKeyPressed(self, event):
		if event.keysym == "w":
			self.doWiggle = not self.doWiggle
		elif self.limitedFocus:
			if event.keysym == "BackSpace":
				self.limitedText = self.limitedText[:-1]
			elif event.keysym in "0123456789":
				self.limitedText += event.keysym
		elif self.limitedVersionFocus:
			if event.keysym == "BackSpace":
				self.limitedVersionText = self.limitedVersionText[:-1]
			elif event.keysym in "0123456789":
				self.limitedVersionText += event.keysym
		elif event.keysym == "n":
			self.makeNewNode(random.randint(0, self.width), random.randint(0, self.height))
		elif event.keysym == "i":
			if self.coachSelection:
				self.coachSelection.total_infection(self.coachSelection.getVersion() + 1)

	def onMouseMotion(self, event):
		if self.mouseDown and self.coachSelection:
			self.coachSelection.updateXY(event.x, event.y)

	def onMouseReleased(self, event):
		self.mouseDown = False

	def onMousePressed(self, event):
		(x,y) = (event.x, event.y)
		if 0 <= x <= self.graphW and 0 <= y <= self.graphH:
			self.handleGraphClick(x, y)
		elif (self.graphW + 10 <= x <= self.width - 10 and
				140 <= y <= 175):
			self.limitedFocus = True
			self.limitedVersionFocus = False
		elif (self.graphW + 10 <= x <= self.width - 10 and
			    180 <= y <= 220):
			self.limitedVersionFocus = True
			self.limitedFocus = False
		elif (self.graphW + 10 <= x <= self.width - 10 and
			     225 <= y <= 265):
			try:
				goal = int(self.limitedText)
				newVersion = int(self.limitedVersionText)
				User.limitedInfection(goal, newVersion)
				self.limitedText = ""
				self.limitedVersionText = ""
			except:
				print "failed to do limitedInfection"
				# invalid numbers or empty in the thing
				pass
		elif (self.graphW + 20 <= x <= self.width - 20 and
			    self.height - 60 <= y <= self.height - 20):
			self.coachSelection.total_infection(self.coachSelection.getVersion() + 1)
		else:
			self.limitedFocus = False
			self.limitedVersionFocus = False
		
	def handleGraphClick(self, x, y):
		self.mouseDown = True
		clickedSomething = False
		for node in self.nodes:
			if node.wasClicked(x,y):
				if self.coachSelection == None:
					self.coachSelection = node
					node.select()
				else:
					self.coachSelection.addStudent(node)
					# self.coachSelection.unselect()
					# self.coachSelection = None
				clickedSomething = True
				break
		if not clickedSomething:
			if self.coachSelection:
				self.coachSelection.unselect()
				self.coachSelection = None
			else:
				self.makeNewNode(x, y)

	def makeNewNode(self, x, y):
		self.nodes.append(DrawableUser(self.initVersion, self.nodeCount, x, y))
		self.nodeCount += 1

	def drawSelectedNode(self):
		isCoach = self.coachSelection.isCoach()
		numStudents = str(len(self.coachSelection.getStudents()))
		version = str(self.coachSelection.getVersion())
		self.canvas.create_rectangle(self.graphW + 10, self.height/2 + 10, self.width - 10, self.height - 10,
			fill = "white")
		self.canvas.create_text(self.graphW + 100, self.height/2 + 20, 
			text = "Selected Node", font = self.font)
		self.canvas.create_text(self.graphW + 100, self.height/3 * 2, 
			text = "Version", font = self.font)
		self.canvas.create_text(self.graphW + 100, self.height/3 * 2 + 25, 
			text = version, font = self.font)
		if isCoach:
			self.canvas.create_text(self.graphW + 100, self.height/4 * 3 + 25, 
				text = "Students", font = self.font)
			self.canvas.create_text(self.graphW + 100, self.height/4 * 3 + 50, 
				text = numStudents, font = self.font)
		self.canvas.create_rectangle(self.graphW + 20, self.height - 60,
			self.width - 20, self.height - 20, fill = "green", width = 0)
		self.canvas.create_text(self.graphW + 100, self.height - 40,
			text = "Infect", fill = "black", font = self.font)

	def drawLimitedInfection(self):
		limitedText = self.limitedText if self.limitedText else "Nummber to Infect"
		limitedColor = "black" if self.limitedText else "grey"
		limitedVersionText = self.limitedVersionText if self.limitedVersionText else "New Version"
		limitedVersionColor = "black" if self.limitedVersionText else "grey"
		self.canvas.create_text(self.graphW + 100, 125, text = "Limited Infection",
			fill = "white", font = self.font)
		# text box for number of users to infect
		self.canvas.create_rectangle(self.graphW + 10, 140, self.width - 10, 175,
			fill = "white")
		self.canvas.create_text(self.graphW + 15, 150, text = limitedText,
			anchor = NW, font = self.font, fill = limitedColor)
		# text box for version to give to users
		self.canvas.create_rectangle(self.graphW + 10, 180, self.width - 10, 215,
			fill = "white")
		self.canvas.create_text(self.graphW + 15, 190, text = limitedVersionText,
			anchor = NW, font = self.font, fill = limitedVersionColor)
		# button box to click to execute the infection
		self.canvas.create_rectangle(self.graphW + 10, 225, self.width - 10, 265,
			fill = "red")
		self.canvas.create_text(self.graphW + 100, 245, text = "execute",
			fill = "white")
		if self.limitedFocus and self.textTickerDisplayCounter >= 750:
			self.canvas.create_line(self.graphW + 15 + len(self.limitedText) * 9, 145,
				self.graphW + 15 + len(self.limitedText) * 9, 170)
		if self.limitedVersionFocus and self.textTickerDisplayCounter >= 750:
			self.canvas.create_line(self.graphW + 15 + len(self.limitedVersionText) * 9, 185,
				self.graphW + 15 + len(self.limitedVersionText) * 9, 210)

	def drawSidePane(self):
		self.canvas.create_rectangle(self.graphW, 0, self.width, self.height, 
			fill = "black")
		self.canvas.create_text(self.graphW + 100, 50, text = "Number of Users", 
			fill = "white", font = self.font)
		self.canvas.create_text(self.graphW + 100, 75, text = str(len(self.nodes)), 
			fill = "white", font = self.font)
		if self.coachSelection:
			self.drawSelectedNode()
		self.drawLimitedInfection()

	def redrawAll(self):
		self.canvas.delete(ALL)
		for node in self.nodes:
			node.drawConnections(self.canvas)
		for node in self.nodes:
			node.drawCircle(self.canvas)
		self.drawSidePane()

	def onTimerFired(self):
		if self.doWiggle:
			for node in self.nodes:
				node.wiggle()
		self.textTickerDisplayCounter += self.timerDelay
		if self.textTickerDisplayCounter >= 1500:
			self.textTickerDisplayCounter = 0
