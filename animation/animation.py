"""Make the animatables MOVE.

Animations are a series of functions that get applied to Animatables.
They return a tuple that holds all the shifts (in tuples) that need to be made to an Animatables points over the necessary amount of frames.
"""

from synthesium.drawing.animatables import *

def shift(target: Animatable, amt: tuple, time: float, fps: float) -> tuple: 
    #TODO, implement rate functions
    num_frames = time * fps
    
    if len(amt) != 4 or type(amt) not in [tuple, list] : 
        raise Exception(f"Parameter amt needed tuple or list of length 4, got {type(amt)} of length {len(amt)}")
    
    #make a list of amount tuples of length 4, for up, down, right, left
    temp = []
    previous = [0, 0, 0, 0]
    for i in range(4) :
        previous[i] += amt[i] / num_frames
        
    for i in range(num_frames) : 
        small_temp = []
        for j in range(4) : 
            x = amt[j] / (num_frames - i) + previous[j] * i
            small_temp.append(x)
        temp.append(tuple(small_temp))
    return tuple(temp)
    
    
    
