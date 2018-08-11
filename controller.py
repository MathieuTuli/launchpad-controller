import launchpad_py as launchpad
import random
import numpy as np
import sys

from pygame import time


class Controller():
	def __init__(self, settings):
		"""
		:param settings = dict
			{
			"id" : "pro/mk2/control xl/launchkey/dicer/mk1 or mini or S",
			"assignments":dict, buttons and their assignment
			}
		"""
		keys = ['id', 'assignments']
		for key in keys:
			if key not in settings:
				print("Incorrect controller settings. Assure {} keys are present.".format(keys))
				sys.exit(0)

		self.lp = launchpad.Launchpad()
		self.mode = None
		self.board = np.zeros((9,9))
		self.colours = {
			"red_dim":{'r':1,'g':0},
			"red_bright":{'r':1,'g':0},
			"green_dim":{'r':0,'g':1},
			"green_bright":{'r':0,'g':3},
			"orange_dim":{'r':1,'g':1},
			"orange_bright":{'r':3,'g':3},
		}
		self.assignments = {}
		self.assignment_functions = {}
		for key, value in settings['assignments'].items():
			if len(value) != 4:
				print("Incorrect assignment values.")
				sys.exit(0)
			else:
				self.addAssignment(key, [value[0], value[1]], value[2], value[3])

		# check what we have here and override lp if necessary
		id = settings['id']
		if id != 'mk1' and id != "S" and id != "mini":
			if id == 'pro':
				if self.lp.Check( 0, "pro" ):
					self.lp = launchpad.LaunchpadPro()
					if self.lp.Open(0,"pro"):
						print("Launchpad Pro")
						self.mode = "Pro"
			elif id == 'mk2':
				if self.lp.Check( 0, "mk2" ):
					self.lp = launchpad.LaunchpadMk2()
					if self.lp.Open( 0, "mk2" ):
						print("Launchpad Mk2")
						self.mode = "Mk2"
			elif id == 'control xl':
				if self.lp.Check( 0, "control xl" ):
					self.lp = launchpad.LaunchControlXL()
					if self.lp.Open( 0, "control xl" ):
						print("Launch Control XL")
						self.mode = "XL"
			elif id == 'launchkey':
				if self.lp.Check( 0, "launchkey" ):
					self.lp = launchpad.LaunchKeyMini()
					if self.lp.Open( 0, "launchkey" ):
						print("LaunchKey (Mini)")
						self.mode = "LKM"
			elif id == 'dicer':
				if self.lp.Check( 0, "dicer" ):
					self.lp = launchpad.Dicer()
					if self.lp.Open( 0, "dicer" ):
						print("Dicer")
						self.mode = "Dcr"
		else:
			if self.lp.Open():
				print("Launchpad Mk1/S/Mini")
				self.mode = "Mk1"

		if self.mode is None:
			print("Could not intialize controller. Assure proper ID is being used and that the controller is properly plugged in.")
			sys.exit(0)
		self.lp.Reset()

	def __del__(self):
		print("Controller dead.\n")

	def allOn(self, colour):
		for key, value in self.assignments.items():
			self.turnOn(value[0], value[1], "green_bright")
		# for i in range(9):
		# 	for j in range(9):
		# 		if(i == 8 and j == 0):
		# 			continue
		# 		self.turnOn(i,j,colour)

	def allOff(self):
		for key, value in self.assignments.items():
			self.turnOff(value[0], value[1])
		# for i in range(9):
		# 	for j in range(9):
		# 		if(i == 8 and j == 0):
		# 			continue
		# 		self.turnOff(i,j)

	def turnOn(self, x, y, colour):
		if self.validateButton([x,y]):
			clr = self.colours[colour]
			self.lp.LedCtrlXY(x, y, clr['r'], clr['g'])
			self.board[x,y] = 1
		else:
			print("Incorrect button coordinates; ({}, {})\n".format(x, y))

	def turnOff(self, x, y):
		if self.validateButton([x,y]):
			self.lp.LedCtrlXY(x, y, 3, 0)
			self.board[x,y] = 0
		else:
			print("Incorrect button coordinates; ({}, {})\n".format(x, y))

	def validateButton(self, button):
		if button == [8, 0]:
			return False
		elif button[0] < 0 or button[0] > 8 or button[1] < 0 or button[1] > 8:
			return False
		return True

	def buttonState(self):
		"""
		returns list [x, y, true/false, 1/0]
		will return a list for true on press down, and one for false on release
		"""
		state = self.lp.ButtonStateXY()
		if state:
			state.append(self.board[state[0], state[1]])
			params = {
				'x':state[0],
				'y':state[1],
				'pressed_down':state[2],
				'on':state[3]
			}
			return params
		return state

	def buttonEvent(self):
		params = self.buttonState()
		if params:
			if params['pressed_down']:
				key = self.findAssignment([params['x'], params['y']])
				if key == None:
					print("Button [{},{}] has no assignment.".format(params['x'], params['y']))
				else:
					if params['on']:
						if key+'_off' in self.assignment_functions:
							self.assignment_functions[key+'_off']()
						else:
							print('Button [{},{}] function not found.'.format(params['x'], params['y']))
					else:
						if key+'_on' in self.assignment_functions:
							self.assignment_functions[key+'_on']()
						else:
							print('Button [{},{}] function not found.'.format(params['x'], params['y']))

	def findAssignment(self, find):
		for key, value in self.assignments.items():
			if find == value:
				return key
		return None

	def addAssignment(self, key, value, on_fcn, off_fcn):
		old_key = self.findAssignment(value)
		if old_key == None and key not in self.assignments:
				self.assignments.update({key:value})
				self.assignment_functions.update({key+'_on':on_fcn})
				self.assignment_functions.update({key+'_off':off_fcn})
				self.turnOff(value[0], value[1])
				print("[{} : {}] added to assignments".format(key,value))
		else:
			print('Button or Key already assigned. Use \'updateAssignment(...)\' if you wish to change any part of the assignment.')
			print("[{} : {}] not added to assignments".format(key,value))

			# if key+'_on' not in self.assignment_functions and key+'_off' not in self.assignment_functions:
			# 	self.assignment_functions.update({key+'_on':on_fcn})
			# 	self.assignment_functions.update({key+'_off':off_fcn})

	def removeAssignment(self, key):
		if key in self.assignments:
			del self.assignments[key]
			del self.assignment_functions[key]
		else:
			print("Can't remove assignment, key doesn't exist.")

	def printAssignments(self):
		for key, value in self.assignments.items():
			print('Button {} assigned: {}'.format(value, key))

	def cleanup(self):
		self.mode == "cleaned"
		self.lp.Reset()
		self.lp.Close()
