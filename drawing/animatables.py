from math import sqrt, pi, sin, cos, atan

import cairo


class Animatable() :
    """An object designed to be seen."""
    def __init__(self, *points) : 
        self.points = (*points,)        
    
    def rotate(self, degrees, center, rotates_clockwise = True) : 
        for point in self.points : 
            point.rotate(self, degrees, center, rotates_clockwise)
            
    def shift(self, amt: tuple) : 
        for point in self.points : 
            point = point.shift(amt)
        self = Animatable(*self.points)
        return self
            
#Class dedicated to defining Points across an imaginary coordinate plane,
#Obviously a must-have for animation
class Point() : 
    def __init__(self, x, y) : 
        self.x = x
        self.y = y
        self.coords = (x,y)

    #for purposes of optimization and simplicity, there is no shift_up and shift_left, etc. 
    #but rather a shift method, and direction/distance is controlled via a tuple (amt) of length 4, corresponding to 
    #up, down, right, and down.
    def shift(self, amt: tuple) : 
        if len(amt) != 4 : 
            raise Exception(f"Parameter amt needed tuple or list of length 4, got {type(amt)} of length {len(amt)}")
        self.y += amt[0] #shift up
        self.y -= amt[1] #shift down
        self.x += amt[2] #shift right
        self.x -= amt[3] #shift left
        return self

    #getters and setters
    def set_x(self, x) :
        self.x = x
        self.coords = (x, self.y)

    def get_x(self) : 
        return self.x
    
    def set_y(self, y) : 
        self.y = y
        self.coords = (self.x, y)
    
    def get_y(self, x) :
        return self.y

    def set_coords(self, x, y) :
        self.x = x
        self.y = y
        self.coords = (x, y)
    
    def get_coords(self) : 
        return tuple([self.x, self.y])
    
    def __str__(self) :
        return f"{str(self.get_coords())}"

    def __repr__(self) : 
        return str(self)
    
    def calculate_distance(self, point2) : 
        #distance formula, calculated from the self point and another point.
        return sqrt( (point2.y - self.y)**2 + (point2.x - self.x)**2 )

    def rotate(self, degrees, center, rotates_clockwise = True) :
        #A bit confusing, but rotate uses math to calculate the rotation of a Point around another (henceforth the Anchor).
        #This is achieved by first setting the Anchor as the "origin" by changing the Point's coords
        #to the relative x + y distance to the Anchor,
        #Then converting from Rectangular to Polar coordinates; they are designed to be good for rotation.
        #After adding the desired degrees to the Polar coordinates,
        #We convert back to Rectangular coordinates,
        #And shift back so that the origin is the origin, not the Anchor.
        
        #set Anchor to be origin 
        self.x -= center.x
        self.y -= center.y

        #generating polar coordinates
        radius = sqrt(self.x**2 + self.y**2)
        try : 
            angle = atan(self.y / self.x)
        except :
            #prevent errors from being thrown if x == 0 
            if abs(self.y) == self.y : 
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
        self.x = round(radius * cos(angle), 5)
        self.y = round(radius * sin(angle), 5) 

        #shift back from center being origin to original location
        self.x += center.x
        self.y += center.y
        
    #add two points, functionality for the '+' operator
    def __add__(self, point2) : 
        self.x += point2.get_x()
        self.y += point2.get_y() 
    
    #subtract two points, functionality for the '-' operator
    def __sub__(self, point2) : 
        self.x -= point2.get_x() 
        self.y -= point2.get_y()


class Curve (Animatable) : 
    """An Animatable for objects best represented by mathematics."""
    def __init__(self, expression: str, bound1, bound2) : 
        self.bound1 = bound1
        self.bound2 = bound2 #where the Curve starts and ends.
        self.expression = expression #expression would be anything to the right of "y=", used to draw the curve itself.

    #getters and setters.
    def get_expression(self) : 
        return self.expression
    
    def set_expression(self, expression) : 
        self.expression = expression

    def get_bound1(self) : 
        return self.bound1

    def set_bound1(self, bound1) : 
        self.bound1 = bound1

    def get_bound2(self) : 
        return self.bound2 

    def set_bound2(self, bound2) :
        self.bound2 = bound2 
        
    def evaluate(self, number, variable_name = "x") : 
        number = str(number)
        return eval(self.expression.replace(variable_name, number))

class Bezier(Animatable) : 
    pass #to be implemented later

class Line(Animatable) : 
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
    
class Polygon(Animatable) : 
    """Base class for Polygons, as the name suggests."""
    def __init__(self, *points) : 
        self.num_points = len(points)
        self.points = tuple(points) #points is a tuple containing Point objects.
        temp = []
        for i in range(len(points)) : 
            temp.append(points[i].get_coords())
            exec(f"self.point{i+1} = points[{i}]")
        self.vertices = tuple(temp) #vertices is a tuple containing tuple coordinate pairs.
    
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
    
    def draw(self, ctx: cairo.Context, color: tuple) : 
        try :
            ctx.set_source_rgba(*color)
        except : 
            raise Exception(f"Parameter Color must have 4 entries, r, g, b, and a. Recieved argument of length {len(color)}")
        point1 = self.vertices[0]
        x, y = 0, 1        
        ctx.move_to(point1[x], point1[y]) #since point1 is a tuple, access the first and second elements as x and y.
        for i in range(len(self.points) - 1) : 
            current_point = self.vertices[i+1]
            ctx.line_to(current_point[x], current_point[y])
        ctx.close_path()    
        ctx.fill()
        
    def shift(self, amt: tuple) : 
        for point in self.points : 
            point = point.shift(amt)
        
        self = Polygon(*self.points)
        return self
       
        
    
class Quadrilateral(Polygon) :
    """Class for any Quadrilaterals, inheriting from Polygon."""
    def __init__(self, point1, point2, point3, point4) : 
        super().__init__(point1, point2, point3, point4)

class Circle(Animatable) : 
    def __init__(self, center, radius) : 
        self.center = center
        self.radius = radius
        self.circumference = pi * (radius **2) 

class Triangle(Polygon) : 
    def __init__(self, point1, point2, point3) : 
        self.points = (point1, point2, point3)
        self.point1 = point1
        self.point2 = point2 
        self.point3 = point3
