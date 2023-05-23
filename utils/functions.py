
import random

from utils.consts import NO_WALLS


class Functions:
    def return_true() -> bool:
        return True
    
    def return_false() -> bool:
        return False
    
    def return_random_bool() -> bool:
        return random.choice([False, True])
    
    def return_number_of_walls() -> int:
        return NO_WALLS
    
    def return_zero() -> int:
        return 0
    
    def return_random_number_of_walls() -> int:
        return random.randint(0, NO_WALLS)