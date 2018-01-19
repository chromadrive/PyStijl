import random
import numpy as np

# Colors and cumulative probability (CDF)
colors = ['blue', 'red', 'yellow', 'white']
colors_cdf = [0.2, 0.4, 0.6, 1]

class Utils:
	def __init__(self, width=600, height=400, padding=40, num_lines=10, seed=None):
		# Seed our RNG
		random.seed(seed)

		# Set variables up
		self.width, self.height = width, height
		self.padding, self.num_lines = padding, num_lines
		self.tolerance = {'HOR': self.padding / self.width,
						  'VER': self.padding / self.height}

		# Initialize canvas with border edges
		self.lines = {'HOR': [(0, (0,1)), (1, (0,1))],
					  'VER': [(0, (0,1)), (1, (0,1))]}
		# Initialize a list to keep track of all boxes we make
		self.boxes = []


		# And an orientations list to keep track of how we've placed lines thus far
		self.orientations = []

	def fetch_color(self):
		# Randomly generate a color based on the probabilities given above
		r = random.random()
		bins = [0] + colors_cdf
		for i in range(len(bins)):
			if bins[i] <= r <= bins[i+1]:
				return colors[i]

	def is_too_close(self, pos, parallel, orientation):
		# Returns whether the partition is too close to a parallel line
		too_close = [abs(pos - line[0]) < self.tolerance[orientation] for line in parallel]
		return any(too_close)

	def select_endpoints(self, pos, perpendicular):
		# Randomly select two points on perpendicular lines to start/end our lines
		intersect = [line for line in perpendicular if line[1][0] < pos < line[1][1] ]
		endpoints = sorted(random.sample([line[0] for line in intersect], 2))
		return endpoints

	def fetch_orientation(self):
		# Randomly select an orientation (Horizontal or Vertical)
		if (len(self.orientations) > 1 and
				self.orientations[-1]==self.orientations[-2]): 
			orientation = ('VER' if self.orientations[-1] == 'HOR' else 'HOR')
		else:
			orientation = random.choice(('HOR', 'VER'))
		self.orientations.append(orientation)
		return orientation
		#return random.choice(('HOR', 'VER'))