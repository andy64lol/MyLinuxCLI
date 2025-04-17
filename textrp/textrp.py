import sys
import random
import json
from typing import List, Dict, Optional
from datetime import datetime

# Constants
INITIAL_GOLD = 100
INITIAL_HEALTH = 100
EXP_TO_LEVEL = 100
CRITICAL_CHANCE = 0.15
DODGE_CHANCE = 0.1

# Weapon types and their properties
WEAPONS = {
    "Wooden Sword": {"damage": 5, "speed": 1.0, "price": 30},
    "Iron Sword": {"damage": 10, "speed": 1.0, "price": 80},
    "Steel Sword": {"damage": 15, "speed": 0.9, "price": 150},
    "Flame Sword": {"damage": 20, "speed": 1.1, "price": 300, "effect": "burn"},
    "Ice Sword": {"damage": 18, "speed": 0.8, "price": 300, "effect": "freeze"},
    "Magic Staff": {"damage": 12, "speed": 1.2, "price": 200, "effect": "magic"},
    "Battle Axe": {"damage": 25, "speed": 0.7, "price": 250},
    "Dagger": {"damage": 8, "speed": 1.5, "price": 100},
}

# Towns and locations
LOCATIONS = {
    "Greenwood Village": {
        "type": "town",
        "shops": ["Blacksmith", "General Store", "Magic Shop"],
        "monsters": ["Goblin", "Wolf"],
        "description": "A peaceful village surrounded by dense forest"
    },
    "Stormhaven": {
        "type": "town",
        "shops": ["Weaponsmith", "Armory", "Alchemist"],
        "monsters": ["Skeleton", "Ghost"],
        "description": "A coastal town known for its skilled craftsmen"
    },
    "Dragon's Peak": {
        "type": "dangerous",
        "monsters": ["Fire Dragon", "Ice Dragon"],
        "description": "A treacherous mountain where dragons dwell"
    },
    "Crystal Cave": {
        "type": "dungeon",
        "monsters": ["Crystal Golem", "Cave Troll"],
        "description": "A cave system filled with valuable crystals"
    },
    "Shadowmere": {
        "type": "town",
        "shops": ["Dark Market", "Mystic Shop"],
        "monsters": ["Shadow Beast", "Dark Knight"],
        "description": "A mysterious town shrouded in eternal twilight"
    }
}

# Character classes
CHARACTER_CLASSES = {
    "Warrior": {"health_bonus": 50, "attack_bonus": 10, "defense_bonus": 15},
    "Mage": {"health_bonus": -20, "attack_bonus": 25, "defense_bonus": 0},
    "Rogue": {"health_bonus": 0, "attack_bonus": 15, "defense_bonus": 5},
    "Paladin": {"health_bonus": 30, "attack_bonus": 15, "defense_bonus": 20},
    "Archer": {"health_bonus": -10, "attack_bonus": 20, "defense_bonus": 5},
    "Berserker": {"health_bonus": 20, "attack_bonus": 30, "defense_bonus": -10},
    "Priest": {"health_bonus": 10, "attack_bonus": 5, "defense_bonus": 10},
    "Assassin": {"health_bonus": -15, "attack_bonus": 35, "defense_bonus": -5}
}

# Item rarity
RARITY_MULTIPLIERS = {
    "Common": 1.0,
    "Uncommon": 1.2,
    "Rare": 1.5,
    "Epic": 2.0,
    "Legendary": 3.0
}

# Basic skills
SKILLS = {
    "Warrior": ["Slam", "Shield Block", "Berserk"],
    "Mage": ["Fireball", "Ice Shield", "Lightning Bolt"],
    "Rogue": ["Backstab", "Stealth", "Poison Strike"],
    "Paladin": ["Holy Strike", "Divine Shield", "Healing Light"],
    "Archer": ["Quick Shot", "Rain of Arrows", "Eagle Eye"],
    "Berserker": ["Rage", "Whirlwind", "Blood Thirst"],
    "Priest": ["Holy Nova", "Divine Heal", "Smite"],
    "Assassin": ["Shadow Strike", "Vanish", "Death Mark"]
}

# Enhanced crafting system
CRAFTING_RECIPES = {
    "Iron Sword": {
        "materials": {"Iron Ingot": 2, "Wood": 1},
        "level_required": 2,
        "type": "weapon",
        "effect": 10
    },
    "Steel Sword": {
        "materials": {"Steel Ingot": 2, "Leather": 1},
        "level_required": 5,
        "type": "weapon",
        "effect": 15
    },
    "Health Potion": {
        "materials": {"Red Herb": 2, "Water Flask": 1},
        "level_required": 1,
        "type": "consumable",
        "effect": 30
    },
    "Iron Armor": {
        "materials": {"Iron Ingot": 4, "Leather": 2},
        "level_required": 3,
        "type": "armor",
        "effect": 10
    }
}

