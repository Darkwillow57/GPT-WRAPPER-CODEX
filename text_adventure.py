#!/usr/bin/env python3
"""
Megan's Journey - A Zork-style Text Adventure Game
A compact fantasy adventure with mystery and magic
"""

import random
import re
from typing import Dict, List, Optional, Set

class Item:
    def __init__(self, name: str, description: str, takeable: bool = True, use_text: str = ""):
        self.name = name.lower()
        self.description = description
        self.takeable = takeable
        self.use_text = use_text
        self.used = False

class Character:
    def __init__(self, name: str, description: str, dialogue: Dict = None, takeable: bool = False):
        self.name = name.lower()
        self.description = description
        self.dialogue = dialogue or {}
        self.mood = "neutral"
        self.takeable = takeable

class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.items: Dict[str, Item] = {}
        self.characters: Dict[str, Character] = {}
        self.exits: Dict[str, str] = {}
        self.visited = False
        self.special_actions: Dict[str, str] = {}

class Game:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.current_room = "cabin"
        self.inventory: Dict[str, Item] = {}
        self.companions: Dict[str, Character] = {}
        self.game_state = {
            "amulet_power": 0,
            "bandits_defeated": False,
            "met_vee": False,
            "demon_awakened": False,
            "george_mood": "content",
            "shadowfang_fed": False,
            "tarot_readings": 0,
            "has_weapon": False,
            "has_potion": False,
            "has_companions": False
        }
        self.setup_world()

    def setup_world(self):
        """Initialize the game world with rooms, items, and characters"""
        
        # Create rooms
        self.create_rooms()
        self.create_items()
        self.create_characters()
        self.connect_rooms()

    def create_rooms(self):
        """Create all rooms in the game"""
        
        self.rooms["cabin"] = Room("Megan's Cabin", 
            "A cozy wooden cabin with a crackling fireplace. Your adventure begins here. "
            "There's a dusty bookshelf against one wall and a small table with some items.")
        
        self.rooms["forest"] = Room("Enchanted Forest",
            "A mystical forest with towering ancient trees. Shafts of golden light filter "
            "through the canopy. You hear strange whispers in the wind.")
        
        self.rooms["clearing"] = Room("Forest Clearing",
            "A peaceful circular clearing surrounded by wildflowers. In the center stands "
            "an ancient stone altar covered in mysterious runes.")
        
        self.rooms["cave"] = Room("Dark Cave",
            "A deep, shadowy cave that extends into the mountain. Strange crystals embedded "
            "in the walls emit a faint blue glow. The air feels thick with magic.")
        
        self.rooms["village"] = Room("Mystic Village",
            "A quaint village with thatched-roof cottages. Smoke rises from chimneys, and "
            "you can hear the bustle of daily life. A tavern sign creaks in the breeze.")
        
        self.rooms["tavern"] = Room("The Prancing Pony Tavern",
            "A warm, inviting tavern filled with the aroma of ale and roasted meat. "
            "Patrons chat quietly at wooden tables lit by flickering candles.")
        
        self.rooms["tower"] = Room("Wizard's Tower",
            "A tall stone tower that stretches toward the clouds. Ancient magical symbols "
            "are carved into every surface, pulsing with otherworldly energy.")
        
        self.rooms["dungeon"] = Room("Ancient Dungeon",
            "A forbidding underground chamber with stone walls slick with moisture. "
            "The air is cold and heavy with the weight of centuries.")

    def create_items(self):
        """Create all items and place them in rooms"""
        
        # Cabin items
        journal = Item("journal", "Megan's personal journal filled with cryptic notes about a mysterious quest.", True, 
                      "The journal reveals hints about a powerful amulet hidden in the ancient dungeon.")
        map_item = Item("map", "A hand-drawn map showing various locations around the mystical realm.", True,
                       "The map reveals secret paths and marks the location of the wizard's tower.")
        
        self.rooms["cabin"].items["journal"] = journal
        self.rooms["cabin"].items["map"] = map_item
        
        # Forest items  
        mushroom = Item("mushroom", "A glowing purple mushroom that pulses with magical energy.", True,
                       "Eating the mushroom fills you with magical energy, increasing your amulet power!")
        
        self.rooms["forest"].items["mushroom"] = mushroom
        
        # Cave items
        crystal = Item("crystal", "A brilliant blue crystal that hums with power.", True,
                      "The crystal's energy courses through you, enhancing your magical abilities.")
        
        self.rooms["cave"].items["crystal"] = crystal
        
        # Village items
        potion = Item("potion", "A healing potion in a small glass vial.", True,
                     "The potion restores your health and vitality.")
        
        self.rooms["village"].items["potion"] = potion
        
        # Tower items
        amulet = Item("amulet", "The legendary Amulet of Power, glowing with ancient magic.", True,
                     "The amulet radiates incredible power. You feel its magic flowing through you!")
        
        self.rooms["tower"].items["amulet"] = amulet
        
        # Dungeon items
        sword = Item("sword", "A gleaming enchanted sword with runes etched along the blade.", True,
                    "The sword feels perfectly balanced in your hand, ready for battle.")
        
        self.rooms["dungeon"].items["sword"] = sword

    def create_characters(self):
        """Create all characters and place them in rooms"""
        
        # Forest character
        fairy = Character("fairy", "A tiny, shimmering fairy with gossamer wings.",
                         {"talk": "The fairy whispers: 'Beware the shadows in the cave, brave Megan. "
                                 "The crystal there will aid you, but dark creatures guard it.'"})
        
        self.rooms["forest"].characters["fairy"] = fairy
        
        # Village characters
        merchant = Character("merchant", "A friendly trader with a cart full of mysterious goods.",
                           {"talk": "The merchant says: 'Welcome, traveler! I have potions and supplies. "
                                   "Have you heard of the wizard in the tower? He seeks brave souls.'"})
        
        blacksmith = Character("blacksmith", "A sturdy dwarf with soot-covered hands and a warm smile.",
                             {"talk": "The blacksmith grunts: 'That sword in the dungeon is legendary, lass. "
                                     "But ye'll need courage to claim it. Beware the guardian!'"})
        
        self.rooms["village"].characters["merchant"] = merchant
        self.rooms["village"].characters["blacksmith"] = blacksmith
        
        # Tavern character
        bard = Character("bard", "A cheerful musician with a lute, ready to share tales of adventure.",
                        {"talk": "The bard strums his lute: 'Ah, another adventurer! I've heard tales of "
                                "Megan's quest. The amulet you seek has the power to save our realm!'"})
        
        self.rooms["tavern"].characters["bard"] = bard
        
        # Tower character
        wizard = Character("wizard", "An ancient wizard with a long silver beard and twinkling eyes.",
                          {"talk": "The wizard speaks: 'Welcome, Megan. I have been expecting you. "
                                  "The amulet here is yours to take, but use its power wisely.'"})
        
        self.rooms["tower"].characters["wizard"] = wizard
        
        # Dungeon character (boss)
        guardian = Character("guardian", "A massive stone golem with glowing red eyes, guarding the ancient treasure.",
                           {"talk": "The guardian rumbles: 'WHO DARES DISTURB THE ANCIENT TREASURE? "
                                   "PROVE YOUR WORTH OR FACE MY WRATH!'"})
        
        self.rooms["dungeon"].characters["guardian"] = guardian

    def connect_rooms(self):
        """Set up exits between rooms"""
        
        # Cabin connections
        self.rooms["cabin"].exits = {"north": "forest", "south": "village"}
        
        # Forest connections  
        self.rooms["forest"].exits = {"south": "cabin", "east": "clearing", "west": "cave"}
        
        # Clearing connections
        self.rooms["clearing"].exits = {"west": "forest", "north": "tower"}
        
        # Cave connections
        self.rooms["cave"].exits = {"east": "forest", "down": "dungeon"}
        
        # Village connections
        self.rooms["village"].exits = {"north": "cabin", "east": "tavern"}
        
        # Tavern connections
        self.rooms["tavern"].exits = {"west": "village"}
        
        # Tower connections
        self.rooms["tower"].exits = {"south": "clearing"}
        
        # Dungeon connections
        self.rooms["dungeon"].exits = {"up": "cave"}

    def display_room(self):
        """Display current room information"""
        room = self.rooms[self.current_room]
        
        print(f"\n--- {room.name} ---")
        print(room.description)
        
        if not room.visited:
            room.visited = True
        
        # Show exits
        if room.exits:
            exits = ", ".join(room.exits.keys())
            print(f"\nExits: {exits}")
        
        # Show items
        if room.items:
            items = ", ".join([item.name for item in room.items.values()])
            print(f"Items here: {items}")
        
        # Show characters
        if room.characters:
            characters = ", ".join([char.name for char in room.characters.values()])
            print(f"People here: {characters}")

    def move(self, direction: str) -> bool:
        """Move to a different room"""
        room = self.rooms[self.current_room]
        
        if direction in room.exits:
            self.current_room = room.exits[direction]
            print(f"\nYou head {direction}...")
            return True
        else:
            print("You can't go that way.")
            return False

    def take_item(self, item_name: str):
        """Take an item from the current room"""
        room = self.rooms[self.current_room]
        
        if item_name in room.items:
            item = room.items[item_name]
            if item.takeable:
                self.inventory[item_name] = item
                del room.items[item_name]
                print(f"You take the {item.name}.")
                
                # Update game state
                if item_name == "sword":
                    self.game_state["has_weapon"] = True
                elif item_name == "potion":
                    self.game_state["has_potion"] = True
                    
            else:
                print(f"You can't take the {item.name}.")
        else:
            print("That item isn't here.")

    def use_item(self, item_name: str):
        """Use an item from inventory"""
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if item.use_text and not item.used:
                print(item.use_text)
                item.used = True
                
                # Special item effects
                if item_name == "mushroom":
                    self.game_state["amulet_power"] += 1
                    print("Your magical power increases!")
                elif item_name == "crystal":
                    self.game_state["amulet_power"] += 2
                    print("You feel significantly more powerful!")
                elif item_name == "amulet":
                    self.game_state["amulet_power"] += 5
                    print("The amulet's power flows through you!")
                elif item_name == "potion":
                    print("You feel refreshed and healed!")
                    
            else:
                print(f"You can't use the {item.name} right now.")
        else:
            print("You don't have that item.")

    def talk_to_character(self, char_name: str):
        """Talk to a character in the current room"""
        room = self.rooms[self.current_room]
        
        if char_name in room.characters:
            character = room.characters[char_name]
            if "talk" in character.dialogue:
                print(character.dialogue["talk"])
                
                # Special character interactions
                if char_name == "wizard" and not self.game_state["met_vee"]:
                    self.game_state["met_vee"] = True
                    print("\nThe wizard nods approvingly at your determination.")
                    
            else:
                print(f"The {character.name} doesn't seem interested in talking.")
        else:
            print("That person isn't here.")

    def fight_character(self, char_name: str):
        """Fight a character (mainly for the guardian)"""
        room = self.rooms[self.current_room]
        
        if char_name in room.characters:
            character = room.characters[char_name]
            
            if char_name == "guardian":
                if self.game_state["has_weapon"] and self.game_state["amulet_power"] >= 3:
                    print("You raise your enchanted sword and channel the amulet's power!")
                    print("The guardian's eyes dim as your magical energy overwhelms it.")
                    print("The massive golem crumbles to dust, defeated!")
                    del room.characters["guardian"]
                    self.game_state["bandits_defeated"] = True
                    print("\nA hidden treasure chest is revealed!")
                    treasure = Item("treasure", "A chest filled with ancient gold and magical artifacts.", True,
                                   "The treasure sparkles with otherworldly beauty!")
                    room.items["treasure"] = treasure
                else:
                    print("The guardian is too powerful! You need a weapon and more magical power.")
                    print("The guardian's attack sends you reeling back!")
            else:
                print(f"You can't fight the {character.name}.")
        else:
            print("That person isn't here.")

    def show_inventory(self):
        """Display player's inventory"""
        if self.inventory:
            items = ", ".join([item.name for item in self.inventory.values()])
            print(f"Inventory: {items}")
        else:
            print("Your inventory is empty.")

    def show_status(self):
        """Show game status"""
        print(f"\n--- Status ---")
        print(f"Location: {self.rooms[self.current_room].name}")
        print(f"Magical Power: {self.game_state['amulet_power']}")
        self.show_inventory()

    def check_win_condition(self):
        """Check if player has won the game"""
        if (self.game_state["amulet_power"] >= 8 and 
            "amulet" in self.inventory and 
            self.game_state["bandits_defeated"]):
            print("\n" + "="*50)
            print("🎉 CONGRATULATIONS! 🎉")
            print("You have completed Megan's Journey!")
            print("\nWith the Amulet of Power and your magical abilities,")
            print("you have saved the mystical realm from darkness!")
            print("The villagers celebrate your heroic deeds!")
            print("="*50)
            return True
        return False

    def parse_command(self, command: str) -> List[str]:
        """Parse user command into action and target"""
        command = command.lower().strip()
        words = command.split()
        
        if not words:
            return []
            
        # Handle multi-word commands
        if len(words) >= 2:
            if words[0] in ["go", "move", "walk"]:
                return ["move", words[1]]
            elif words[0] in ["take", "get", "pick"]:
                return ["take", " ".join(words[1:])]
            elif words[0] in ["use", "activate"]:
                return ["use", " ".join(words[1:])]
            elif words[0] in ["talk", "speak"]:
                return ["talk", " ".join(words[1:]).replace("to ", "")]
            elif words[0] in ["fight", "attack", "battle"]:
                return ["fight", " ".join(words[1:])]
            else:
                return [words[0], " ".join(words[1:])]
        else:
            return [words[0]]

    def process_command(self, command: str):
        """Process a user command"""
        parsed = self.parse_command(command)
        
        if not parsed:
            print("I don't understand that command.")
            return
            
        action = parsed[0]
        target = parsed[1] if len(parsed) > 1 else ""
        
        # Movement commands
        if action in ["north", "n"]:
            self.move("north")
        elif action in ["south", "s"]:
            self.move("south")
        elif action in ["east", "e"]:
            self.move("east")
        elif action in ["west", "w"]:
            self.move("west")
        elif action in ["up", "u"]:
            self.move("up")
        elif action in ["down", "d"]:
            self.move("down")
        elif action == "move" and target:
            self.move(target)
            
        # Object interaction
        elif action == "take" and target:
            self.take_item(target)
        elif action == "use" and target:
            self.use_item(target)
            
        # Character interaction
        elif action == "talk" and target:
            self.talk_to_character(target)
        elif action == "fight" and target:
            self.fight_character(target)
            
        # Information commands
        elif action in ["look", "l"]:
            self.display_room()
        elif action in ["inventory", "i", "inv"]:
            self.show_inventory()
        elif action in ["status", "stats"]:
            self.show_status()
            
        # Game commands
        elif action in ["help", "h"]:
            self.show_help()
        elif action in ["quit", "exit", "q"]:
            return False
            
        else:
            print("I don't understand that command. Type 'help' for available commands.")
            
        return True

    def show_help(self):
        """Display help information"""
        print("\n--- Commands ---")
        print("Movement: north/n, south/s, east/e, west/w, up/u, down/d")
        print("Actions: take <item>, use <item>, talk to <person>, fight <person>")
        print("Info: look/l, inventory/i, status, help/h")
        print("Game: quit/q")
        print("\nGoal: Collect magical items, gain power, and complete your quest!")

    def game_loop(self):
        """Main game loop"""
        print("="*60)
        print("🧙‍♀️ Welcome to Megan's Journey! 🧙‍♀️")
        print("A magical text adventure awaits...")
        print("="*60)
        print("\nYou are Megan, a brave adventurer on a quest to find the legendary")
        print("Amulet of Power and save the mystical realm from encroaching darkness.")
        print("\nType 'help' for commands or 'look' to examine your surroundings.")
        
        self.display_room()
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                    
                if not self.process_command(command):
                    print("\nThank you for playing Megan's Journey!")
                    break
                    
                # Check win condition after each command
                if self.check_win_condition():
                    break
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thank you for playing!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break

def main():
    """Start the game"""
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()