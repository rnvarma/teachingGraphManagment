# eventBasedAnimationClass.py
# Taken and adapted from 15-112 course notes

from Tkinter import *

class EventBasedAnimationClass(object):
    def onMousePressed(self, event): pass
    def onMouseReleased(self, event): pass
    def onMouseMotion(self, event): pass
    def onKeyPressed(self, event): pass
    def onTimerFired(self): pass
    def redrawAll(self): pass
    def initAnimation(self): pass

    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height
        self.timerDelay = 250 # in milliseconds (set to None to turn off timer)

    def onMousePressedWrapper(self, event):
        self.onMousePressed(event)
        self.redrawAll()

    def onMouseReleasedWrapper(self, event):
        self.onMouseReleased(event)
        self.redrawAll()

    def onMouseMotionWrapper(self, event):
        self.onMouseMotion(event)
        self.redrawAll()

    def onKeyPressedWrapper(self, event):
        self.onKeyPressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):
        if (self.timerDelay == None):
            return # turns off timer
        self.onTimerFired()
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)         
    
    def run(self):
        # create the root and the canvas
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.initAnimation()
        # set up events
        def f(event): self.onMousePressedWrapper(event)
        def g(event): self.onMouseReleasedWrapper(event) 
        def h(event): self.onMouseMotionWrapper(event)        
        self.root.bind("<Button-1>", f)
        self.root.bind("<B1-ButtonRelease>", g)
        self.root.bind("<B1-Motion>", h)
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()
        self.root.mainloop()
