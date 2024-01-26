import json
from sympy import *
from sympy.abc import x, y, z
from sympy.plotting.plot import plot3d
from random import random as r


class DataBase:
  def __init__(self):
    self.Funcs={}
    self.Equas={}

  def add(self, name, expr, TYPE):
    #check for duplicates
    if self.fndfunc(name) is not None or self.fndequa(name) is not None:
      return self.ERROR(5,name)
    
    #equation preprocess
    if TYPE:
      leftside, rightside = expr.split("=")

      #interpreting
      try:
        leftside = sympify(leftside)
        rightside = sympify(rightside)
        res = Eq(simplify(leftside.subs(self.Funcs) - rightside.subs(self.Funcs)),0)
      except:
        return self.ERROR(3)
      
      #atom check
      ATOM = sorted(self.fndatom(leftside)+self.fndatom(rightside))
      if ATOM is not None:
        self.addequa(name, res, ATOM)
        return 1
    
    #function preprocess
    else:
      #interpreting
      try:
        res = simplify(sympify(expr).subs(self.Funcs))
      except:
        return self.ERROR(3)
      
      #atom check
      ATOM = self.fndatom(res)
      if ATOM is not None:
        self.addfunc(name, res)
        return 1    
      
    #fail
    return 0
  
  def addfunc(self, fname, fexpr):
    self.Funcs.update({fname:fexpr})
  
  def addequa(self, ename, eexpr):
    self.Equas.update({ename:eexpr})
  
  def fnd(self, name):
    fnc = self.fndfunc(name)
    equ = self.fndequa(name)
    if fnc is not None:
      pprint(fnc)
      return fnc
    elif equ is not None:
      pprint(equ)
      return equ
    else:
      return self.ERROR(4, name)

  def fndfunc(self, fname):
    return self.Funcs.get(fname)
  
  def fndequa(self, ename):
    return self.Equas.get(ename)
  
  def fndatom(self, expr):
    res = list(expr.atoms(Symbol))
    for i in range(len(res)):
      res[i] = str(res[i])
      if res[i] not in "xyz":
        return self.ERROR(2, res[i])
    return sorted(res)

  def evl(self, fname, fpont):
    F = self.fnd(fname)
    if F is not None:
      try:
        fpont = {key:Float(value) for key,value in fpont}
        res = F.subs(self.Funcs).evalf(subs=fpont, chop=true)
      except:
        res = F.subs(self.Funcs).subs(fpont).subs(self.Funcs)
        pass
      
      pprint(res)
      return res
    else:
      return self.ERROR(4,fname)

  def makequa(self, inp):
    inpl = sympify(inp[0]).subs(self.Funcs)
    inpr = sympify(inp[1]).subs(self.Funcs)
    res = Eq(simplify(inpl-inpr),0)
    return res

  def slv(self, equations, variables):
    sol = None
    gsol = None
    if len(variables)==1:
      ANSS = []
      for i in equations:
        ANSS.append(solveset(i,variables[0]))
      gsol = ANSS[0]
      for i in ANSS:
        gsol = Intersection(gsol, i)
    sol = solve(equations, variables)
    
    print("The solution is represented as: ")
    pprint(sol)
    print()

    if gsol is not None:
      print("The general solution is of the form:")
      pprint(gsol)

    return [sol,gsol]

  def plt(self,DATA):
    n = len(DATA)
    for i in range(n):
      try:
        DATA[i] = plot3d(self.fnd(DATA[i][0]),(x,DATA[i][1],DATA[i][2]),(y,DATA[i][1],DATA[i][2]), show=False, surface_color=i/r())
        if DATA[i] is None:
          return None
      except:
        return self.ERROR(6)
    print("Plotting...")
    p = DATA[0]
    for i in range(1,n):
      p.extend(DATA[i])

    p.show()
    return p

  def stor(self, filename):
    data = {}
    funcs = {}
    equas = {}
    for i in self.Funcs:
      funcs.update({i: str(self.Funcs[i])})
    for i in self.Equas:
      equas.update({i: str(self.Equas[i])})
    data.update({"F": funcs})
    data.update({"E": equas})
    with open (f"./{filename}","w") as file:
      json.dump(data, file)
    return 1

  def load(self, filename):
    with open (f"./{filename}","r") as file:
      data = json.load(file)
      for i in data["F"]:
        self.Funcs.update({i: sympify(data["F"][i])})
      for i in data["E"]:
        self.Equas.update({i: sympify(data["E"][i])})
    return 1

  def ERROR(self,code, name=""):
    if code == 0:
      print(f"DataBaseError: The function '{name}' is not defined yet. Try 'save {name}: [Expression]'")
      return None
    elif code == 1:
      print(f"DataBaseError: The equation '{name}' is not defined yet. Try 'save {name}: [Expression]'")
      return None
    elif code == 2:
      print(f"DataBaseError: The variable '{name}' is undefined. Only x, y and z can be used.")
      return None
    elif code == 3:
      print(f"DataBaseError: The expression is not interpretable. You may need to check for typos.")
      return None
    elif code == 4:
      print(f"DataBaseError: The name '{name}' is not assigned to anything yet. Try 'save {name}: [Expression]'")
      return None
    elif code == 5:
      print(f"DataBaseError: The name '{name}' is aleady in use. Try a different name for your expression.")
      return None
    elif code == 6:
      print(f"DataBaseError: The plot operation can only perform on functions.")
      return None


DB = DataBase()