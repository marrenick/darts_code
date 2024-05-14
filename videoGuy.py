import os

import numpy as np
from matplotlib import pyplot as plt

from moviepy.editor import ImageSequenceClip
from graphPlotter import graphPlotter


class videoGuy:
    def __init__(self, grapPlotter):
        self.graphPlotter = grapPlotter

    def make_heatmaps(self, dartbord, std_min, std_max, step_size, save_folder, grid_size, processes):
        counter = 1
        for std in np.arange(std_min, std_max, step_size):
            id_number = format(counter, f'0{5}d')
            counter+=1
            player = 'dummy' + str(std)
            print('Making the plot for standard deviation = {0}'.format(std))
            plot = self.graphPlotter.make_heatmap(dartboard=dartbord, grid_size=grid_size, player=player,
                                                  processes=processes)
            plt.savefig(f'{save_folder}/{id_number}_contour_plot_{std}.png')
            plt.close()

    def make_heatmap_video(self, image_folder, framerate, video_name):
        dir = [image_folder + '/' + s for s in os.listdir(image_folder)]
        clip = ImageSequenceClip(sorted(dir), fps=framerate)
        clip.write_videofile('videos/{0}.mp4'.format(video_name), fps=framerate)

