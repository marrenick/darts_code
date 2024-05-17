from dataRetriever import dataRetriever
from statisticsMan import statisticsMan
from dartboardField import dartboardField
from Integrator import Integrator
from graphPlotter import graphPlotter
from videoGuy import videoGuy
import matplotlib.pyplot as plt
import numpy as np
import re



if __name__ == '__main__':
    dartboard = dartboardField()
    datadude = dataRetriever('./connection.ini')
    data = datadude.database_read_data(schema='darts', table_name='dartsapp_map')
    statisticsman = statisticsMan(data)

    player = 'Marnick'
    cov = statisticsman.calculateCovarianceMatrix(player,number = '20',section='TRIPLE')
    std_x, std_y = statisticsman.std_from_cov(cov)
    print('Standard deviation from the covariance in the x-direction is {0}'.format(std_x))
    print('Standard deviation from the covariance in the Y-direction is {0}'.format(std_y))

    graphPlotter = graphPlotter()
    graphPlotter.make_heatmap(dartboard=dartboard, grid_size=20, player=player, processes=6)
    plt.show()


