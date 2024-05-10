import numpy as np
from scipy.integrate import dblquad
from dartboardField import dartboardField



class integrator:
    def __init__(self,x0,y0,sigma_x,sigma_y,rho):
        self.x0 = x0
        self.y0 = y0
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        self.rho = rho
        self.dartboard = dartboardField()
    # TODO : heatmap maken voor elk grid point expected value berekenen voor standaard deviatie
    def pdf_2d_normal(self, x, y, x0, y0, sigma_x, sigma_y, rho):
        z = ((x - x0) ** 2 / sigma_x ** 2 - 2 * rho * (x - x0) * (y - y0) / (sigma_x * sigma_y) + (
                y - y0) ** 2 / sigma_y ** 2) / (2 * (1 - rho ** 2))
        return np.exp(-z) / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho ** 2))

    def integrand(self, x, y):
        return self.pdf_2d_normal(x, y, self.x0, self.y0, self.sigma_x, self.sigma_y, self.rho) * self.dartboard.calculate_dart_score(x,y)

    def integrate(self):
        expected_value, _ = dblquad(self.integrand, -200, 200, lambda x: -200, lambda x: 200, epsabs=1e-4, epsrel=1e-4)
        print(expected_value)
        return expected_value




