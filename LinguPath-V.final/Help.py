Help = """
Hey! This, is a calculator project.
The core uses Sympy to calculate your queries.

Here is the basic guide that you may want to know before using:
- Enter "help" to see this helper section.
- Enter "exit" to close the program (there's no other way to do that).
- Enter "clrp" to clear the terminal screen.
- Math capabilities: (expression: literally every expression that sympy supports.)
  1 - To save an expression as a function, use this format:
        save function_name : [your expression]
        e.g.:
        save f: x**2+y
  2 - To see your saved function, use this format:
        show function_name
  3 - To evaluate a saved function at an arbitrary point (can use other funcs too), use this format:
        eval function_name : [your point]
        e.g.:
        eval f: x:5,y:6,etc...
  4 - To solve a set of equations (previously saved), use this format:
        solv no_of_equations,variables
        func1_name+... = func2_name+...
        equation5
        etc...
        e.g.:
        solv 2,x,y
        f+5*x=g
        f=h**2
        eqA
  5 - To plot your saved functions, use this format (default range is always [-10,10]):
        plot number_of_functions
        func1_name, min_range, max_range
        etc...
  6 - To store all functions in a file for later use, use this format:
        STOR file_name
  7 - To load all functions from a file, use this format:
        LOAD file_name

Note: 
- function names should not include spaces. 
- if they do, everything after the first space will be ignored.
- math syntax is exactly like sympy. for example, powers should be written as "**" not "^".

Feel free to ask further questions via my github page at https://github.com/Clark-Castro/LinguPath-uniproject
"""
