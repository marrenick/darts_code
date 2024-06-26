import numpy as np
from matplotlib import pyplot as plt

from dartboardField import dartboardField
from dataRetriever import dataRetriever
from statisticsMan import statisticsMan


class Bots:
    def __init__(self, player, difficulty):
        self.player = player
        self.dartboard = dartboardField()
        self.difficulty = difficulty
        # ./om te refereren naar zelfde folder als .py files
        datadude = dataRetriever('./connection.ini')

        data = datadude.database_read_data(schema='darts', table_name='dartsapp_map')
        self.statisticsman = statisticsMan(data)
        std = self.statisticsman.calculateStandardDeviation(self.player, 20, "TRIPLE") * difficulty
        print('Standard deviation of the bot : {0}.'.format(std))

    def throw(self, player, aimed_at_number, aimed_at_section):
        x_centre, y_centre = self.dartboard.get_coordinates_from_throw(aimed_at_number, aimed_at_section)
        cov = self.statisticsman.calculateCovarianceMatrix(player, aimed_at_number, aimed_at_section).mul(
            self.difficulty)
        if cov.empty:
            cov = self.statisticsman.calculateCovarianceMatrix(player, 20, 'TRIPLE').mul(
                self.difficulty)
        x, y = np.random.multivariate_normal([x_centre, y_centre], cov, 1).T
        throws = [self.dartboard.calculate_dart_score(x_throw, y_throw) for x_throw in x for y_throw in y]
        sections = [str(self.dartboard.calculate_dart_section(x_throw, y_throw))+str(self.dartboard.calculate_dart_number(x_throw, y_throw))
                    for x_throw in x for y_throw in y]
        return throws[0], sections[0], [x, y]


if __name__ == '__main__':
    player = input('Choose opponent:')
    difficulty = 0.45

    bot = Bots(player, difficulty)
    cova = bot.statisticsman.calculateCovarianceMatrix(player=player, number=20, section='TRIPLE').mul(difficulty)
    std_x, std_y = bot.statisticsman.std_from_cov(cova)
    print(std_x, std_y)
    while True:
        aimed_at_number = input('Aim at number: ')
        aimed_at_section = input('Aim at section: ')
        throw, section, coords = bot.throw(player, aimed_at_number, aimed_at_section)
        print(str(throw))
