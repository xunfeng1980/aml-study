from ipd import *
from strategies import *

bag=[Periodic("D"), HardMajority(), Tft(), Spiteful(),  Gradual()]
t= Tournament(g,bag)        # default: length=1000
e= Ecological(t)            # default: pop=100
e.run()
print(e.tournament.matrix)
print(e.historic)
e.drawPlot()
e.drawCooperation()
