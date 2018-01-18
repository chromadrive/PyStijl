from utils import Utils

utils = Utils()

def generate_lines
	# Add utils.num_lines number of horiz/vert lines
	for line in range(utils.num_lines):
		orientation = utils.fetch_orientation()
		perpendicular = ('HOR' if orientation == 'VER' else 'VER')
		# Generate a line that's not too close to another parallel one
		while True:
			pos = random.random()
			if not self.too_close(pos, utils.lines[orientation], orientation):
				break
		# Generate endpoints from an existing line
		endpoints = self.select_endpoints(pos, utils.lines[perpendicular])
		utils.lines[orientation].append((pos, endpoints))

	self.lines['HOR'].sort()
	self.lines['VER'].sort()


