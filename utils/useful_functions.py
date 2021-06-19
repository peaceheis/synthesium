    from math import sqrt
def calculate_distance(point1: tuple, point2: tuple): 
        """distance formula, calculated from two coordinate pair tuples"""
        return sqrt((point1[0] - point1[1])**2 + (point2[0] - point2[1])**2)

def rotate(point: tuple, degrees: int, center: tuple, rotates_clockwise: bool = True):
    from math import sin, cos, atan, pi
    """
    A bit confusing, but rotate uses math to calculate the rotation of a Point around another (henceforth the Anchor).
    This is achieved by first setting the Anchor as the "origin" by changing the point's coords
    to the relative x + y distance to the Anchor,
    Then converting from Rectangular to Polar coordinates; they are designed to be good for rotation.
    After adding the desired degrees to the Polar coordinates,
    We convert back to Rectangular coordinates,
    And shift back so that the origin is the origin, not the Anchor.
    """
    
    #set Anchor to be origin 
    point[0] -= center[0]
    point[1] -= center[1]

    #generating polar coordinates
    radius = sqrt(point[0]**2 + point[1]**2)
    try : 
        angle = atan(point[1] / point[0])
    except :
        #prevent errors from being thrown if x == 0 
        if abs(point[1]) == point[1] : 
            angle = pi / 2
        else : 
            angle = 3 * pi / 2

    #rotates by adding the angle (in radians)
    radians = pi * degrees / 180
    if rotates_clockwise : 
        angle -= radians
    else :     
        angle += radians

    #convert back to rectangular coordinates
    point[0] = round(radius * cos(angle), 5)
    point[1] = round(radius * sin(angle), 5) 

    #shift back from center being origin to original location
    point[0] += center[0]
    point[1] += center[1]