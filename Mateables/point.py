from math import sqrt, pi, sin, cos, atan

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
