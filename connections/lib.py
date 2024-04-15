def is_valid_color(color):
    """Checks if a given color is
        - a tuple
        - has three values 
        - each of which is an int between 0 and 255
    
    Parameters
    ----------
    color : any
    """
    if type(color) is not tuple:
        return False
    if not len(color) == 3:
        return False
    
    for c in color:
        if type(c) is not int or (0 > c) or (c > 255):
            return False
    
    return True