# Materials that can be gathered
MATERIALS = {
    "Wood": {"areas": ["Forest"], "tool_required": "Axe"},
    "Iron Ore": {"areas": ["Cave", "Mountain"], "tool_required": "Pickaxe"},
    "Red Herb": {"areas": ["Forest", "Plains"], "tool_required": None},
    "Water Flask": {"areas": ["River", "Lake"], "tool_required": "Flask"},
    "Leather": {"areas": ["Plains"], "tool_required": "Hunting Knife"},
    "Steel Ingot": {"areas": ["Blacksmith"], "tool_required": "Furnace"}
}

# Sample quests
QUESTS = [
    {
        "id": 1,
        "name": "Goblin Slayer",
        "description": "Kill 3 goblins",
        "target": {"monster": "Goblin", "count": 3},
        "reward": {"gold": 50, "exp": 100}
    },
    {
        "id": 2,
        "name": "Dragon Hunter",
        "description": "Defeat any dragon",
        "target": {"monster": "Dragon", "count": 1},
        "reward": {"gold": 200, "exp": 300}
    }
]

# Initialize user data with proper typing
user_data: Dict = {
    "class": None,
    "level": 1,
    "inventory": [],
    "equipped": {"weapon": None, "armor": None},
    "gold": INITIAL_GOLD,
    "coolness": 0,
    "guild": None,
    "pets": [],
    "progress": "starter",
    "exp": 0,
    "health": INITIAL_HEALTH,
    "max_health": INITIAL_HEALTH,
    "attack": 10,
    "defense": 0,
    "skills": [],
    "active_quests": [],
    "completed_quests": [],
    "materials": {},
    "tools": ["Axe", "Pickaxe", "Flask", "Hunting Knife"],  # Starting tools
    "current_area": "Town"
}

# Shop items
shop_items = [
    {"name": "Wooden Sword", "type": "weapon", "effect": 5, "price": 30},
    {"name": "Iron Sword", "type": "weapon", "effect": 10, "price": 80},
    {"name": "Bone Armor", "type": "armor", "effect": 5, "price": 40},
    {"name": "Iron Armor", "type": "armor", "effect": 10, "price": 100},
    {"name": "Healing Potion", "type": "consumable", "effect": 30, "price": 20},
]

# Sample monsters with loot drops (name, level, health, attack, drops)
monsters: List[Dict] = [
    {"name": "Goblin", "level": 1, "health": 50, "attack": 10, "drops": ["Gold Coin", "Wooden Sword"]},
    {"name": "Skeleton", "level": 2, "health": 75, "attack": 15, "drops": ["Gold Coin", "Bone Armor"]},
    {"name": "Fire Dragon", "level": 5, "health": 150, "attack": 30, "drops": ["Dragon Scale", "Gold Coin", "Flame Sword"]},
    {"name": "Ice Dragon", "level": 5, "health": 150, "attack": 30, "drops": ["Dragon Scale", "Gold Coin", "Ice Sword"]},
    {"name": "Dark Knight", "level": 4, "health": 120, "attack": 25, "drops": ["Dark Armor", "Gold Coin"]},
    {"name": "Troll", "level": 3, "health": 100, "attack": 20, "drops": ["Troll Hide", "Gold Coin"]},
    {"name": "Vampire", "level": 4, "health": 120, "attack": 25, "drops": ["Blood Gem", "Gold Coin"]},
    {"name": "Werewolf", "level": 3, "health": 90, "attack": 20, "drops": ["Fur Cloak", "Gold Coin"]},
    {"name": "Zombie", "level": 1, "health": 40, "attack": 5, "drops": ["Rotten Flesh", "Gold Coin"]},
    {"name": "Mummy", "level": 2, "health": 60, "attack": 10, "drops": ["Ancient Artifact", "Gold Coin"]},
    {"name": "Giant Spider", "level": 3, "health": 80, "attack": 15, "drops": ["Spider Silk", "Gold Coin"]},
    {"name": "spider", "level": 2, "health": 70, "attack": 12, "drops": ["Webbing", "Gold Coin"]},
    {"name": "Giant", "level": 4, "health": 110, "attack": 25, "drops": ["Giant's Club", "Gold Coin"]},
    {"name": "Ghost", "level": 4, "health": 100, "attack": 20, "drops": ["Spirit Essence", "Gold Coin"]},
    {"name": "Hellhound", "level": 5, "health": 130, "attack": 28, "drops": ["Hellfire Gem", "Gold Coin"]},
    {"name": "Griffin", "level": 5, "health": 140, "attack": 30, "drops": ["Griffin Feather", "Gold Coin"]},
    {"name": "Harpy", "level": 5, "health": 130, "attack": 28, "drops": ["Harpy Wing", "Gold Coin"]},
]

