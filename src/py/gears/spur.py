# Spur gears based on 
# https://www.bostongear.com/pdf/gear_theory.pdf

import math



class Tooth(object):
    """
    """

    def __init__(self, pressure_angle, teeth, pitch):
        self.pressure_angle = pressure_angle
        self.teeth = teeth
        self.pitch = pitch

    def generate_dimensions(self):

        base_diameter = gears_base_diameter(self.pressure_angle, self.teeth, self.pitch ) / 2.0
        outer_diameter = gears_outer_diameter(self.teeth, self.pitch ) / 2.0
        root_diameter = gears_root_diameter(self.teeth, self.pitch) / 2.0
        pitch_diameter = gears_pitch_diameter(self.teeth, self.pitch)



class Involute(object):
    """
    An involute curve.
    """
    
    def __init__(self, radius, r_max, theta_max, steps=30):
        self.radius = radius
        self.r_max = r_max
        self.theta_max = theta_max
        self.steps = steps


    def helper(self, i):
        it = i * dtheta
        ct = math.cos(it)
        st = math.sin(it)

        tx = self.radius * (ct + it * st)
        ty = self.radius * (st - it * ct)
        
        return (tx, ty)



    def generate(self):
        dtheta = self.theta_max / float(self.steps)
        x = []
        y = []
        theta = []

        rlast = self.radius

        for i in range(self.steps+1):

            tx, ty = self.helper(i)

            distance = math.sqrt(tx**2 + ty**2)

            if distance < self.r_max:
                x.append(tx) 
                y.append(ty)

                ttheta = math.atan2(ty, tx)
                theta.append(ttheta)

            else:
                a = (self.r_max - rlast)/ (d - rlast)
                tx = x[-1] * (1.0-a) + tx*a
                ty = y[-1] * (1.0-a) + ty*a

                x.append(tx)
                y.append(ty)

                ttheta = theta[-1] * (1.0 - a) + math.atan2(ty, tx) * a
                theta.append(ttheta)

                break

            else:

        return x, y, theta




def make_gear(pressure_angle, teeth, pitch):
    """
    generates a spur gear with a given pressure angle, number of teeth and pitch
    """

    l = []

    x = []
    y = []

    tx, ty = make_tooth(pressure_angle, teeth, pitch)

    for i in range(teeth):

        m = float(i) * 2.0 * math.pi / float(teeth)
        rx, ry = gears_rotate(m, tx, ty)
        x.extend(rx)
        y.extend(ry)

    x.append(x[0])
    y.append(y[0])

    return x, y

