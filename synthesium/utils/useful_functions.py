from math import sqrt


#TODO, write some more rate_funcs

#rate_funcs
def constant(current_frame, total_frames): 
    return 1

def linear_increase(current_frame, total_frames): 
    return current_frame/total_frames

def linear_decrease(current_frame, total_frames): 
    return 1 - current_frame/total_frames

