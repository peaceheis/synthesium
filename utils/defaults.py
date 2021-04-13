#frame thingies
DEFAULT_FRAME_WIDTH = 1200
DEFAULT_FRAME_HEIGHT = 675
DEFAULT_FRAME_SIZE = (1200, 675)

#color thingies
PURE_BLUE = (0, 0, 1, 1) 
PURE_RED = (1, 0, 0, 1)
PURE_GREEN = (0, 1, 0, 1)
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)

#cairo thingies
def initialize_surface(ctx, size_x, size_y) : 
    ctx.rectangle(0, 0, size_x, size_y)
    ctx.set_source_rgba(*BLANK)
    ctx.fill()
