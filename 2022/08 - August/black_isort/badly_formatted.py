import mod2
import pyperclip
from mod1 import TestA, abc, TestB, xyz, TestC
import json
from typing import List, Union, Any
import numpy




def mult(
    a: int | str,
    b: int
):
    return a*b




if __name__ == '__main__':
    print( mult( 'a', 10 ) )

    long_var_name_a=10
    long_var_name_b=20
    # a long line of code that goes over the max line length
    if (long_var_name_a and long_var_name_b and long_var_name_a > 10 and long_var_name_b < 100 and long_var_name_a > long_var_name_b):
        print("no idea what that expression actually checks for :-)")
