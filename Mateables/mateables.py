from math import sqrt, pi, sin, cos, atan

from point import Point


class Matable() :
    """Short for Animatable Object, a Matable is designed to hold points and instructions on how to connect them."""
    def __init__(self, *points) : 
        self.points = (*points,)        
    
    def rotate(self, degrees, center, rotates_clockwise = True) : 
        for point in self.points : 
            point.rotate(self, degrees, center, rotates_clockwise)
            
    def shift(self, amt: tuple) : 
        for point in self.points : 
            point = point.shift(amt)
        self = Matable(*self.points)
        return self
            
    def __init__(self, x, y) : 
        self.x = x
        self.y = y
        self.coords = (x,y)


class Bezier(Matable) : 
    pass #to be implemented later

class Line(Matable) : 
    """A class made for straight lines going between two Points."""
    def __init__(self, bound1 : Point, bound2 : Point) : 
        self.bound1 = bound1
        self.bound2 = bound2
    
    #getters and setters
    def set_bound1(self, bound1) :
        self.bound1 = bound1
        
    def get_bound1(self) :
        return self.bound1
    
    def set_bound2(self, bound2) : 
        self.bound2 = bound2
        
    def get_bound2(self) : 
        return self.bound2
    
class Polygon(Matable) : 
    """Base class for Polygons, as the name suggests."""
    def __init__(self, *points) : 
        self.num_points = len(points)
        self.points = {f"{i}": point for i, point in enumerate(points)} #dictionary comprehension is SO powerful, it's frightening.
        self.vertices = {f"{i}": point.get_coords() for i, point in enumerate(points)} #self.vertices is for a quick way to access the raw coodinates, not Point objects.
    
    def get_num_points(self) : 
        return len(self.points)
    
    def get_points(self) : 
        return self.points

    def __str__(self) : 
        string = ""
        for i, point in enumerate(self.points) : 
            string += f"{i}: {point}\n"
        return string
    
    def __repr__(self) : 
        return f"Polygon of type {type(self)}, {str(self)}"
        
    def shift(self, amt: tuple) : 
        for point in self.points : 
            point = point.shift(amt)
        
        self = Polygon(*self.points)
        return self
       
        
    
class Quadrilateral(Polygon) :
    """Class for any Quadrilaterals, inheriting from Polygon."""
    def __init__(self, point1, point2, point3, point4) : 
        super().__init__(point1, point2, point3, point4)

class Circle(Matable) : 
    def __init__(self, center, radius) : 
        self.center = center
        self.radius = radius
        self.circumference = pi * (radius **2) 

class Triangle(Polygon): 
    def __init__(self, point1, point2, point3): 
        self.points = (point1, point2, point3)
        self.point1 = point1
        self.point2 = point2 
        self.point3 = point3

test_polygon = Polygon(Point(1, 2), Point(2, 3), Point(3, 4))
print(test_polygon)