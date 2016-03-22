# https://heritagerobotics.wordpress.com/2014/02/26/python-gear-generator-for-freecad/

# Copyright 2013 Arno Wilhelm 
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see .

import Part
from FreeCAD import Base
from math import *

# get the angle between (0,0,0) and two points where the involute
# intersects at a given radius
def getInvoluteIntersectAngle(innerRadius, outerRadius):
    innerRadius, outerRadius = float(innerRadius), float(outerRadius)
    return (sqrt(outerRadius**2 - innerRadius**2) / (innerRadius)) - (acos(innerRadius / outerRadius))

# calculate Point on Circle in x-y plane with given radius and angle:
#              |
#  alpha       | y
# -------------|
#        x
#     sin(alpha) = y / radius => y = sin(alpha)*radius
#     cos(alpha) = x / radius => x = cos(alpha)*radius
def getPointOnCircle(radius, angle):
    x = radius * cos(radians(angle))
    y = radius * sin(radians(angle))
    return App.Vector( x, y, 0.0)

class Gear:
    def __init__(self, obj):
        ''' Add the properties: NumberTeeth, Module, PressureAngle, GearHeight, CenterRadius, Verbose (see Property View)'''
        obj.addProperty("App::PropertyInteger","NumberTeeth","Gear","Number of teeth").NumberTeeth=20
        obj.addProperty("App::PropertyFloat","Module","Gear","The length in mm of the pitch circle diameter per tooth.").Module=10.0
        obj.addProperty("App::PropertyAngle","PressureAngle","Gear","Pressure Angle (common values: 14.5, 20, 25 degrees)").PressureAngle=20.0
        obj.addProperty("App::PropertyLength","GearHeight","Gear","Height of gear (=material thickness)").GearHeight=10.0
        obj.addProperty("App::PropertyLength","CenterRadius","Gear","Radius of center hole (used for mounting shaft)").CenterRadius=10.0
        obj.addProperty("App::PropertyInteger","LevelOfDetail","Gear","Level of detail of involute. The higher the number the more detail but calculation time increases.").LevelOfDetail=10
        obj.addProperty("App::PropertyBool","Verbose","Gear","Verbose mode shows data in output window.").Verbose=True
        obj.Proxy = self

    def onChanged(self, fp, prop):
        if prop == "NumberTeeth" or prop == "Module" or prop == "PressureAngle" or prop == "GearHeight" or prop == "CenterRadius" or prop == "LevelOfDetail" or prop == "Verbose": #if one of these is changed
            self.execute(fp)

    # main part of script
    def execute(self, fp):
        numberTeeth        = fp.NumberTeeth
        module             = fp.Module
        pressureAngle      = fp.PressureAngle
        gearHeight         = fp.GearHeight
        centerRadius       = fp.CenterRadius
        nrPoints2Calculate = fp.LevelOfDetail
        verbose            = fp.Verbose

        # sometimes position changes (why?): remeber value and reassign at end of method:
        #print "-> Name: %s" % fp.Name
        #print "-> Placement: %s" % fp.Placement
        #print "-> Placement.Base: %s" % fp.Placement.Base
        #print "-> Placement.Rotation: %s" % fp.Placement.Rotation
        placementBase = fp.Placement.Base
        placementRotation = fp.Placement.Rotation

        if numberTeeth <= 5:
            raise Exception("Error: Number of teeth must not be <= 5 !")
        if module  70:
            raise Exception("Error: Module out of range! Must be >= 0.1 and <= 70.")
        if gearHeight <= 0:
            raise Exception("Error: Height of gear must not be <= zero !")
        if centerRadius < 0:
            raise Exception("Error: Radius of center must not be negativ !")
        if nrPoints2Calculate < 3:
            raise Exception("Error: Level of detail must not be = 1 and module <=70:          #DIN 3960 (1987) 1 <= m  0.6 and module < 1:     #DIN 5840 (1984) 0.6 < m = 0.1 and module <= 0.6: #DIN 5840 (1984) 0.1 <= m <= 0.6 : hp = 2.6 * m")
            wholeDepth = 2.6 * module
