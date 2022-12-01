import sys

project_home = "/home/morninbru/plotsar"
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from utils.plotter import Plotter

plot = Plotter()
plot.deploy()
application = plot.app.server
