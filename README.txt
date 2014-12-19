Author: Rohan Varma
Made for Khan Academy Project Interview

Impliments algorithms and visualization for maintaining a set of Users that
can act as Students, Coaches, or neither. A 'total infection' is when one
person has its version of software upgraded. This leads to every person on
that connected component of the graph to also be upgraded. A 'limited infection'
is when the manager wants to upgrade x people to a certain version throughout
the entire graph.

Two main files:
-------------------
infections.py
	- manages the backend in the User class

visualization.py
	- model-view-controller based tkinter application to visualize graph 

HOWTO:
------------------
python main.py test
	- this will run the tests for the graph algorithm

python main.py visualize
	- will launch the visualizer

GUIDE TO VISUALIZER
------------------

IMPORTANT: in infections.py, set the "DEFAULT_ERROR_ALLOWED" variable to whatever
	you would like to default error to be. Important for visualizer because
	cannot specify error amount on the visualizer

Creating nodes in graph: click on the white graph area to initialize a new node

Creating a coach->student relationship: select a node by clicking on it. then
	click on the desired student node to make the selecte node a coach of it

Total infection: click on a node and press the total infection button on the
	left side bar to do total infection and make the verison one more than previously

Limited Infection: at any time use the operations on the right hand side: type
	in the number of nodes you want to infect and the new version then press the button!