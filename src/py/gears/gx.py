# http://jamesgregson.blogspot.com/2012/05/python-involute-spur-gear-script.html

import math

# =================================================================================
# =================================================================================
# Spur-gear generation script
# (c) James Gregson, 2012
# Free for all use, including commercial, but do not redistribute. 
# Use at your own risk.
#
# Notes:
#  - seems to work well for pressure angles up to about 30 degrees
# =================================================================================
# =================================================================================


# Diameters

def gears_root_diameter(teeth, pitch):
    """
    compute the root diameter of a gear with a given pressure-angle
    """
    return (teeth-2.5)/pitch


def gears_base_diameter(pressure_angle, teeth, pitch):
    """
    compute the base diameter of a gear with a given pressure-angle
    """
    return gears_pitch_diameter(teeth, pitch) * math.cos(pressure_angle * math.pi/180.0)


def gears_outer_diameter(teeth, pitch):
    """compute the outer diameter of a gear with a given pressure-angle"""
    return gears_pitch_diameter(teeth, pitch) + 2.0 * gears_addendum(pitch)


def gears_pitch_diameter(teeth, pitch):
    """compute the outer diameter of a gear with a given pressure-angle"""
    return float(teeth) / float(pitch)


def gears_circular_pitch(pitch):
    """compute the outer diameter of a gear with a given pressure-angle (pa)"""
    return math.pi / float(pitch)


def gears_circular_tooth_thickness(pitch, backlash=0.05):
    """
    compute the circular tooth thickness of a gear with a given 
    """
    return gears_circular_pitch(pitch) / (2.0+backlash)


def gears_circular_tooth_angle(teeth, pitch):
    """compute the circular tooth angle of a gear with a given"""
    return gears_circular_tooth_thickness(pitch) * 2.0 / gears_pitch_diameter(teeth, pitch)


def gears_addendum(pitch):
    """compute the addendum height for a gear with a given"""
    return 1.0 / float(pitch)


def gears_dedendum(pitch):
    return 1.25 / float(pitch)


def generate_involute_curve(radius, r_max, theta_max, steps=30):
    """generates an involute curve from a circle of radius r up to theta_max radians
    with a specified number of steps
    """

    dtheta = theta_max / float(steps)
    x = []
    y = []
    theta = []
    rlast = radius

    for i in range(steps+1):
        xx = i * dtheta

        c = math.cos(xx)
        s = math.sin(xx)
        tx = radius * (c + xx*s)
        ty = radius * (s - xx*c)

        distance = math.sqrt(tx**2 + ty**2)

        if distance > r_max:
            a = (r_max - rlast)/ (distance - rlast)
            tx = x[-1] * (1.0-a) + tx*a
            ty = y[-1] * (1.0-a) + ty*a

            x.append(tx)
            y.append(ty)

            ttheta = theta[-1]*(1.0-a) + math.atan2( ty, tx ) * a
            theta.append(ttheta)
            break

        else:
            x.append(tx) 
            y.append(ty)
            theta.append( math.atan2( ty, tx) )

    return x, y, theta




def locate_involute_cross_angle_for_radius(r, ix, iy, itheta):
    """
    returns the angle where an involute curve crosses a circle with a given radius
    or -1 on failure
    """

    for i in range( 0, len(ix)-1 ):
        r2 = ix[i+1]*ix[i+1] + iy[i+1]*iy[i+1]
        if r2 > r*r:
            r1 = math.sqrt( ix[i]*ix[i] + iy[i]*iy[i] )
            r2 = math.sqrt( r2 )
            a = (r-r1)/(r2-r1)
            return itheta[i]*(1.0-a) + itheta[i+1]*a
    return -1.0


def gears_align_involute(Dp, ix, iy, itheta):
    """
    rotates the involute curve around the gear center in order to have the involute
    cross the x-axis at the pitch diameter
    """

    theta = -locate_involute_cross_angle_for_radius(Dp/2.0, ix, iy, itheta)

    c = math.cos(theta)
    s = math.sin(theta)

    for i in range(len(ix)):
        tx = c*ix[i] - s*iy[i]
        ty = s*ix[i] + c*iy[i]
        ix[i] = tx
        iy[i] = ty

    return ix, iy


def gears_mirror_involute( ix, iy ):
    """
    reflects the input curve about the x-axis to generate the opposing face of a tooth
    """
    tx = []
    ty = []

    for i in range(len(iy)):
        tx.append(ix[len(iy)-1-i])
        ty.append(-iy[len(iy)-1-i])

    return tx, ty


def gears_rotate(theta, ix, iy):
    """
    rotates the input curve by a given angle (in radians)
    """

    c = math.cos(theta)
    s = math.sin(theta)

    x = []
    y = []
    for i in range(len(ix)):

        tx = c*ix[i] - s*iy[i]
        ty = s*ix[i] + c*iy[i]
        x.append(tx)
        y.append(ty)

    return x, y


def gears_translate( dx, dy, ix, iy ):
    """translates the input curve by [dx, dy]"""
    x = []
    y = []

    for i in range(len(ix)):
        x.append(ix[i]+dx)
        y.append(iy[i]+dy)

    return x, y
    

def make_tooth(pressure_angle, teeth, pitch):
    """generates a single tooth profile of a spur gear"""

    base_diameter = gears_base_diameter(pressure_angle, teeth, pitch ) / 2.0
    outer_diameter = gears_outer_diameter(teeth, pitch ) / 2.0
    root_diameter = gears_root_diameter(teeth, pitch) / 2.0
    pitch_diameter = gears_pitch_diameter(teeth, pitch)

    ix, iy, itheta = generate_involute_curve(base_diameter, outer_diameter, math.pi/2.1 ) # 2.1??

    ix.insert(0, min(base_diameter, root_diameter))
    iy.insert(0, 0.0)
    itheta.insert(0, 0.0)

    ix, iy = gears_align_involute(pitch_diameter, ix, iy, itheta)

    mx, my = gears_mirror_involute(ix, iy)
    mx, my = gears_rotate(gears_circular_tooth_angle(teeth, pitch ), mx, my )

    ix.extend(mx)
    iy.extend(my)

    return ix, iy


def make_gear(diameter, pressure_angle, teeth, pitch):
    """
    generates a spur gear with a given pressure angle, number of teeth and pitch
    """
    tx, ty = make_tooth(pressure_angle, teeth, pitch)
    print(tx)
    print(ty)

    x = []
    y = []

    for i in range(teeth):
        m = float(i) * 2.0 * math.pi / float(teeth)
        rx, ry = gears_rotate(m, tx, ty)
        x.extend(rx)
        y.extend(ry)

    x.append(x[0])
    y.append(y[0])
    
    x = [e * diameter for e in x]
    y = [e * diameter for e in y]

    return zip(x, y)


def rhino_gear(diameter, pressure_angle, teeth, pitch):
    import rhinoscriptsyntax as rs

    px = make_gear(diameter, pressure_angle, teeth, pitch)
    points = [(x, y, 0) for (x, y) in px]
    return rs.AddPolyline(points)


if __name__ == "__main__":
    print(rhino_gear(1, 20, 20, 12))
    #make_gear(1, 20, 10, 8)

