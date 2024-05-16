from dataRetriever import dataRetriever
from statisticsMan import statisticsMan
from dartboardField import dartboardField
from Integrator import Integrator
from graphPlotter import graphPlotter
from videoGuy import videoGuy
import matplotlib.pyplot as plt
import numpy as np
import re

dartboard = dartboardField()

if __name__ == '__main__':
    player = 'dummy40'

    graphPlotter = graphPlotter()
    graphPlotter.make_heatmap(dartboard=dartboard, grid_size=10, player=player, processes=6)
    plt.show()


