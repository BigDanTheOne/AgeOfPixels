from typing import Dict, List
from PodSixNet.Connection import connection, ConnectionListener
from _thread import *
from copy import deepcopy
from collections import defaultdict


class NetworkClient(ConnectionListener):
	_events = defaultdict(lambda: [])
	_players_order = []

	def __init__(self, host, port, player_name):
		self.Connect((host, port))
		self.player_name = player_name
		connection.Send({"action": "player_name", "player_name": player_name})
		#t = start_new_thread(self.InputLoop, ())

	def get_events(self, player_name):
		player_events = deepcopy(self._events[player_name])
		del self._events[player_name]
		return player_events

	def get_players_order(self):
		return self._players_order

	def Update(self):
		connection.Pump()
		self.Pump()

	def SendEvents(self, events):
		connection.Send({"action": "events", "events": events})

	#######################################
	### Network event/message callbacks ###
	#######################################

	def Network_players_order(self, data):
		self._players_order = data['players_order']

	def Network_events(self, data):
		print('hey')
		print(data)
		self._events[data['player_name']].append(data['events'][0])

	# built in stuff

	def Network_connected(self, data):
		print("You are now connected to the server")

	def Network_error(self, data):
		print('error:', data['error'][1])
		connection.Close()

	def Network_disconnected(self, data):
		print('Server disconnected')
		exit()
