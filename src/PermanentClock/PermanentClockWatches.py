import math

from Components.Renderer.Renderer import Renderer
from enigma import eCanvas, eRect, eSize, gRGB
from skin import parseColor


class PermanentClockWatches(Renderer):
	GUI_WIDGET = eCanvas

	def __init__(self):
		Renderer.__init__(self)
		self.fColor = gRGB(255, 255, 255, 0)
		self.bColor = gRGB(0, 0, 0, 255)
		self.numval = -1

	def applySkin(self, desktop, parent):
		attribs = []
		for attrib, what in self.skinAttributes:
			if attrib == 'foregroundColor':
				self.fColor = parseColor(what)
			elif attrib == 'backgroundColor':
				self.bColor = parseColor(what)
			else:
				attribs.append((attrib, what))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	def calculate(self, watch_value, radius, middle):
		angle = watch_value * 6
		radians = math.pi / 180
		x = int(round(radius * math.sin(angle * radians)))
		y = int(round(radius * math.cos(angle * radians)))
		return (middle + x, middle - y)

	def hand(self):
		width = self.instance.size().width()
		height = self.instance.size().height()
		radius = min(width, height) // 2
		end_x, end_y = self.calculate(self.numval, radius, radius)
		self.draw_line(radius, radius, end_x, end_y)

	def draw_line(self, x0, y0, x1, y1):
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		if y0 < y1:
			ystep = 1
		else:
			ystep = -1
		deltax = x1 - x0
		deltay = abs(y1 - y0)
		error = -(deltax // 2)
		y = y0
		for x in range(x0, x1 + 1):
			if steep:
				self.instance.fillRect(eRect(y, x, 1, 1), self.fColor)
			else:
				self.instance.fillRect(eRect(x, y, 1, 1), self.fColor)
			error += deltay
			if error > 0:
				y += ystep
				error -= deltax

	def changed(self, what):
		current_value = self.source.value
		if what[0] != self.CHANGED_CLEAR and self.instance and self.numval != current_value:
			self.numval = current_value
			self.instance.clear(self.bColor)
			self.hand()

	def postWidgetCreate(self, instance):
		def parseSize(value):
			x_value, y_value = value.split(',')
			return eSize(int(x_value), int(y_value))

		for attrib, value in self.skinAttributes:
			if attrib == 'size':
				self.instance.setSize(parseSize(value))
		self.instance.clear(self.bColor)
