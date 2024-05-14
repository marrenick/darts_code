from dataRetriever import dataRetriever
from statisticsMan import statisticsMan
from dartboardField import dartboardField
from Integrator import Integrator
from graphPlotter import graphPlotter
from videoGuy import videoGuy
import matplotlib.pyplot as plt
import numpy as np
import re

dartbord = dartboardField()

if __name__ == '__main__':
    player = 'dummy10.2'
    number = 25
    section = 'DOUBLE'
    # ./om te refereren naar zelfde folder als .py files
    datadude = dataRetriever('./connection.ini')

    data = datadude.database_read_data(schema='darts', table_name='dartsapp_map')

    statisticsman = statisticsMan(data)
    average, total = statisticsman.calculateAverageThrow(player, number, section)
    std_sym = statisticsman.calculateStandardDeviation(player, number, section)
    cov = statisticsman.calculateCovarianceMatrix(player, number, section)

    std_x, std_y = statisticsman.std_from_cov(cov)

    print('Average throw: ' + str(average) + ' in {0} throws.'.format(total))
    print('Standard deviation {0}'.format(std_sym))
    print('Standard deviation from the covariance in the x-direction is {0}'.format(std_x))
    print('Standard deviation from the covariance in the Y-direction is {0}'.format(std_y))
    graphPlotter = graphPlotter()
    #graphPlotter.make_heatmap(dartboard=dartbord, grid_size=10, player=player,processes=6)
    #plt.show()
    #videoguy = videoGuy(graphPlotter)
    #videoguy.make_heatmaps(dartbord, std_min = 1, std_max = 100, step_size=1, save_folder='plots/dummy_step1', grid_size=20, processes=6)
    #videoguy.make_heatmap_video('plots/dummy_step1',framerate=10,video_name='dummy_step1')

