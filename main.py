from dataRetriever import dataRetriever
from statisticsMan import statisticsMan
from dartboardField import dartboardField
from integrator import integrator
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

dartbord = dartboardField()

if __name__ == '__main__':
    player = 'Warre'
    number = 20
    section = 'TRIPLE'
    #aan te passen zodat connection file meteen goed staat
    datadude = dataRetriever('C:/Users/MarnickClé/PycharmProjects/DartsAnalysis/connection.ini')

    data = datadude.database_read_data(schema='darts', table_name='dartsapp_map')


    statisticsman = statisticsMan(data)
    average,total = statisticsman.calculateAverageThrow(player,number,section)
    std_sym = statisticsman.calculateStandardDeviation(player,number,section)
    cov = statisticsman.calculateCovarianceMatrix(player,number,section)

    std_x,std_y = statisticsman.std_from_cov(cov)


    print('Average throw: ' + str(average) + ' in {0} throws.'.format(total))
    print('Standard deviation {0}'.format(std_sym))
    print('Standard deviation from the covariance in the x-direction is {0}'.format(std_x))
    print('Standard deviation from the covariance in the Y-direction is {0}'.format(std_y))






    corr = statisticsman.calculate_correlation(cov, std_x, std_y)
    print(corr)
    integrator = integrator(x0=0,y0=0,sigma_x=std_x,sigma_y=std_y,rho=corr)
    #integrator.integrate()