import json
import os
from configs import RESOURCES_FOLDER


def read_upgrades():
	with open(os.path.join(RESOURCES_FOLDER, 'upgrades_list.json'), 'r') as f:
		return json.load(f)


'''
x = [
	{
		'name': 'stronger sword 1',
		'building': 'barracks',
		'bonuses': {'DamageUpgrade': 10, 'SpeedUpgrade': -2},
		'image': 'stronger_sword_1.png',
		'cost': {'gold': 100, 'food': 0, 'wood': 0, 'stone': 0},
		'influenced_units': ['Swordsman']
	},
	{
		'name': 'faster boots',
		'building': 'barracks',
		'bonuses': {'SpeedUpgrade': 5},
		'image': 'faster_boots.png',
		'cost': {'gold': 0, 'food': 200, 'wood': 0, 'stone': 0},
		'influenced_units': ['Swordsman', 'Villager']
	}
]

with open('resources/upgrades_list1.json', 'w') as f:
	json.dump(x, f, indent=True)

'''