
import math

from dataRetriever import dataRetriever

#ini file opnieuw
datadude = dataRetriever('C:/Users/MarnickClé/PycharmProjects/DartsAnalysis/connection.ini')
centerpoints = datadude.database_read_data(schema='darts', table_name='dartboard_centerpoints')

class dartboardField:
    def __init__(self):
        self.sector_boundaries = [9, 27, 45, 63, 81, 99, 117, 135, 153, 171, 189, 207, 225, 243, 261, 279, 297, 315, 333, 351]
        self.sector_scores = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]


    def calculate_dart_score(self,x, y):
        # Calculate the distance from the origin (0,0)
        distance = math.sqrt(x ** 2 + y ** 2)

        # Define the radii of different scoring regions
        bullseye_radius = 6.35  # Bullseye radius (inner bullseye)
        outer_bullseye_radius = 15.9  # Outer bullseye radius
        double_ring_radius = 170  # Radius of the outer edge of the triple ring

        # Check if the dart lands outside the dartboard
        if distance > double_ring_radius:
            section = 'MISS'
            return 0  # Score is zero if the dart lands outside the dartboard

        # Check if the dart lands in the bullseye
        if distance <= bullseye_radius:
            section = 'BULLSEYE'
            return 50  # Bullseye

        # Check if the dart lands in the outer bullseye
        if distance <= outer_bullseye_radius:
            section = 'BULL'
            return 25  # Outer bullseye

        # Calculate the angle of the dart from the positive x-axis
        angle = math.atan2(y, x)  # atan2 returns the angle in radians

        # Convert angle to degrees for easier comparison
        angle_degrees = math.degrees(angle)
        if angle_degrees < 0:
            angle_degrees += 360  # Ensure positive angle

        # Define the sector boundaries and corresponding scores
        sector_boundaries = [9, 27, 45, 63, 81, 99, 117, 135, 153, 171, 189, 207, 225, 243, 261, 279, 297, 315, 333, 351]
        sector_scores = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15,
                         10]  # Sector scores from 1 to 20

        # Find the sector the dart is in
        sector = None
        for i in range(len(sector_boundaries)):
            if angle_degrees < sector_boundaries[i]:
                sector = i
                break
        if sector is None:
            sector = 0  # Handle the case when the angle is greater than 351 degrees

        # Check if the dart lands in the double or triple ring
        if distance <= double_ring_radius:
            # Determine the score based on the sector and distance from the center
            score = sector_scores[sector]

            # Check if the dart lands in the double or triple ring
            if 162.6 <= distance <= 170:  # Double ring
                section = 'DOUBLE'
                return score * 2
            elif 99 <= distance <= 107:  # Triple ring
                section = 'TRIPLE'
                return score * 3
            else:
                section = 'SINGLE'
                return score  # Single ring


    def get_coordinates_from_throw(self,number,section):
        cp = centerpoints.loc[centerpoints['number'] == str(number)]
        cp = cp.loc[cp['section'] == str(section)]
        section = str(cp['section'].values[0])+str(cp['number'].values[0])
        return cp['_x'].values[0],cp['_y'].values[0],section