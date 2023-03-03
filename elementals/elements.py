import random


class ElementTile:
    def __init__(self, element_type):
        self.element_type = element_type
        self.face_up = False

    def flip(self):
        self.face_up = not self.face_up

    def __str__(self):
        if self.face_up:
            return self.element_type
        else:
            return "X"  # this represents a face-down tile


class Wizard:
    def __init__(self, wizard_type):
        self.wizard_type = wizard_type
        self.collected = False

    def collect(self):
        self.collected = True

    def __str__(self):
        if self.collected:
            return self.wizard_type
        else:
            return " "  # this represents an uncollected wizard


class Player:
    def __init__(self, name):
        self.name = name
        self.collected_wizards = set()

    def flip_tiles(self, board):
        tile1, tile2 = random.sample(board.tiles, 2)
        tile1.flip()
        tile2.flip()
        print("Player", self.name, "flips over", tile1, "and", tile2)
        if tile1.element_type == tile2.element_type:
            self.collect_tiles(tile1, tile2, board)

    def collect_tiles(self, tile1, tile2, board):
        self.collected_wizards.add(tile1.element_type)
        tile1_collected = board.remove_tile(tile1)
        tile2_collected = board.remove_tile(tile2)
        if tile1_collected and tile2_collected:
            board.add_tiles()

    def has_won(self):
        return len(self.collected_wizards) >= 3

    def __str__(self):
        return self.name


class Board:
    def __init__(self, element_types, num_tiles=9):
        self.element_types = element_types
        self.tiles = []
        for i in range(num_tiles):
            element_type = random.choice(self.element_types)
            tile = ElementTile(element_type)
            self.tiles.append(tile)

    def remove_tile(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)
            return True
        else:
            return False

    def add_tiles(self):
        for i in range(2):
            element_type = random.choice(self.element_types)
            tile = ElementTile(element_type)
            self.tiles.append(tile)


class Game:
    def __init__(self, player_names, element_types):
        self.players = [Player(name) for name in player_names]
        self.board = Board(element_types)

    def start(self):
        print("Starting the game with", len(self.players), "players...")
        while not self.has_winner():
            for player in self.players:
                player.flip_tiles(self.board)
                if self.has_winner():
                    break
        self.end()

    def has_winner(self):
        for player in self.players:
            if player.has_won():
                print("Player", player.name, "has collected 3 wizards and wins!")
                return True
        return False

    def end(self):
        print("Game over!")
        print("Final scores:")
        for player in self.players:
            print(player.name, "-", len(player.collected_wizards), "wizards collected:",
                  ", ".join(player.collected_wizards))



game = Game(["Alice", "Bob", "Charlie", "Dave"], ["Fire", "Water", "Earth", "Air", "Lightning", "Darkness"])
game.start()