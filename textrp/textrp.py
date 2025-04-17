import sys
import random
from typing import List, Dict, Optional

# Constants
INITIAL_GOLD = 100
INITIAL_HEALTH = 100

# Global variables for user state
user_data: Dict[str, Optional[List]] = {
    "level": 1,
    "inventory": [],
    "gold": INITIAL_GOLD,
    "coolness": 0,
    "guild": None,
    "pets": [],
    "progress": "starter",
    "exp": 0,
    "health": INITIAL_HEALTH,
}

# Sample monsters with loot drops (name, level, health, attack, drops)
monsters: List[Dict] = [
    {"name": "Goblin", "level": 1, "health": 50, "attack": 10, "drops": ["Gold Coin", "Wooden Sword"]},
    {"name": "Skeleton", "level": 2, "health": 75, "attack": 15, "drops": ["Gold Coin", "Bone Armor"]},
    {"name": "Dragon", "level": 5, "health": 150, "attack": 30, "drops": ["Dragon Scale", "Gold Coin", "Flame Sword"]},
    {"name": "Troll", "level": 3, "health": 100, "attack": 20, "drops": ["Troll Hide", "Gold Coin"]},
]

# Sample dungeons with monsters and loot
dungeons: List[Dict] = [
    {"name": "Goblin Cave", "monsters": ["Goblin", "Skeleton"], "loot": ["Gold Coin", "Healing Potion"]},
    {"name": "Dark Forest", "monsters": ["Troll", "Goblin"], "loot": ["Mystic Gem", "Gold Coin"]},
    {"name": "Dragon's Lair", "monsters": ["Dragon"], "loot": ["Dragon Scale", "Flame Sword", "Gold Coin"]},
]

# Function to display headers
def print_header(title: str) -> None:
    print("\n" + "=" * 40)
    print(f"{title}")
    print("=" * 40)

# Show the help menu
def show_help() -> None:
    print("""
EPIC RPG CLI - COMMANDS

HORSE FESTIVAL
/hf               - Horse festival 2021

PROGRESS
/start            - Starter guide
/areas / /a      - Area guides
/dungeons / /d   - Dungeon guides
/timetravel / /tt - Time travel guide
/coolness         - Info about coolness

CRAFTING
/craft            - Recipes calculator
/dismantle / /dm  - Dismantling calculator
/invcalc / /ic    - Inventory calculator
/drops            - Monster drops
/enchants / /e    - Enchants info

HORSE & PETS
/horse            - Horse guide
/pet              - Pets guide

TRADING
/trading          - Trading guide

PROFESSIONS
/professions / /pr - Professions guide

GUILD
/guild            - Guild guide

EVENTS
/events           - Event guides

MONSTERS
/mobs [area]      - Monsters in [area]
/dailymob         - Today's monster
/fight [monster]  - Fight a monster
/dungeon [name]   - Enter a dungeon and fight monsters

GAMBLING
/gambling         - Gambling guide

MISC
/calc             - Calculator
/codes            - Redeemable codes
/duel             - Duel info
/farm             - Farming guide
/tip              - Random tip

LINKS
/invite           - Invite info
/support          - Support server
/links            - Wiki & support

SETTINGS
/settings / /me   - Your settings
/setprogress / /sp - Change progress
/prefix           - Show prefix
""")

# Function to handle commands
def handle_command(cmd: str) -> None:
    global user_data

    command_map = {
        "/start": start_guide,
        "/areas": area_guides,
        "/dungeons": dungeon_guides,
        "/coolness": coolness_info,
        "/tip": random_tip,
        "/guild": guild_guide,
        "/settings": user_settings,
        "/prefix": command_prefix,
        "/exit": exit_game,
    }

    if cmd.startswith("/dungeon "):
        enter_dungeon(cmd.split(" ", 1)[1])
    elif cmd.startswith("/fight "):
        fight_monster(cmd.split(" ", 1)[1])
    elif cmd.startswith("/join_guild "):
        join_guild(cmd.split(" ", 1)[1])
    elif cmd.startswith("/adopt_pet "):
        adopt_pet(cmd .split(" ", 1)[1])
    elif cmd.startswith("/mobs "):
        show_mobs(cmd.split(" ", 1)[1])
    elif cmd in command_map:
        command_map[cmd]()
    else:
        print("Unknown command. Type '/help' for a list of commands.")

def start_guide() -> None:
    print_header("Starter Guide")
    print("Welcome to TextRP CLI! Type /help for help!")

def area_guides() -> None:
    print_header("Area Guides")
    print("Areas: Forest, Cave, Desert, Snowy Peaks...")

