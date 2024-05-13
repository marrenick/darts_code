import math

import numpy as np
from matplotlib import pyplot as plt

from Integrator import Integrator
from dartboardField import dartboardField
from dataRetriever import dataRetriever
from statisticsMan import statisticsMan


class graphPlotter:
    def __init__(self):

        datadude = dataRetriever('./connection.ini')
        data = datadude.database_read_data(schema='darts', table_name='dartsapp_map')
        self.statisticsman = statisticsMan(data)

    def make_heatmap(self, dartboard, grid_size, player):
        double_bull_radius = 6.35
        single_bull_radius = 15.9
        inner_triple_radius = 99
        outer_triple_radius = 107
        inner_double_radius = 162
        outer_double_radius = 170
        #
        x = np.arange(-200, 200, grid_size)
        y = np.arange(-200, 200, grid_size)
        expected_values = np.zeros((len(x), len(y)))
        cov_dict = {}

        for section in ['SINGLE', 'DOUBLE', 'TRIPLE', 'MISS']:
            for number in dartboard.sector_scores + [0, 25]:
                cov_dict[section + str(number)] = self.statisticsman.calculateCovarianceMatrix(player, number, section)

        for i in range(len(x)):
            x_0 = x[i]
            print('Starting row with coordinates ' + str(x_0))
            for j in range(len(y)):
                y_0 = y[j]
                number = dartboard.calculate_dart_number(x_0, y_0)
                section = dartboard.calculate_dart_section(x_0, y_0)

                cov = cov_dict.get(section + str(number))
                std_x, std_y = self.statisticsman.std_from_cov(cov)

                rho = self.statisticsman.calculate_correlation(cov, std_x, std_y)

                integrator = Integrator(x_0, y_0, std_x, std_y, rho, dartboard)
                EV = integrator.integrate()

                expected_values[i, j] = EV

        max_index = np.unravel_index(np.argmax(expected_values), expected_values.shape)
        X, Y = np.meshgrid(x, y)
        max_x = X[max_index]
        max_y = Y[max_index]


        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))



        print('Maximum expected value is {0} on number {1} and section {2}.'.format(
            expected_values[max_index],
            dartboard.calculate_dart_number(max_y, max_x),
            dartboard.calculate_dart_section(max_y, max_x)))
        heatmap = ax1.pcolormesh(Y, X, expected_values, cmap='RdYlBu_r', shading='auto')
        fig.colorbar(heatmap, ax=ax1, label='Expected Value')
        ax1.set_xlim(-200, 200)
        ax1.set_ylim(-200, 200)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_aspect('equal')
        ax1.set_title('Heatmap expected value')

        # Plot the dartboard in the second subplot
        theta = np.linspace(0, 2 * np.pi, 100)
        ax2.plot(double_bull_radius * np.cos(theta), double_bull_radius * np.sin(theta), 'k-', lw=1)  # Double bull
        ax2.plot(single_bull_radius * np.cos(theta), single_bull_radius * np.sin(theta), 'k-', lw=1)  # Single bull
        ax2.plot(inner_triple_radius * np.cos(theta), inner_triple_radius * np.sin(theta), 'k-', lw=1)  # Inner triple
        ax2.plot(outer_triple_radius * np.cos(theta), outer_triple_radius * np.sin(theta), 'k-', lw=1)  # Outer triple
        ax2.plot(inner_double_radius * np.cos(theta), inner_double_radius * np.sin(theta), 'k-', lw=1)  # Inner double
        ax2.plot(outer_double_radius * np.cos(theta), outer_double_radius * np.sin(theta), 'k-', lw=1)  # Outer double
        ax2.plot(max_y, max_x, 'ko', markersize=3)
        ax2.set_aspect('equal')
        ax2.set_xlim(-200, 200)
        ax2.set_ylim(-200, 200)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('Dartboard')
        # Plot radial outward lines from outer bull wire to outer double wire
        for boundary in dartboard.sector_boundaries:
            boundary = math.radians(boundary)
            ax2.plot([single_bull_radius * np.cos(boundary), outer_double_radius * np.cos(boundary)],
                     [single_bull_radius * np.sin(boundary), outer_double_radius * np.sin(boundary)], 'k-', lw=1)

        # Add number labels to the dartboard
        for number, boundary in zip(dartboard.sector_scores, dartboard.sector_boundaries):
            boundary = math.radians(boundary)
            x_text = (outer_double_radius - 30) * np.cos(boundary)
            y_text = (outer_double_radius - 30) * np.sin(boundary)
            ax2.text(x_text, y_text, str(number), fontsize=12, ha='center', va='center')

        plt.tight_layout()
        plt.show()