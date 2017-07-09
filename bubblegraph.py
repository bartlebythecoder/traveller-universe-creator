#!/usr/bin/python

import matplotlib.pyplot as plt

law = (2,4,4,1,1,13,10,0,2,8,7)
accept = (1,9,3,1,5,9,9,1,9,4,2)
tech = (90,90,1100,90,90,80,1000,70,1300,1100,80)
port = ("R",
"G",
"C",
"R",
"C",
"G",
"Y",
"R",
"G",
"C",
"C")
place = ('Swan','Hanlon','Cypher','Toor','Chertsey','Benoit','BP','Bre','Dundas','Efram','Rifaie')


#plt.plot([law], [ycol], 'ro')


plt.xlabel('Law Level')
plt.ylabel('Acceptance Level')
plt.title('The Systems of Jordan, Acceptance and Law')

plt.axis([-1, 11, -1, 11])
plt.scatter(law,accept,s=tech, c = port)

for i, txt in enumerate(place):
	plt.annotate(txt, (law[i]-.25,accept[i]+.25))
	
plt.show()