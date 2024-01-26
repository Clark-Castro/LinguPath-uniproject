import os
import Help
from DataBase import DB

def Query():
  #initial input style
  print("-"*50)
  print("LinguPath > ",end="")

  #query parser
  UserInput = ""
  try:
    UserInput = input().strip()
  except:
    print()
    pass
  QType = UserInput[:4]
  Q = UserInput[4:].strip()

  #special queries
  if QType == "exit":
    print("-"*50+"\nExitting...")
    exit()
  elif QType == "clrp":
    os.system("clear")
    return Query()
  elif QType == "help":
    print(Help.Help)
  elif QType == "":
    return Query()
  
  #save query
  elif QType == "save":
    #parameter construction
    name, expr = Q.split(":", maxsplit = 1)
    name = name.strip().split(" ")[0]
    expr = expr.strip()
    TYPE = "=" in expr

    #DB access
    res = DB.add(name, expr, TYPE)
    if res:
      print("DataBase: "+"function"*(not TYPE)+"equation"*(TYPE)+f" saved as '{name}'")
    return res
  
  #show query
  elif QType == "show":
    #DB access
    return DB.fnd(Q)

  #eval query
  elif QType == "eval":
    #name parameter construction
    fname, fpont = Q.split(":", maxsplit = 1)
    fname = fname.strip()

    #points parameter construction
    fpont = fpont.strip().split(",")
    for i in range(len(fpont)):
       fpont[i] = fpont[i].split(":", maxsplit=1)
       fpont[i][0] = fpont[i][0].strip()
       fpont[i][1] = fpont[i][1].strip()
    
    #DB access
    return DB.evl(fname, fpont)
  
  #solv query
  elif QType == "solv":
    #parameter construction
    EQS = []
    EQNUM,VARS = Q.split(",",maxsplit=1)
    EQNUM = int(EQNUM)
    VARS = VARS.split(",")
    for i in range(len(VARS)):
      VARS[i] = VARS[i].strip()

    #user input & DB access for listing equations
    for i in range(EQNUM):
      inp = input(f"Eq #{i}: ")
      if "=" in inp:
        inp = inp.split("=",maxsplit=1)
        inp[0] = inp[0].strip()
        inp[1] = inp[1].strip()
        medeq = DB.makequa(inp)
      else:
        inp = inp.strip()
        medeq = DB.fnd(inp)
      EQS.append(medeq)
    
    #DB access for solving the equation list
    print("\nSolving...\n")
    res = DB.slv(EQS,VARS)
    return res

  #plot query
  elif QType == "plot":
    #user input & listing the functions for plotting
    DATA = []
    PLNUM = int(Q)
    for i in range(PLNUM):
      inp = input(f"Function #{i}: ")
      inp = inp.split(",")
      while len(inp)<3:
        inp.append(str(10*((-1)**len(inp))))
      for i in range(3):
        inp[i] = inp[i].strip()
      DATA.append(inp)

    #DB access to plot the list
    res = DB.plt(DATA)
    print()
    return res
  
  elif QType == "STOR":
    stor = DB.stor(Q)
    print(f"DataBase: The current database is stored into the following file '{Q}'")
    return stor

  elif QType == "LOAD":
    save = DB.load(Q)
    print(f"DataBase: The following file is loaded into the database '{Q}'")
    return save

  else:
    print("QueryError: Invalid query. Try 'help' to learn how the query model works.")
    return Query()