import pandas as pd
import numpy as np
import math
import re
import binascii

from dataRetriever import dataRetriever


def getMultiplier(section_hit_dart):
    if section_hit_dart == 'MISS':
        return 0
    elif section_hit_dart == 'DOUBLE':
        return 2
    elif section_hit_dart == 'UPPER SINGLE' or section_hit_dart == 'LOWER SINGLE' or section_hit_dart == 'SINGLE':
        return 1
    elif section_hit_dart == 'TRIPLE':
        return 3
    else:
        return 0


class statisticsMan:
    def __init__(self, data):
        pd.set_option('mode.chained_assignment', None)
        pd.set_option('display.max_columns', None)
        self.board_config = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        self.data = data

    def calculateAverageThrow(self, player, number, section):

        data_filtered = self.data.loc[self.data['player'] == player]
        if section:
            data_filtered = data_filtered.loc[self.data['aims_at_section'] == str(section)]
        if number:
            data_filtered = data_filtered.loc[self.data['aims_at_number'] == str(number)]

        if data_filtered.shape[0] == 0:
            print('No data available.')
            return 0, 0
        else:
            result = []
            for index in data_filtered.index:
                throw = getMultiplier(data_filtered['section_hit'][index]) * data_filtered['number_hit'][index]
                result.append(throw)

            data_filtered['average_throw'] = result

            average = data_filtered[['average_throw']].mean(axis=0)

            return round(average.values[0], 2), data_filtered.shape[0]

    def calculateStandardDeviation(self, player, number, section):

        std = 0
        data_filtered = self.data.loc[self.data['player'] == player]
        if section:
            data_filtered = data_filtered.loc[self.data['aims_at_section'] == str(section)]
        if number:
            data_filtered = data_filtered.loc[self.data['aims_at_number'] == str(number)]

        if data_filtered.shape[0] == 0:
            print('No data available.')
            return 0
        else:
            for index in data_filtered.index:
                std += data_filtered['distance_to_aimedsection'][index] ** 2

            std_normalised = math.sqrt(std / data_filtered.shape[0])
            return round(std_normalised, 2)

    def calculateCovarianceMatrix(self, player, number, section):
        if 'dummy' in player:
            std = float(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", player)[0])
            cov_matrix = [[std ** 2, 0],
                          [0, std ** 2]]

            # Create DataFrame
            return pd.DataFrame(cov_matrix, columns=['x', 'y'])
        else:
            # TODO : uitbreiden naar All numbers en All sections
            df = pd.DataFrame(columns=['x', 'y'])
            data_filtered = self.data.loc[self.data['player'] == str(player)]
            data_filtered = data_filtered.loc[data_filtered['aims_at_number'] == str(number)]
            if data_filtered.shape[0] == 0:
                data_filtered = self.data.loc[self.data['player'] == str(player)]
                data_filtered = data_filtered.loc[data_filtered['aims_at_number'] == '20']
                data_filtered = data_filtered.loc[data_filtered['aims_at_section'] == 'TRIPLE']
            else:
                data_filtered = data_filtered.loc[data_filtered['aims_at_section'] == str(section)]
                if data_filtered.shape[0] == 0:
                    # print('No data available. Using the data of the player on triple 20.')
                    data_filtered = self.data.loc[self.data['player'] == str(player)]
                    data_filtered = data_filtered.loc[data_filtered['aims_at_number'] == str(number)]

            # data_filtered = self.data.loc[self.data['player'] == str(player)]
            # data_filtered = data_filtered.loc[data_filtered['aims_at_number'] == '20']
            # data_filtered = data_filtered.loc[data_filtered['aims_at_section'] == 'TRIPLE']

            for index in data_filtered.index:
                coords = [data_filtered['x'][index], data_filtered['y'][index]]
                df.loc[len(df)] = coords
        return df.cov()

    def calculateCovarianceMatrix_new(self, player, number, section):
        # Dummy player that throws perfect normal in 2d. Put std in player name. Example : dummy10.2 has std = 10.2
        if 'dummy' in player:
            std = float(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", player)[0])
            cov_matrix = [[std ** 2, 0],
                          [0, std ** 2]]

            # Create DataFrame
            return pd.DataFrame(cov_matrix, columns=['x', 'y'])
        else:
            # TODO : uitbreiden naar All numbers en All sections
            df = pd.DataFrame(columns=['x', 'y'])
            data_filtered = self.data.loc[self.data['player'] == str(player)]

            # ALs de variable leeg wordt gegeven of het getal zit niet in de data, neem gemiddelde van alle data
            if not number or number not in data_filtered['aims_at_number'].values:
                for number in data_filtered['aims_at_number'].values:
                    data_filtered = data_filtered.loc[self.data['aims_at_number'] == str(number)]

                    if not section or section not in data_filtered['aims_at_section'].values:

                        for section in data_filtered['aims_at_section'].values:
                            data_filtered = data_filtered.loc[self.data['aims_at_section'] == str(section)]
                            for index in data_filtered.index:
                                coords = [data_filtered['x'][index], data_filtered['y'][index]]
                                df.loc[len(df)] = coords
                            cov = df.cov()

            return df.cov()

    def std_from_cov(self, cov):
        if cov.empty:
            print('No data available.')
            return 0, 0
        else:
            cov_xx = cov.iloc[0, 0]
            cov_yy = cov.iloc[1, 1]
            return round(math.sqrt(cov_xx), 2), round(math.sqrt(cov_yy), 2)

    def calculate_correlation(self, cov, std_x, std_y):
        return cov.iloc[0, 1] / (std_x * std_y)
