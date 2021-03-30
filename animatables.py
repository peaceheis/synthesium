from math import sqrt, pi, sin, cos, atan
class Point() : 
    def __init__(self, x, y) : 
        self.x = x
        self.y = y
        self.coords = (x,y)

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

    def __str__(self) :
        return f"{self.x},{self.y}"

    def calculate_distance(self, point2) : 
        #distance formula
        return sqrt( (point2.y - self.y)**2 + (point2.x - self.x)**2 )

    def rotate(self, degrees, center, rotates_clockwise = True) :

        #set center to be origin 
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
        

    def __add__(self, point2) : 
        self.x += point2.get_x()
        self.y += point2.get_y() 
class Curve () : 
    def __init__(self, expression, bound1, bound2) : 
        self.bound1 = bound1
        self.bound2 = bound2
        self.expression = expression

    def generate_expression(self, bound1, bound2) : 
        pass

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

x = Point(0, 1) 
x.rotate(45, Point(0,0))
print(x)

