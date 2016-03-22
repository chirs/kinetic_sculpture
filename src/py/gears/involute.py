# Draw involute curves.

# http://web.mit.edu/harishm/www/papers/involuteEWC.pdf

# A transcendental equation is an equation containing a transcendental function of the variable(s) being solved for. Such equations often do not have closed-form solutions. Examples include:

import math


def simple(r, steps, step):
    """
    Generate a very simple involute curve.
    """
    l = []
    for i in range(steps):
        theta = i * step
        x = r * (math.cos(theta) + theta * math.sin(theta))
        y = r * (math.sin(theta) - theta * math.cos(theta))
        l.append((x, y, 0))

    return l


def main():
    import rhinoscriptsyntax as rs
    
    for e in range(1, 50):
        dx = .1 / e
        points = simple(e, 10000, dx)
        rs.AddPolyline(points)



if __name__ == "__main__":
    main()
        
        
    
    
