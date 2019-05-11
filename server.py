from __future__ import print_function

import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""

	def __init__(self, *args, **kwargs):
		self.player_name = "NOT READY"
		Channel.__init__(self, *args, **kwargs)

	def Close(self):
		self._server.DelPlayer(self)

	##################################
	### Network specific callbacks ###
	##################################

	def Network_events(self, data):
		data["player_name"] = self.player_name
		print(data)
		self._server.SendToAll(data)

	def Network_player_name(self, data):
		self.player_name = data['player_name']
		self._server.SendPlayersOrder()


class ChatServer(Server):
	channelClass = ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print('Server launched')

	def Connected(self, channel, addr):
		self.AddPlayer(channel)

	def AddPlayer(self, player):
		print("New Player" + str(player.addr))
		self.players[player] = True
		self.SendPlayersOrder()
		print("players", [p for p in self.players])

	def DelPlayer(self, player):
		print("Deleting Player" + str(player.addr))
		del self.players[player]
		self.SendPlayersOrder()

	def SendPlayersOrder(self):
		self.SendToAll({"action": "players_order", "players_order": [p.player_name for p in self.players]})

	def SendToAll(self, data):
		for p in self.players:
			p.Send(data)

	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)



s = ChatServer(localaddr=('localhost',34252 ))
s.Launch()
