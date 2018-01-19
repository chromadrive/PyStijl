from utils import Utils
import random

utils = Utils()

def generate_lines():
	# Add utils.num_lines number of horiz/vert lines
	for line in range(utils.num_lines):
		orientation = utils.fetch_orientation()
		perpendicular = ('HOR' if orientation == 'VER' else 'VER')
		# Generate a line that's not too close to another parallel one
		while True:
			pos = random.random()
			if not utils.is_too_close(pos, utils.lines[orientation], orientation):
				break
		# Generate endpoints from an existing line
		endpoints = utils.select_endpoints(pos, utils.lines[perpendicular])
		utils.lines[orientation].append((pos, endpoints))

	utils.lines['HOR'].sort()
	utils.lines['VER'].sort()


def fetch_boxes():
	boxes = []
	for i, (y, (x1, x2)) in enumerate(utils.lines['HOR'][:-1]):
		box_y1 = y
		# Find vertical lines that intersect this horizontal line
		for j, (x, (y1, y2)) in enumerate(utils.lines['VER'][:-1]):
			if x > x2:
				break
			if x < x1 or y1 > y or y2 <= y:
				# Intersection must have its upper end beyond y
				continue
			box_x1=x
			# Find the right side of the box
			for (right_x1, (right_y1, right_y2)) in utils.lines['VER'][j+1:]:
				if right_y1 <= y < right_y2:
					break
			box_x2 = right_x1

			# Find the top side of the box
			for (upper_y, (upper_x1, upper_x2)) in utils.lines['HOR'][i+1:]:
				if upper_x1 <= box_x1 and upper_x2 >= box_x2:
					box_y2 = upper_y
					break
			utils.boxes.append((box_x1, box_y1, box_x2, box_y2))

def paint():
	# Paint our picture!
	generate_lines()
	fetch_boxes()

def generate_svg(file_name='image.svg'):
	svg = ['<?xml version="1.0" encoding="utf-8"?>',
		   '<svg xmlns="http://www.w3.org/2000/svg"',
		   ' xmlns:xlink="http://www.w3.org/1999/xlink" width="{}"'
		   ' height="{}" >'.format(utils.width, utils.height),
		   '<defs>',
		   '	<style type="text/css"><![CDATA[',
		   '		line {',
		   '		stroke: #000;',
		   '		stroke-width: 5px;',
		   '		}',
		   '	]]></style>'
		   '</defs>']

	# Write boxes
	for box in utils.boxes:
		x1, x2 = box[0]*utils.width, box[2]*utils.width
		y1, y2 = box[1]*utils.height, box[3]*utils.height

		box_width, box_height = x2 - x1, y2 - y1
		colour = utils.fetch_color()
		svg.append('<rect x="{}" y="{}" width="{}" height="{}"'
				   ' style="fill: {}"/>'.format(x1, y1, box_width, box_height, colour))
	# Write lines (over boxes)
	for orientation in ['HOR', 'VER']:
		for line in utils.lines[orientation][1:-1]:
			y1 = line[0]
			y2 = line[0]
			x1, x2 = line[1]
			if orientation == 'VER':
				x1,x2, y1,y2 = y1,y2, x1,x2
			x1 = x1 * utils.width
			x2 = x2 * utils.width
			y1 = y1 * utils.height
			y2 = y2 * utils.height
			svg.append('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2))

	# End of file
	svg.append('</svg>')
	svg = '\n'.join(svg)
	with open(file_name, 'w') as file:
		file.write(svg)

def main():
	paint()
	generate_svg()

main()