#        Old version:
#        if module  rootRadius + 1:
            raise Exception("Error: Diameter of hole in center may not be greater then gear itself!")

        if verbose:
            print "\nNumber Teeth:  %s" % numberTeeth
            print "Module:          %s" % module
            print "Pressure Angle:  %s" % pressureAngle

            print "Diametral Pitch: %s" % (25.4 / module)
            print "Circular Pitch:  %s" % circularPitch
            print "Circular Tooth Thickness: %s" % circularToothTickness

            print "Whole Depth:     %s" % wholeDepth
            print "Addendum:        %s" % addendum
            print "Dedendum:        %s" % dedendum

            print "Outer Diameter:  %s" % outerDiameter
            print "Pitch Diameter:  %s" % pitchDiameter
            print "Base Diameter:   %s" % baseDiameter
            print "Root Diameter:   %s" % rootDiameter
            print "Outer Radius:    %s" % outerRadius
            print "Pitch Radius:    %s" % pitchRadius
            print "Base Radius:     %s" % baseRadius
            print "Root Radius:     %s" % rootRadius

        # draw outer circle
        outerCircle = Part.Circle()
        outerCircle.Radius = outerRadius
        outerCircleObj = fp.Document.addObject("Part::Feature", "Outer Circle")
        outerCircleObj.ViewObject.LineWidth = 1.0
        outerCircleObj.ViewObject.LineColor = (0.00,0.00,1.00)
        outerCircleObj.Shape = outerCircle.toShape()
        outerCircleObj.ViewObject.hide()

        # draw pitch circle
        pitchCircle = Part.Circle()
        pitchCircle.Radius = pitchRadius
        pitchCircleObj = fp.Document.addObject("Part::Feature", "Pitch Circle")
        pitchCircleObj.ViewObject.LineWidth = 1.0
        pitchCircleObj.ViewObject.LineColor = (0.00,0.00,1.00)
        pitchCircleObj.Shape = pitchCircle.toShape()
        pitchCircleObj.ViewObject.hide()

        # draw base circle
        baseCircle = Part.Circle()
        baseCircle.Radius = baseRadius
        baseCircleObj = fp.Document.addObject("Part::Feature", "Base Circle")
        baseCircleObj.ViewObject.LineWidth = 1.0
        baseCircleObj.ViewObject.LineColor = (0.00,0.00,1.00)
        baseCircleObj.Shape = baseCircle.toShape()
        baseCircleObj.ViewObject.hide()

        # draw root circle
        rootCircle = Part.Circle()
        rootCircle.Radius = rootRadius
        rootCircleObj = fp.Document.addObject("Part::Feature", "Root Circle")
        rootCircleObj.ViewObject.LineWidth = 1.0
        rootCircleObj.ViewObject.LineColor = (0.00,0.00,1.00)
        rootCircleObj.Shape = rootCircle.toShape()
        rootCircleObj.ViewObject.hide()

        # draw crosshair
        verticalCross=Part.Line()
        verticalCross.StartPoint=(0.0,-(outerRadius+10),0.0)
        verticalCross.EndPoint=(0.0,(outerRadius+10),0.0)
        verticalCrossObj=fp.Document.addObject("Part::Feature","Vertical Cross")
        verticalCrossObj.ViewObject.LineWidth = 0.5
        verticalCrossObj.ViewObject.LineColor = (0.57,0.57,0.57)
        verticalCrossObj.Shape = verticalCross.toShape()
        verticalCrossObj.ViewObject.hide()

        horizontalCross=Part.Line()
        horizontalCross.StartPoint=(-(outerRadius+10),0.0, 0.0,)
        horizontalCross.EndPoint=((outerRadius+10),0.0, 0.0,)
        horizontalCrossObj=fp.Document.addObject("Part::Feature","Horizontal Cross")
        horizontalCrossObj.ViewObject.LineWidth = 0.5
        horizontalCrossObj.ViewObject.LineColor = (0.57,0.57,0.57)
        horizontalCrossObj.Shape = horizontalCross.toShape()
        horizontalCrossObj.ViewObject.hide()

        # calculate angle of involute curve from base circle to outer circle
        toothFlankAngle = (sqrt( outerRadius*outerRadius - baseRadius*baseRadius )) / baseRadius
        if verbose: print "Angel of Tooth Flank: %s" % toothFlankAngle

        # divide the toothFlankAngle trough the number of points that should be
        # calculated along the involute curve in order to construct this curve.
        # The higher the number of points the smaller the single angle and the more
        # detailed the resulting curve
        singleAngle = toothFlankAngle / float(nrPoints2Calculate)

        # calculate x and y coordinate for each point along the involute curve where the
        # angle = [0 : nrPoints2Calculate]*singleAngle  1:
                line = Part.Line(pointList[-2], pointList[-1])
                lineList.append(line.toShape())

        involuteWire = Part.Wire(lineList)
        # draw line from end of involute to root cirlce.
        # This line goes from endpoint of involute (on base circle) to root circle
        # in the direction towards the center of the gear and provides clearence.
         # either: rootLine = Part.Line(pointList[0], getPointOnCircle(rootRadius, 0) )
         # or mais simple because endpoint of involute lies on x-axis :O :
        rootLine = Part.Line(App.Vector(rootRadius, 0), App.Vector(baseRadius, 0) )
        rootLineWire=Part.Wire(rootLine.toShape().Edges)
        involute = Part.Wire([rootLineWire, involuteWire])

        # calculate mirror line for single tooth flank
        # mirror line goes trough (0,0,0) and the point on the pitch circle where
        # lenght along pitch circle = circularToothTickness/2
        # calculate angle:
        # Attention: since the involute starts at the base circle at angle 0 but
        # the angle of mirrorline is calculated from point were involute intersects
        # pitch circle we have to add this angle to the mirror angle.
            # Die Laenge b eines Kreisbogens mit dem Mittelpunktswinkel alpha im Winkelmass
            # und dem Radius r lewsst sich durch folgende Formel berechnen:
            # b = pi * r (alpha\180) => alpha = (b * 180) / (pi * r)
            # mirrorAngle = ( (circularToothTickness/2.0) * 180.0) / ( pi * pitchRadius )
            # OR MUCH EASIER :): mirrorAngle = (360.0 / numberTeeth) / 4.0
        toothAngle = 360.0 / numberTeeth
        baseToPitchAngle = getInvoluteIntersectAngle( baseRadius, pitchRadius )
        # TODO: is this baseToPitchAngle in degree or radians ?! Is calculation right??
        #mirrorAngle = (toothAngle/4.0) + degrees(baseToPitchAngle)
        #mirrorAngle = toothAngle/4.0
        mirrorAngle = (toothAngle/4.0) + baseToPitchAngle
        mirrorPoint = getPointOnCircle(outerRadius, mirrorAngle)

        if verbose:
            print "Angle single tooth occupies: %s" % toothAngle
            print "Angle between involute on base circle and involute on pitch circle: %s ?!" % baseToPitchAngle
            print "Mirror angel: %s" % mirrorAngle
            print "Mirror point: %s" % mirrorPoint

        # mirror involute around line in middle of tooth (=mirrorLine)
        # calculate the transform matrix for reflection around arbitrary line through (0,0,0)
        # see: http://www.scibuff.com/2009/06/22/reflection-matrix/
        # see: http://answers.yahoo.com/question/index?qid=20110628095842AARdMwL
        # see: http://www.geom.uiuc.edu/docs/reference/CRC-formulas/node9.html
        oans = float(cos(2*radians(mirrorAngle)))
        zwoa = float(sin(2*radians(mirrorAngle)))
        drai = float(sin(2*radians(mirrorAngle)))
        via =  float(-(cos(2*radians(mirrorAngle))))
        mirrorMatrix = Base.Matrix(oans,zwoa,0.0,0.0,drai,via,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
        if verbose: print "mirrorMatrix: %s" % mirrorMatrix
        mirrorInvolute = involute.transformGeometry(mirrorMatrix)
        # Since the vertexes in the mirrored involute are reversed in the list of vertices ->
        # -> in order to join them successfully with the other wires we have to reverse them:
        edgeList = []
        for i in xrange(len(mirrorInvolute.Vertexes)-1, -1, -1):
            if i  0:
            centerHole = Part.Circle()
            centerHole.Radius = float(centerRadius)
            centerHoleShape = centerHole.toShape()
            centerHoleFace = Part.Face(Part.Wire(centerHoleShape.Edges))
            gearFace = gearFace.cut(centerHoleFace)

        gearShell = Part.Shell(gearFace.Faces)
        extrudedGear = gearShell.extrude(Base.Vector(0.0,0.0,gearHeight))
        fp.Shape = extrudedGear

        # sometimes position changes (why?): reset positon to rembered value:
        fp.Placement.Base = placementBase
        fp.Placement.Rotation = placementRotation

def makeGear():
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument("Gear")
    gear=doc.addObject("Part::FeaturePython","Gear") #add object to document
    gear.Label = "Gear"
    Gear(gear)
    gear.ViewObject.Proxy=0
    doc.recompute()
    Gui.SendMsgToActiveView("ViewFit") # center gear in view ...

if __name__ == "__main__": #feature will be generated after macro execution
    makeGear()
