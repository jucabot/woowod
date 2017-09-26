import argparse
import sys,csv
import json

from wodai import Box,Wod

def main():
	
	parser = argparse.ArgumentParser(description='World of WOD CLI')
	parser.add_argument('box', help='Box config file name')
	parser.add_argument('--protocols', default="protocols.json", help='Training protocols file name (default protocols.json)')

	args = parser.parse_args()
	print args

	#Set args
	box_filepath = args.box
	print "Welcome to WOD.AI CLI for %s" % (box_filepath)

	#load protocols definition
	protocols_filepath = args.protocols
	protocols =	json.load(open(protocols_filepath,mode='r'))

	#load box configuration
	f_box = open(box_filepath,mode='r')
	box_conf = Box.DEFAULT_CONFIG

	for row in csv.DictReader(f_box,delimiter=';'):
		box_conf[Box.MOVES].append(row)
	f_box.close()

	#Create a sequence of workouts
	box	= Box(box_conf,protocols)
	print "Available moves : "
	for move in box.get_available_moves():
		print move["Task"]
	print
	print "Available training schemes : "
	for scheme in box.get_available_schemes():
		print scheme

	print "Wods :"

	wod = box.create_workout('Cardio')
	print wod

	wod = box.create_workout('Cardio+Gym')
	print wod

	wod = box.create_workout('Cardio+Weight')
	print wod

	wod = box.create_workout('Gym+Weight')
	print wod

	wod = box.create_workout('Cardio+Gym+Weight')
	print wod

	wod = box.create_workout('Gym')
	print wod

	wod = box.create_workout('Weight')
	print wod

	
if __name__ =="__main__":
	main()

