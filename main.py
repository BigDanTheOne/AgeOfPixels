import pygame.locals
from world import *
from selection_rect import *
import sys
from menu import Menu
import platform
from player import HumanPlayer
from network_client import NetworkClient

if platform.system() in ['Windows']:
	import ctypes
	from ctypes import windll


def rect_to_list(r: Rect):
	return [r.x, r.y, r.w, r.h]


def process_events(world: World, player: HumanPlayer, selection_rect: SelectionRect, menu: Menu):
	events = []
	for event in pygame.event.get():
		if event.type == pygame.locals.QUIT or \
				(event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
			return False, None
		elif event.type == pygame.locals.KEYDOWN:
			if event.key == pygame.locals.K_DELETE:
				events.append({'name': 'delete_button', 'params': []})
			# player.delete_button()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Left mouse button
				selection_rect.start_selection(event.pos)
				events.append({'name': 'left_click', 'params': [event.pos]})
			# player.left_click(event.pos)
			elif event.button == 3:  # Right mouse button
				events.append({'name': 'right_click', 'params': [event.pos]})
			# player.right_click(event.pos)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				selection_rect.finish_selection()
				# players[0].selection_rect_finished(selection_rect.get_rect())
				events.append({'name': 'selection_rect_finished', 'params': [rect_to_list(selection_rect.get_rect())]})
		elif event.type == pygame.MOUSEMOTION:
			selection_rect.drag_selection(event.pos)

	return True, events


def create_network_client():
	host = '192.168.0.102' #input("Enter server IP: ")
	port = '34252' #input("Enter server port: ")
	player_name = 'fefefe1' #input("Enter your nickname: ")
	return NetworkClient(host, int(port), player_name)


def main():
	global SCREEN_RECT

	network_client = create_network_client()
	if network_client is None:
		return False

	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, -1)
	pygame.init()

	info_object = pygame.display.Info()
	SCREEN_RECT = Rect(0, 0, info_object.current_w, info_object.current_h)

	if platform.system() in ['Windows']:
		# Fix bug with text scaling in Windows
		ctypes.windll.user32.SetProcessDPIAware()
		true_res = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
	elif platform.system() in ['Linux', 'Darwin']:
		true_res = (SCREEN_RECT.w, SCREEN_RECT.h)
	else:
		true_res = (1920, 1080)

	screen: pygame.Surface = pygame.display.set_mode(true_res)
	pygame.display.set_caption("AgeOfPixels")

	# Create background
	grass = pygame.image.load(os.path.join(IMAGES_FOLDER, 'sand.jpg')).convert()

	clock = pygame.time.Clock()
	world = World(screen)
	menu = Menu(screen, world, SCREEN_RECT)
	selection_rect = SelectionRect()

	players = [HumanPlayer(world, network_client.player_name)]
	players_order_buffer = [network_client.player_name]
	players[0].act()
	players[0].create_army(1)
	# players[1].create_army(1)

	while True:
		elapsed_time = clock.tick_busy_loop() / 1000

		rc, events = process_events(world, players[0], selection_rect, menu)
		if not rc:
			return

		if len(events) > 0:
			network_client.SendEvents(events)
		network_client.Update()
		players_order = network_client.get_players_order()
		if players_order != players_order_buffer:
			for player in players_order:
				if player not in players_order_buffer:
					players.append(HumanPlayer(world, player))

		for player in players:
			if player == players[0]:
				player.push_events(events)
			else:
				player.push_events(network_client.get_events(player.name))

		for player in players:
			player.process_events()

		world.step(elapsed_time)
		world.render()
		menu.render()

		if selection_rect.is_selection_active():
			selection_rect.render(screen)

		menu.render_fps(int(clock.get_fps()))

		pygame.display.flip()
		pygame.time.delay(1)
		screen.fill(1)
		screen.blit(grass, (0, 0))


if __name__ == "__main__":
	sys.exit(main())
