
import FreeCADGui as Gui
import FreeCAD,Part,Sketcher
App=FreeCAD

import Draft
import numpy as np


'''
multiplizitaet erhoehen
App.ActiveDocument.Sketch.modifyBSplineKnotMultiplicity(7,3,1) 
App.ActiveDocument.Sketch.exposeInternalGeometry(6)
App.ActiveDocument.Sketch.modifyBSplineKnotMultiplicity(6,3,-1) 
'''

def run(name='ribbow',moves=[],box=[40,0,-40,30]):

	label=name
	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	sk=App.activeDocument().addObject('Sketcher::SketchObject',name)
	sk.Label=label
	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	anz=16
	r=50
	pts= [FreeCAD.Vector(r*np.sin(2*np.pi/anz*i),r*np.cos(2*np.pi/anz*i)+50,0) for i in range(anz)]

	for i,p in enumerate(pts):
		sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		if 0:
			#if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000)) 
			if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i)) 
		else:
			radius=2.0
			sk.addConstraint(Sketcher.Constraint('Radius',i,radius)) 
			sk.renameConstraint(i, 'Weight ' +str(i+1))


	k=i+1
	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]


	if 0:
		# open spline
		sk.addGeometry(Part.BSplineCurve(l,False),False)
	else:
		# periodic spline
		#sk.addGeometry(Part.BSplineCurve(l,True),False)
		sk.addGeometry(Part.BSplineCurve(l,None,None,True,3,None,False),False)


	conList = []
	for i,p in enumerate(pts):
		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i,3,k,i))
	sk.addConstraint(conList)
	App.activeDocument().recompute()

	for p in range (0,anz):
		ll=sk.addGeometry(Part.LineSegment(App.Vector(100+10*p,100+10*p,0),App.Vector(-100,-100,0)),False)
		sk.toggleConstruction(ll) 
		sk.addConstraint(Sketcher.Constraint('Coincident',p,3,ll,1)) 
		App.ActiveDocument.recompute()
		if p==anz-1: p=-1
		sk.addConstraint(Sketcher.Constraint('Coincident',p+1,3,ll,2)) 
		App.ActiveDocument.recompute()

	sk.addConstraint(Sketcher.Constraint('Parallel',32,17)) 

	sk.addConstraint(Sketcher.Constraint('Parallel',20,21)) 

	sk.addConstraint(Sketcher.Constraint('Parallel',23,24)) 
	sk.addConstraint(Sketcher.Constraint('Parallel',24,25)) 
	sk.addConstraint(Sketcher.Constraint('Parallel',25,26)) 

	sk.addConstraint(Sketcher.Constraint('Parallel',28,29)) 

	#rahmen rechteck
	if 0:
		sk.addConstraint(Sketcher.Constraint('Horizontal',17)) 
		sk.addConstraint(Sketcher.Constraint('Horizontal',23)) 

		sk.addConstraint(Sketcher.Constraint('Vertical',20)) 
		sk.addConstraint(Sketcher.Constraint('Vertical',28)) 

	else:
		d=sk.addConstraint(Sketcher.Constraint('Angle',23,1,-1,1,np.pi)) 
		sk.renameConstraint(d, u'angleBottom')
		d=sk.addConstraint(Sketcher.Constraint('Angle',-1,1,17,1,0)) 
		sk.renameConstraint(d, u'angleTop')
		d=sk.addConstraint(Sketcher.Constraint('Angle',-1,2,20,1,np.pi/2)) 
		sk.renameConstraint(d, u'angleRight')
		d=sk.addConstraint(Sketcher.Constraint('Angle',29,2,-1,1,np.pi/2)) 
		sk.renameConstraint(d, u'angleLeft')

	# symmetrische Ecken
	sk.addConstraint(Sketcher.Constraint('Equal',21,20)) 
	sk.addConstraint(Sketcher.Constraint('Equal',28,29)) 
	sk.addConstraint(Sketcher.Constraint('Equal',32,17)) 
	sk.addConstraint(Sketcher.Constraint('Equal',23,26)) 


#	sk.addConstraint(Sketcher.Constraint('Symmetric',25,2,24,1,24,2))

	App.activeDocument().recompute()
	Gui.SendMsgToActiveView("ViewFit")

	dd=2
	#d=sk.addConstraint(Sketcher.Constraint('Distance',20,dd)) 
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',4,3,3,3,30)) 
	sk.renameConstraint(d, u'tangentRight')
	
	#d=sk.addConstraint(Sketcher.Constraint('Distance',23,15)) 
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',8,3,6,3,30)) 
	sk.renameConstraint(d, u'tangentBottom')

	#d=sk.addConstraint(Sketcher.Constraint('Distance',25,dd)) 
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',8,3,7,3,10)) 
	sk.renameConstraint(d, u'WidthBottomA')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',9,3,8,3,10)) 
	sk.renameConstraint(d, u'WidthBottomB')


	#d=sk.addConstraint(Sketcher.Constraint('Distance',28,dd)) 
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',11,3,12,3,30)) 

	sk.renameConstraint(d, u'tangentLeft')
	#d=sk.addConstraint(Sketcher.Constraint('Distance',32,dd)) 
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,3,30)) 
	sk.renameConstraint(d, u'tangentTop')

	[r,b,l,t]=box

	sk.movePoint(0,0,App.Vector(0,t,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',0,3,0)) 
	sk.renameConstraint(d, u'p0X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',0,3,t)) 
	sk.renameConstraint(d, u'p0Y')
	App.activeDocument().recompute()

	sk.movePoint(2,0,App.Vector(r,t,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',2,3,r)) 
	sk.renameConstraint(d, u'p2X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',2,3,t)) 
	sk.renameConstraint(d, u'p2Y')
	App.activeDocument().recompute()

	sk.movePoint(14,0,App.Vector(l,t,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',14,3,l)) 
	sk.renameConstraint(d, u'p14X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',14,3,t)) 
	sk.renameConstraint(d, u'p14Y')
	App.activeDocument().recompute()

	sk.movePoint(4,0,App.Vector(r,b+dd,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',4,3,r)) 
	sk.renameConstraint(d, u'p4X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',4,3,b+dd)) 
	sk.renameConstraint(d, u'p4Y')
	App.activeDocument().recompute()

	sk.movePoint(12,0,App.Vector(l,b+dd,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',12,3,l)) 
	sk.renameConstraint(d, u'p12X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',12,3,b+dd)) 
	sk.renameConstraint(d, u'p12Y')
	App.activeDocument().recompute()

	sk.movePoint(8,0,App.Vector(0,b,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',8,3,0)) 
	sk.renameConstraint(d, u'p8X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',8,3,b)) 
	sk.renameConstraint(d, u'p8Y')
	App.activeDocument().recompute()

	print (name,"moves ...")
	for [k,x,y] in moves:
		print (k,x,y)
		sk.movePoint(k,3,App.Vector(x,y,0),0)
		App.activeDocument().recompute()

	return sk



def test():

	sk1=run("rib1",[[8,0,0],[0,0,120],[4,120,-10],[12,-130,0]])
	sk2=run("rib2",[[8,0,0],[0,0,150],[4,70,10],[12,-90,10]])


#target=run("rib3",[],[40,-10,-40,30])