# Dungeons with monsters and loot
dungeons: List[Dict] = [
    {"name": "Goblin Cave", "monsters": ["Goblin", "Skeleton"], "loot": ["Gold Coin", "Healing Potion"]},
    {"name": "Dark Forest", "monsters": ["Troll", "Goblin"], "loot": ["Mystic Gem", "Gold Coin"]},
    {"name": "Fire Dragon's Lair", "monsters": ["Fire Dragon"], "loot": ["Dragon Scale", "Flame Sword", "Gold Coin"]},
    {"name": "Ice Dragon's Lair", "monsters": ["Ice Dragon"], "loot": ["Dragon Scale", "Ice Sword", "Gold Coin"]},
    {"name": "Vampire Castle", "monsters": ["Vampire", "Skeleton"], "loot": ["Blood Gem", "Gold Coin"]},
    {"name": "Werewolf Den", "monsters": ["Werewolf", "Zombie"], "loot": ["Fur Cloak", "Gold Coin"]},
    {"name": "Mummy Tomb", "monsters": ["Mummy", "Skeleton"], "loot": ["Ancient Artifact", "Gold Coin"]},
    {"name": "Giant Spider's Web", "monsters": ["Giant Spider", "spider"], "loot": ["Spider Silk", "Gold Coin"]},
    {"name": "Giant's Lair", "monsters": ["Giant"], "loot": ["Giant's Club", "Gold Coin"]},
    {"name": "Ghost Town", "monsters": ["Ghost"], "loot": ["Spirit Essence", "Gold Coin"]},
    {"name": "Hellhound's Den", "monsters": ["Hellhound"], "loot": ["Hellfire Gem", "Gold Coin"]},
    {"name": "Griffin's Nest", "monsters": ["Griffin"], "loot": ["Griffin Feather", "Gold Coin"]},
    {"name": "Harpy's Roost", "monsters": ["Harpy"], "loot": ["Harpy Wing", "Gold Coin"]},
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

PROGRESS
/start            - Starter guide
/areas             - Area guides
/dungeons          - Dungeon guides
/timetravel        - Time travel guide
/coolness          - Info about coolness

CRAFTING
/craft             - Recipes calculator
/dismantle         - Dismantling calculator
/invcalc           - Inventory calculator
/drops             - Monster drops
/enchants          - Enchantments info

HORSE & PETS
/horse             - Horse guide
/pet               - Pets guide

TRADING
/trading           - Trading guide

PROFESSIONS
/professions       - Professions guide

GUILD
/guild             - Guild guide

EVENTS
/events            - Event guides

MONSTERS
/mobs [area]       - Monsters in [area]
/dailymob          - Today's monster
/fight [monster]   - Fight a monster
/dungeon [name]    - Enter a dungeon
/dungeon_list      - List all dungeons
/bestiary          - List all monsters

GAMBLING
/gambling          - Gambling guide

MISC
/codes             - Redeemable codes
/duel              - Duel info
/farm              - Farming guide
/tip               - Random tip
/shop              - Visit the shop
/equip [item]      - Equip an item
/stats             - Show your stats
/support           - Support information
/save              - Save game
/load              - Load game
/quests            - View and accept quests
/new               - Create a new character
/inventory         - Show your inventory

SETTINGS
/settings          - Your settings
/setprogress       - Change progress
/prefix            - Show prefix
/exit              - Exit game
/gather            - Gather materials
/materials         - Show materials
/travel            - Travel to area
""")

# Function to handle commands
def handle_command(cmd: str) -> None:
    commands = {
        "/start": start_guide,
        "/help": show_help,
        "/pet": show_pets,
        "/mobs": show_mobs,
        "/professions": show_professions,
        "/stats": show_stats,
        "/shop": visit_shop,
        "/inventory": show_inventory,
        "/quests": show_quests,
        "/gather": lambda: gather_materials(user_data["current_area"]),
        "/craft": craft_item,
        "/materials": print_materials,
        "/travel": travel_to_area,
        "/new": create_character,
        "/save": save_game,
        "/load": load_game,
        "/exit": exit_game,
        "/guild": guild_guide,
        "/areas": area_guides,
        "/dungeons": dungeon_guides,
        "/timetravel": time_travel_guide,
        "/coolness": coolness_info,
        "/dismantle": dismantle_items,
        "/invcalc": inventory_calculator,
        "/drops": show_drops,
        "/enchants": show_enchants,
        "/horse": horse_festival,
        "/trading": lambda: print("Trading system coming soon!"),
        "/professions": lambda: print("Professions system coming soon!"),
        "/events": lambda: print("No active events at the moment."),
        "/gambling": gambling_guide,
        "/codes": redeem_codes,
        "/duel": duel_info,
        "/farm": farming_guide,
        "/tip": random_tip,
        "/support": show_support,
        "/dungeon_list": list_dungeons,
        "/bestiary": show_bestiary,
        "/dailymob": daily_monster,
        "/weapon_info": lambda: show_weapon_info(),
        "/settings": user_settings,
        "/setprogress": lambda: print("Progress system coming soon!"),
        "/prefix": command_prefix
    }

    # Handle commands with arguments
    if cmd.startswith("/fight "):
        fight_monster(cmd.split(" ", 1)[1])
    elif cmd.startswith("/equip "):
        equip_item(cmd.split(" ", 1)[1])
    elif cmd.startswith("/dungeon "):
        enter_dungeon(cmd.split(" ", 1)[1])
    elif cmd in commands:
        commands[cmd]()
    else:
        print("Unknown command. Type '/help' for a list of commands.")

# Define functions
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
    print_header("User Settings")
    print(f"Level: {user_data['level']}")
    print(f"Gold: {user_data['gold']}")
    print(f"Coolness: {user_data['coolness']}")
    print(f"Guild: {user_data['guild']}")
    print(f"Pets: {', '.join(user_data['pets']) if user_data['pets'] else 'No pets'}")
    print(f"Health: {user_data['health']}/{user_data['max_health']}")
    print(f"Experience: {user_data['exp']}")
    print(f"Current Area: {user_data['current_area']}")
    print_materials()

def command_prefix() -> None:
    print_header("Command Prefix")
    print("Prefix for commands is '/'. Use '/help' for all available commands.")

def exit_game() -> None:
    print("Exiting game CLI. Goodbye!")
    sys.exit()

def show_villages() -> None:
    print_header("Villages")
    for village in villages:
        print(f"Name: {village['name']}, Population: {village['population']}, Special Items: {', '.join(village['special_items'])}")

def show_biomes() -> None:
    print_header("Biomes")
    for biome in biomes:
        print(f"Name: {biome['name']}, Description: {biome['description']}")

def join_guild(guild_name: str) -> None:
    user_data["guild"] = guild_name
    print_header("Join Guild")
    print(f"Successfully joined the {guild_name} guild!")

def adopt_pet(pet_name: str) -> None:
    user_data["pets"].append(pet_name)
    print_header("Adopt Pet")
    print(f"Adopted a new pet named {pet_name}!")

def show_mobs(area: str = None) -> None:
    print_header("Monsters")
    if area:
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(area, {}).get("monsters", [])]
        if area_monsters:
            print(f"Monsters in {area}:")
            for monster in area_monsters:
                print(f"- {monster['name']} (Level {monster['level']})")
        else:
            print(f"No monsters found in {area}")
    else:
        current_area = user_data["current_area"]
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(current_area, {}).get("monsters", [])]
        if area_monsters:
            print(f"Monsters in {current_area}:")
            for monster in area_monsters:
                print(f"- {monster['name']} (Level {monster['level']})")
        else:
            print("No monsters in current area")

# Function to handle a fight with a monster
def fight(monster: Dict) -> None:
    global user_data
    monster_health = monster["health"]

    print(f"You encountered a {monster['name']} (Level {monster['level']})!")

    while user_data["health"] > 0 and monster_health > 0:
        print(f"\nYour Health: {user_data['health']}/{user_data['max_health']} | {monster['name']} Health: {monster_health}")
        print("\nActions:")
        print("[1] Attack")
        print("[2] Use Skill")
        print("[3] Use Health Potion")
        print("[4] Flee")

        action = input("Choose an action: ")

        if action == "1":
            # Normal attack with critical chance
            damage = random.randint(5, 15) + (user_data["equipped"]["weapon"]["effect"] if user_data["equipped"]["weapon"] else 0)
            if random.random() < CRITICAL_CHANCE:
                damage *= 2
                print("Critical hit!")
            monster_health -= damage
            print(f"You dealt {damage} damage to {monster['name']}!")

        elif action == "2":
            if user_data["skills"]:
                print("\nAvailable skills:")
                for i, skill in enumerate(user_data["skills"], 1):
                    print(f"[{i}] {skill}")
                try:
                    skill_choice = int(input("Choose skill (0 to cancel): "))
                    if 0 < skill_choice <= len(user_data["skills"]):
                        skill = user_data["skills"][skill_choice - 1]
                        damage = random.randint(15, 25)  # Skills do more damage
                        monster_health -= damage
                        print(f"You used {skill} and dealt {damage} damage!")
                except ValueError:
                    print("Invalid choice.")
            else:
                print("You have no skills available!")
                continue

        elif action == "3":
            if "Healing Potion" in user_data["inventory"]:
                user_data["health"] = min(user_data["health"] + 30, user_data["max_health"])
                user_data["inventory"].remove("Healing Potion")
                print("You used a Healing Potion! Health restored.")
                continue
            else:
                print("You have no Healing Potions!")
                continue

        elif action == "4":
            if random.random() < 0.7:  # 70% chance to flee
                print("You successfully fled the battle!")
                return
            print("Failed to flee!")

        else:
            print("Invalid action!")
            continue

        # Monster's turn
        if monster_health > 0:
            if random.random() > DODGE_CHANCE:  # Dodge chance
                monster_damage = max(1, random.randint(5, monster["attack"]) - (user_data["equipped"]["armor"]["effect"] if user_data["equipped"]["armor"] else 0))
                user_data["health"] -= monster_damage
                print(f"{monster['name']} attacks! You take {monster_damage} damage.")
            else:
                print("You dodged the attack!")

    if monster_health <= 0:
        print(f"\nYou defeated {monster['name']}!")
        exp_gain = monster["level"] * 20
        user_data["exp"] += exp_gain
        print(f"You gained {exp_gain} experience!")

        # Level up check
        check_level_up()

        # Quest progress
        update_quest_progress(monster["name"])

        loot(monster)

def level_up() -> None:
    user_data["level"] += 1
    user_data["max_health"] += 20
    user_data["health"] = user_data["max_health"]
    user_data["attack"] += 5
    user_data["defense"] += 3
    print(f"\nLevel Up! You are now level {user_data['level']}!")
    print("Your stats have increased!")

def update_quest_progress(monster_name: str) -> None:
    for quest in user_data["active_quests"]:
        if quest["target"]["monster"] == monster_name:
            quest["target"]["count"] -= 1
            if quest["target"]["count"] <= 0:
                complete_quest(quest)

def complete_quest(quest: Dict) -> None:
    print(f"\nQuest Complete: {quest['name']}")
    user_data["gold"] += quest["reward"]["gold"]
    user_data["exp"] += quest["reward"]["exp"]
    user_data["active_quests"].remove(quest)
    user_data["completed_quests"].append(quest["id"])
    print(f"Rewards: {quest['reward']['gold']} gold, {quest['reward']['exp']} exp")

def save_game() -> None:
    with open("savegame.json", "w") as f:
        json.dump(user_data, f)
    print("Game saved successfully!")

def load_game() -> bool:
    try:
        with open("savegame.json", "r") as f:
            global user_data
            user_data = json.load(f)
        print("Game loaded successfully!")
        return True
    except FileNotFoundError:
        print("No saved game found.")
        return False

def show_quests() -> None:
    print_header("Available Quests")
    for quest in QUESTS:
        if quest["id"] not in user_data["completed_quests"] and quest not in user_data["active_quests"]:
            print(f"\n{quest['name']}")
            print(f"Description: {quest['description']}")
            print(f"Reward: {quest['reward']['gold']} gold, {quest['reward']['exp']} exp")
            if input("Accept quest? (y/n): ").lower() == 'y':
                user_data["active_quests"].append(quest)
                print("Quest accepted!")


# Function to handle loot drops
def loot(monster: Dict) -> None:
    global user_data
    drops = monster["drops"]
    print("\nLoot found:")
    for idx, item in enumerate(drops, 1):
        print(f"{idx}. {item}")

    try:
        choice = int(input(f"Choose item to take (1-{len(drops)}): "))
        if 1 <= choice <= len(drops):
            item = drops[choice - 1]
            if item == "Gold Coin":
                gold_amount = random.randint(5, 15)
                user_data["gold"] += gold_amount
                print(f"Gained {gold_amount} gold!")
            else:
                user_data["inventory"].append(item)
                print(f"Added {item} to inventory!")
        else:
            print("Invalid choice, no loot taken.")
    except ValueError:
        print("Invalid input, no loot taken.")

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

# Shop functions
def visit_shop() -> None:
    print_header("Shop")
    print("Welcome to the shop! What would you like to buy?")
    for idx, item in enumerate(shop_items):
        print(f"{idx + 1}. {item['name']} - {item['price']} gold")
    print(f"{len(shop_items) + 1}. Exit shop")

    choice = int(input("Choose an item to buy (1-{}): ".format(len(shop_items) + 1)))
    if 1 <= choice <= len(shop_items):
        buy_item(choice - 1)
    elif choice == len(shop_items) + 1:
        print("Exiting shop...")
    else:
        print("Invalid choice.")

def buy_item(item_index: int) -> None:
    global user_data
    item = shop_items[item_index]
    if user_data["gold"] >= item["price"]:
        user_data["gold"] -= item["price"]
        user_data["inventory"].append(item["name"])
        print(f"You bought {item['name']} for {item['price']} gold!")
    else:
        print("You don't have enough gold!")

def equip_item(item_name: str) -> None:
    global user_data
    item = next((i for i in user_data["inventory"] if i.lower() == item_name.lower()), None)
    if item:
        item_type = None
        effect = 0

        # Determine item type and effect
        if item in ["Wooden Sword", "Iron Sword", "Flame Sword", "Ice Sword", "Steel Sword"]:
            item_type = "weapon"
            effect = 5 if item == "Wooden Sword" else 10 if item == "Iron Sword" else 15 if item == "Steel Sword" else 15
        elif item in ["Bone Armor", "Iron Armor", "Dark Armor"]:
            item_type = "armor"
            effect = 5 if item == "Bone Armor" else 10 if item == "Iron Armor" else 15

        if item_type:
            user_data["equipped"][item_type] = {"name": item, "effect": effect}
            print_header("Equip Item")
            print(f"You equipped {item}!")
        else:
            print(f"{item} cannot be equipped.")
    else:
        print(f"You don't have {item_name} in your inventory.")

def show_stats() -> None:
    print_header("Your Stats")
    print(f"Level: {user_data['level']}")
    print(f"Health: {user_data['health']}/{user_data['max_health']}")
    print(f"Attack: {user_data['attack'] + (user_data['equipped']['weapon']['effect'] if user_data['equipped']['weapon'] else 0)}")
    print(f"Defense: {user_data['defense'] + (user_data['equipped']['armor']['effect'] if user_data['equipped']['armor'] else 0)}")
    print(f"Gold: {user_data['gold']}")
    print(f"Equipped Weapon: {user_data['equipped']['weapon']['name'] if user_data['equipped']['weapon'] else 'None'}")
    print(f"Equipped Armor: {user_data['equipped']['armor']['name'] if user_data['equipped']['armor'] else 'None'}")

# New functions for additional commands
def list_dungeons() -> None:
    print_header("Dungeon List")
    for dungeon in dungeons:
        print(f"Name: {dungeon['name']}, Monsters: {', '.join(dungeon['monsters'])}, Loot: {', '.join(dungeon['loot'])}")

def show_bestiary() -> None:
    print_header("Bestiary")
    for monster in monsters:
        print(f"Name: {monster['name']}, Level: {monster['level']}, Health: {monster['health']}, Attack: {monster['attack']}, Drops: {', '.join(monster['drops'])}")

def show_support() -> None:
    print_header("Support Information")
    print("For support, visit our Discord server or check the wiki.")
    print("Wiki: https://example.com/wiki")
    print("Discord: https://discord.gg/example")

# Function stubs for other commands
def farming_guide() -> None:
    print_header("Farming Guide")
    print("Farming allows you to gather resources and grow crops for crafting and trading.")

def duel_info() -> None:
    print_header("Duel Info")
    print("Duels allow you to challenge other players for rewards and bragging rights.")
    print("Use '/duel [player_name]' to initiate a duel.")

def redeem_codes() -> None:
    print_header("Redeemable Codes")
    print("Enter redeemable codes to claim rewards!")
    code = input("Enter code: ").strip()
    if code == "WELCOME2023":
        print("Code redeemed! You received 50 gold.")
        user_data["gold"] += 50
    else:
        print("Invalid code. Try again.")

def gambling_guide() -> None:
    print_header("Gambling Guide")
    print("Gambling allows you to risk your gold for a chance to win big rewards. Play responsibly!")

def daily_monster() -> None:
    print_header("Daily Monster")
    monster = random.choice(monsters)
    print(f"Today's monster is: {monster['name']} (Level {monster['level']})")
    print(f"Health: {monster['health']}, Attack: {monster['attack']}")
    print(f"Loot: {', '.join(monster['drops'])}")

def inventory_calculator() -> None:
    print_header("Inventory Calculator")
    print("This feature calculates the total value of your inventory.")

def time_travel_guide() -> None:
    print_header("Time Travel Guide")
    print("Time travel allows you to revisit past events and gain unique rewards.")

def craft_recipes() -> None:
    print_header("Crafting Recipes")
    print("Crafting recipes will be displayed here.")

def dismantle_items() -> None:
    print_header("Dismantling Items")
    print("Dismantling items will be displayed here.")

def show_drops() -> None:
    print_header("Monster Drops")
    print("Monster drops will be displayed here.")

def show_enchants() -> None:
    print_header("Enchantments")
    print("Enchantments will be displayed here.")

def show_inventory() -> None:
    print_header("Inventory")
    if not user_data["inventory"]:
        print("Your inventory is empty.")
        return
    for idx, item in enumerate(user_data["inventory"], 1):
        print(f"{idx}. {item}")

def create_character() -> None:
    print_header("Character Creation")
    print("Choose your class:")
    for class_name in CHARACTER_CLASSES:
        print(f"[{class_name}]")
        for stat, value in CHARACTER_CLASSES[class_name].items():
            print(f"  {stat}: {value:+}")

    while True:
        choice = input("Enter class name: ").capitalize()
        if choice in CHARACTER_CLASSES:
            user_data["class"] = choice
            user_data["skills"] = SKILLS[choice]
            stats = CHARACTER_CLASSES[choice]
            user_data["max_health"] += stats["health_bonus"]
            user_data["health"] = user_data["max_health"]
            user_data["attack"] += stats["attack_bonus"]
            user_data["defense"] += stats["defense_bonus"]
            print(f"\nWelcome, {choice}! Your adventure begins...")
            break
        print("Invalid class. Try again.")

# Sample villages (added for completeness)
villages = [
    {"name": "Greenwood", "population": 150, "special_items": ["Herbal Potion", "Wooden Bow"]},
    {"name": "Stonehaven", "population": 200, "special_items": ["Iron Sword", "Shield"]},
    # ... other villages
]

# Sample biomes (added for completeness)
biomes = [
    {"name": "Forest", "description": "A lush green area filled with trees and wildlife."},
    {"name": "Desert", "description": "A vast sandy area with scarce resources."},
    # ... other biomes
]

# Horse festival function (added for completeness)
def horse_festival() -> None:
    print_header("Horse Festival")
    print("The annual Horse Festival is a grand event with exciting races and prizes.")

# New function for gathering materials
def gather_materials(area: str) -> None:
    if area not in [mat["areas"] for mat in MATERIALS.values()]:
        print(f"No materials can be gathered in {area}")
        return

    available_materials = [name for name, info in MATERIALS.items() if area in info["areas"]]
    print(f"\nAvailable materials in {area}:")
    for i, mat in enumerate(available_materials, 1):
        tool_req = MATERIALS[mat]["tool_required"]
        print(f"{i}. {mat} {'(Requires: ' + tool_req + ')' if tool_req else ''}")

    choice = input("\nChoose material to gather (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(available_materials):
            material = available_materials[choice - 1]
            tool_required = MATERIALS[material]["tool_required"]

            if tool_required and tool_required not in user_data["tools"]:
                print(f"You need a {tool_required} to gather {material}")
                return

            amount = random.randint(1, 3)
            user_data["materials"][material] = user_data["materials"].get(material, 0) + amount
            print(f"Gathered {amount} {material}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def craft_item() -> None:
    print_header("Crafting")
    available_recipes = [name for name, recipe in CRAFTING_RECIPES.items()
                        if user_data["level"] >= recipe["level_required"]]

    if not available_recipes:
        print("No recipes available at your level")
        return

    print("\nAvailable recipes:")
    for i, recipe_name in enumerate(available_recipes, 1):
        recipe = CRAFTING_RECIPES[recipe_name]
        print(f"\n{i}. {recipe_name}")
        print("Required materials:")
        for material, amount in recipe["materials"].items():
            have_amount = user_data["materials"].get(material, 0)
            print(f"  - {material}: {amount} (Have: {have_amount})")
        print(f"Level required: {recipe['level_required']}")

    choice = input("\nChoose item to craft (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(available_recipes):
            recipe_name = available_recipes[choice - 1]
            recipe = CRAFTING_RECIPES[recipe_name]

            # Check materials
            can_craft = True
            for material, amount in recipe["materials"].items():
                if user_data["materials"].get(material, 0) < amount:
                    print(f"Not enough {material}")
                    can_craft = False

            if can_craft:
                # Consume materials
                for material, amount in recipe["materials"].items():
                    user_data["materials"][material] -= amount

                # Add item to inventory
                user_data["inventory"].append(recipe_name)
                print(f"Successfully crafted {recipe_name}!")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def print_materials() -> None:
    print_header("Materials")
    if not user_data["materials"]:
        print("You don't have any materials")
        return

    for material, amount in user_data["materials"].items():
        print(f"{material}: {amount}")

def travel_to_area() -> None:
    print_header("Travel")
    print("\nAvailable locations:")
    locations = list(LOCATIONS.keys())
    for i, loc in enumerate(locations, 1):
        info = LOCATIONS[loc]
        print(f"{i}. {loc} - {info['description']}")
        if info['type'] == 'town':
            print(f"   Shops: {', '.join(info['shops'])}")

    choice = input("\nChoose area to travel to (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(locations):
            user_data["current_area"] = locations[choice - 1]
            print(f"Traveled to {user_data['current_area']}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def fight_monster(monster_name: str) -> None:
    monster = next((m for m in monsters if m["name"].lower() == monster_name.lower()), None)
    if not monster:
        print(f"Monster '{monster_name}' not found!")
        return

    if user_data["health"] <= 0:
        print("You can't fight while defeated! Use a healing potion or rest.")
        return

    print_header(f"Fighting {monster['name']}")
    monster_health = monster["health"]

    while user_data["health"] > 0 and monster_health > 0:
        try:
            print(f"\nYour Health: {user_data['health']}/{user_data['max_health']}")
            print(f"Monster Health: {monster_health}/{monster['health']}")
            print("\nActions:")
            print("1. Attack")
            print("2. Use Healing Potion")
            print("3. Flee")

            choice = input("Choose action (1-3): ").strip()

            if choice == "1":
                # Calculate damage with equipped weapon
                base_damage = user_data["attack"]
                weapon_bonus = user_data["equipped"]["weapon"]["effect"] if user_data["equipped"]["weapon"] else 0
                damage = base_damage + weapon_bonus

                if random.random() < CRITICAL_CHANCE:
                    damage *= 2
                    print("Critical hit!")

                monster_health -= damage
                print(f"You deal {damage} damage!")

            elif choice == "2":
                if "Healing Potion" in user_data["inventory"]:
                    heal_amount = 30
                    user_data["health"] = min(user_data["max_health"], user_data["health"] + heal_amount)
                    user_data["inventory"].remove("Healing Potion")
                    print(f"You heal for {heal_amount} health!")
                else:
                    print("No healing potions available!")
                    continue

            elif choice == "3":
                if random.random() < 0.6:
                    print("You successfully fled!")
                    return
                print("Failed to flee!")

            else:
                print("Invalid choice!")
                continue

            # Monster attacks if still alive
            if monster_health > 0:
                defense_bonus = user_data["equipped"]["armor"]["effect"] if user_data["equipped"]["armor"] else 0
                damage_taken = max(1, monster["attack"] - defense_bonus)
                if random.random() > DODGE_CHANCE:
                    user_data["health"] -= damage_taken
                    print(f"Monster deals {damage_taken} damage!")
                else:
                    print("You dodged the attack!")

        except Exception as e:
            print(f"Error during combat: {e}")
            return

    if monster_health <= 0:
        print(f"\nYou defeated the {monster['name']}!")
        exp_gain = monster["level"] * 20
        user_data["exp"] += exp_gain
        print(f"Gained {exp_gain} experience!")

        # Handle loot
        loot(monster)

        # Check for level up
        check_level_up()
    else:
        print("You were defeated!")

def check_level_up() -> None:
    while user_data["exp"] >= EXP_TO_LEVEL * user_data["level"]:
        user_data["level"] += 1
        user_data["max_health"] += 20
        user_data["health"] = user_data["max_health"]
        user_data["attack"] += 5
        user_data["defense"] += 3
        print(f"\nLevel Up! You are now level {user_data['level']}!")
        print("Your stats have increased!")
        print(f"Health: {user_data['health']}/{user_data['max_health']}")
        print(f"Attack: {user_data['attack']}")
        print(f"Defense: {user_data['defense']}")

def show_weapon_info() -> None:
    print_header("Weapon Information")

def show_pets() -> None:
    print_header("Pet System")
    if not user_data["pets"]:
        print("You don't have any pets yet!")
        print("\nAvailable pets to adopt:")
        available_pets = ["Cat", "Dog", "Dragon Hatchling", "Phoenix Chick"]
        for i, pet in enumerate(available_pets, 1):
            print(f"{i}. {pet}")
        
        try:
            choice = input("\nChoose a pet to adopt (0 to cancel): ")
            if choice.isdigit() and 1 <= int(choice) <= len(available_pets):
                pet = available_pets[int(choice) - 1]
                user_data["pets"].append(pet)
                print(f"\nYou adopted a {pet}!")
        except ValueError:
            print("Invalid choice")
    else:
        print("Your pets:")
        for pet in user_data["pets"]:
            print(f"- {pet}")

def show_professions() -> None:
    print_header("Professions")
    professions = {
        "Mining": "Gather ore and precious stones",
        "Herbalism": "Collect and process herbs",
        "Smithing": "Craft weapons and armor",
        "Alchemy": "Create potions and elixirs"
    }
    
    print("Available professions:")
    for prof, desc in professions.items():
        print(f"\n{prof}:")
        print(f"  {desc}")
    for weapon, stats in WEAPONS.items():
        print(f"\n{weapon}:")
        print(f"  Damage: {stats['damage']}")
        print(f"  Speed: {stats['speed']}")
        print(f"  Price: {stats['price']} gold")
        if 'effect' in stats:
            print(f"  Special Effect: {stats['effect']}")

# Main loop
if __name__ == "__main__":
    print("Welcome to Enhanced TextRP CLI!")
    print("Type '/help' for commands or '/new' to create a character.")

    while True:
        try:
            command = input("\n>> ").strip().lower()
            handle_command(command)
        except Exception as e:
            print(f"Error: {e}")
            print("Type '/help' for available commands.")
