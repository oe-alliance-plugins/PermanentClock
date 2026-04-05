from Components.Converter.Converter import Converter
from Components.Element import cached
from time import localtime


class PermanentClockTime(Converter, object):
	SECHAND = 1
	MINHAND = 2
	HOURHAND = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "secHand":
			self.type = self.SECHAND
		elif type == "hourHand":
			self.type = self.HOURHAND
		else:
			self.type = self.MINHAND

	@cached
	def getValue(self):
		current_time = self.source.time
		if current_time is None:
			return 0

		t = localtime(current_time)
		if self.type == self.SECHAND:
			return t.tm_sec
		elif self.type == self.MINHAND:
			return t.tm_min
		elif self.type == self.HOURHAND:
			hour = t.tm_hour
			minute = t.tm_min
			if hour > 11:
				hour -= 12
			return (hour * 5) + (minute / 12.0)
		return 0

	value = property(getValue)