def dungeon_guides() -> None:
    print_header("Dungeon Guides")
    print("Dungeons are challenging! Bring a team and gear up.")

def coolness_info() -> None:
    print_header("Coolness")
    print("Coolness is a rare stat that boosts drop rates and XP gain.")

def random_tip() -> None:
    tips = [
        "Always carry health potions!",
        "Upgrade your gear before dungeons.",
        "Check for redeemable codes weekly!",
    ]
    print_header("Random Tip")
    print(random.choice(tips))

def guild_guide() -> None:
    print_header("Guild Guide")
    if user_data["guild"]:
        print(f"You're part of the {user_data['guild']} guild!")
    else:
        print("You are not in a guild. Type '/join_guild [guild_name]' to join one.")

def user_settings() -> None:
    print_header("User  Settings")
    print(f"Level: {user_data['level']}")
    print(f"Gold: {user_data['gold']}")
    print(f"Coolness: {user_data['coolness']}")
    print(f"Guild: {user_data['guild']}")
    print(f"Pets: {', '.join(user_data['pets']) if user_data['pets'] else 'No pets'}")
    print(f"Health: {user_data['health']}")
    print(f"Experience: {user_data['exp']}")

def command_prefix() -> None:
    print_header("Command Prefix")
    print("Prefix for commands is '/'. Use '/help' for all available commands.")

def exit_game() -> None:
    print("Exiting game CLI. Goodbye!")
    sys.exit()

def fight_monster(monster_name: str) -> None:
    monster = next((m for m in monsters if m["name"].lower() == monster_name.lower()), None)
    if monster:
        print_header(f"Fighting {monster_name}!")
        fight(monster)
    else:
        print("Monster not found!")

def join_guild(guild_name: str) -> None:
    user_data["guild"] = guild_name
    print_header("Join Guild")
    print(f"Successfully joined the {guild_name} guild!")

def adopt_pet(pet_name: str) -> None:
    user_data["pets"].append(pet_name)
    print_header("Adopt Pet")
    print(f"Adopted a new pet named {pet_name}!")

def show_mobs(area: str) -> None:
    print_header(f"Monsters in {area.capitalize()}")
    print(f"List of monsters in {area.capitalize()}...")

# Function to handle a fight with a monster
def fight(monster: Dict) -> None:
    global user_data

    print(f"You encountered a {monster['name']} (Level {monster['level']})!")

    while user_data["health"] > 0 and monster["health"] > 0:
        print(f"\nYour Health: {user_data['health']} | {monster['name']} Health: {monster['health']}")
        action = input("Choose an action: [1] Attack  [2] Flee\n>> ")

        if action == "1":
            damage = random.randint(5, 15)
            monster["health"] -= damage
            print(f"You dealt {damage} damage to {monster['name']}!")

            if monster["health"] <= 0:
                print(f"\nYou defeated {monster['name']}!")
                loot(monster)
                break

            monster_damage = random.randint(5, monster["attack"])
            user_data["health"] -= monster_damage
            print(f"{monster['name']} attacks! You take {monster_damage} damage.")

        elif action == "2":
            print("You fled the battle.")
            break
        else:
            print("Invalid action. Choose [1] or [2].")

        if user_data["health"] <= 0:
            print("You have been defeated!")

# Function to handle loot drops
def loot(monster: Dict) -> None:
    global user_data
    loot_items = monster["drops"]
    loot_item = random.choice(loot_items)
    print(f"You found a {loot_item}!")

    if loot_item == "Gold Coin":
        user_data["gold"] += random.randint (1, 10)
        print(f"You gained some gold. Current gold: {user_data['gold']}")
    else:
        user_data["inventory"].append(loot_item)
        print(f"Added {loot_item} to your inventory.")

# Function to enter a dungeon
def enter_dungeon(dungeon_name: str) -> None:
    global user_data
    dungeon = next((d for d in dungeons if d["name"].lower() == dungeon_name.lower()), None)
    if dungeon:
        print_header(f"Entering {dungeon['name']}...")
        print("Prepare yourself for tough battles and great loot!")
        for monster_name in dungeon["monsters"]:
            monster = next(m for m in monsters if m["name"].lower() == monster_name.lower())
            fight(monster)
        print(f"You have completed the {dungeon['name']}!")
        loot_item = random.choice(dungeon["loot"])
        print(f"At the end of the dungeon, you found: {loot_item}")
        user_data["inventory"].append(loot_item)
    else:
        print(f"{dungeon_name} not found.")

# Main loop
if __name__ == "__main__":
    print("Welcome to TextRP CLI!")
    print("Type '/help' to view available commands.")
    while True:
        command = input("\n>> ").strip()
        handle_command(command)
