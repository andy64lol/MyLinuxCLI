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
    "Bone Sword": {"damage": 7, "speed": 1.0, "price": 50},
    "Iron Sword": {"damage": 10, "speed": 1.0, "price": 80},
    "Steel Sword": {"damage": 15, "speed": 0.9, "price": 150},
    "Flame Sword": {"damage": 20, "speed": 1.1, "price": 300, "effect": "burn"},
    "Ice Sword": {"damage": 18, "speed": 0.8, "price": 300, "effect": "freeze"},
    "Magic Staff": {"damage": 12, "speed": 1.2, "price": 200, "effect": "magic"},
    "Battle Axe": {"damage": 25, "speed": 0.7, "price": 250},
    "Longbow": {"damage": 20, "speed": 1.5, "price": 180},
    "Shortbow": {"damage": 18, "speed": 1.3, "price": 150},
    "Dagger": {"damage": 8, "speed": 1.5, "price": 100},
    "Spear": {"damage": 12, "speed": 1.2, "price": 120},
    "Crossbow": {"damage": 15, "speed": 0.6, "price": 200},
    "Katana": {"damage": 22, "speed": 1.0, "price": 350},
    "Elder Wand": {"damage": 30, "speed": 1.0, "price": 500, "effect": "ultimate"},
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
    },
    "Frostvale": {
        "type": "town",
        "shops": ["Ice Forge", "Potion Shop"],
        "monsters": ["Ice Troll", "Frost Giant"],
        "description": "A snowy town known for its ice magic"
    },
    "Long Shui Zhen (Dragonwater Town)": {
        "type": "city",
        "shops": ["Dragon Market", "Dragon Temple"],
        "monsters": ["Dragon Knight", "Water Elemental"],
        "description": "A bustling city with a rich history of dragon taming"
    },
    "Jade Lotus Village": {
    "type": "town",
    "shops": ["Herbalist", "Tea House", "Charm Shop"],
    "monsters": ["Lotus Spirit", "Pond Serpent"],
    "description": "A tranquil village known for its serene gardens and sacred lotus ponds"
},
"Thundercliff Hold": {
    "type": "dangerous",
    "monsters": ["Storm Elemental", "Rock Wyvern"],
    "description": "A high cliff fortress battered by storms and haunted by sky beasts"
},
"Ember Hollow": {
    "type": "dungeon",
    "monsters": ["Lava Hound", "Molten Wraith"],
    "description": "A volcanic cavern where fire magic pulses through the earth"
},
"Moonveil Harbor": {
    "type": "town",
    "shops": ["Navigator's Guild", "Seafood Market", "Lunar Shrine"],
    "monsters": ["Moonshade Specter", "Sea Serpent"],
    "description": "A mystical harbor town bathed in moonlight and tied to ancient sea legends"
},
"Verdant Spire": {
    "type": "city",
    "shops": ["Elven Boutique", "Sky Garden", "Mystic Archives"],
    "monsters": ["Treant", "Forest Guardian"],
    "description": "A soaring city built into a sacred tree, home to ancient knowledge and nature spirits"
},
"Silent Ashes": {
    "type": "dungeon",
    "monsters": ["Ash Revenant", "Cursed Wanderer"],
    "description": "The ruins of a once-great city buried in ash and echoing with whispers of the past"
}

}

# Character classes
CHARACTER_CLASSES = {
    "Warrior": {"health_bonus": 20, "attack_bonus": 10, "defense_bonus": 15},
    "Mage": {"health_bonus": -10, "attack_bonus": 25, "defense_bonus": 0},
    "Rogue": {"health_bonus": 0, "attack_bonus": 15, "defense_bonus": 5},
    "Paladin": {"health_bonus": 30, "attack_bonus": 15, "defense_bonus": 20},
    "Archer": {"health_bonus": -10, "attack_bonus": 20, "defense_bonus": 5},
    "Berserker": {"health_bonus": 20, "attack_bonus": 30, "defense_bonus": -10},
    "Priest": {"health_bonus": 10, "attack_bonus": 5, "defense_bonus": 10},
    "Assassin": {"health_bonus": -15, "attack_bonus": 35, "defense_bonus": -5},
    "Druid": {"health_bonus": 15, "attack_bonus": 10, "defense_bonus": 15},
    "Samurai": {"health_bonus": 0, "attack_bonus": 20, "defense_bonus": 10},
    "Ninja": {"health_bonus": -5, "attack_bonus": 25, "defense_bonus": 5},
    "Knight": {"health_bonus": 40, "attack_bonus": 10, "defense_bonus": 20},
    "Hunter": {"health_bonus": 0, "attack_bonus": 15, "defense_bonus": 10},
    "Tamer": {"health_bonus": 35, "attack_bonus": 50, "defense_bonus": -25},
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
    "Assassin": ["Shadow Strike", "Vanish", "Death Mark"],
    "Druid": ["Entangle", "Nature's Touch", "Beast Form"],
    "Samurai": ["Iaijutsu Slash", "Bushido Focus", "Wind Cutter"],
    "Ninja": ["Shuriken Toss", "Shadow Clone", "Silent Step"],
    "Knight": ["Shield Bash", "Taunt", "Valor Strike"],
    "Hunter": ["Trap Set", "Beast Call", "Piercing Arrow"],
    "Tamer": ["Summon Beast", "Beast Fury", "Bonded Strike"]

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
    "Steel Ingot": {"areas": ["Blacksmith"], "tool_required": "Furnace"},
    "Gold Ore": {"areas": ["Mountain", "Deep Cave"], "tool_required": "Pickaxe"},
"Magic Crystal": {"areas": ["Crystal Cave", "Ancient Ruins"], "tool_required": "Magic Chisel"},
"Fish": {"areas": ["River", "Lake", "Coast"], "tool_required": "Fishing Rod"},
"Silk Thread": {"areas": ["Forest", "Spider Nest"], "tool_required": "Silk Spinner"},
"Clay": {"areas": ["Riverbank", "Swamp"], "tool_required": "Shovel"},
"Coal": {"areas": ["Mine", "Mountain"], "tool_required": "Pickaxe"},
"Ancient Relic": {"areas": ["Ruins", "Temple"], "tool_required": "Archaeology Kit"},
"Salt": {"areas": ["Cave", "Desert Spring"], "tool_required": "Pickaxe"},
"Venom Sac": {"areas": ["Swamp", "Spider Nest"], "tool_required": "Hunting Knife"},
"Feathers": {"areas": ["Plains", "Cliffside"], "tool_required": "None"}

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
    },
    {
    "id": 3,
    "name": "Howling Threat",
    "description": "Hunt down 5 wolves in the forest",
    "target": {"monster": "Wolf", "count": 5},
    "reward": {"gold": 40, "exp": 90}
    },
    { 
    "id": 4,
    "name": "Skeleton Cleanup",
    "description": "Destroy 4 skeletons near the cemetery",
    "target": {"monster": "Skeleton", "count": 4},
    "reward": {"gold": 60, "exp": 110}
    },
    {
    "id": 5,
    "name": "Ghostly Presence",
    "description": "Banish 3 ghosts from Stormhaven",
    "target": {"monster": "Ghost", "count": 3},
    "reward": {"gold": 70, "exp": 150}
    },
    {
    "id": 6,
    "name": "Troll Trouble",
    "description": "Defeat 2 Cave Trolls",
    "target": {"monster": "Cave Troll", "count": 2},
    "reward": {"gold": 90, "exp": 180}
    },
    {
    "id": 7,
    "name": "Dark Knight Duel",
    "description": "Take down 1 Dark Knight in Shadowmere",
    "target": {"monster": "Dark Knight", "count": 1},
    "reward": {"gold": 120, "exp": 250}
    },
    {
    "id": 8,
    "name": "Fire Dragon Challenge",
    "description": "Defeat the Fire Dragon atop Dragon's Peak",
    "target": {"monster": "Fire Dragon", "count": 1},
    "reward": {"gold": 250, "exp": 400}
    },
    {
    "id": 9,
    "name": "Crystal Golem Rampage",
    "description": "Stop 2 Crystal Golems in Crystal Cave",
    "target": {"monster": "Crystal Golem", "count": 2},
    "reward": {"gold": 100, "exp": 200}
    },
    {
    "id": 10,
    "name": "Ice Troll Hunt",
    "description": "Eliminate 3 Ice Trolls in Frostvale",
    "target": {"monster": "Ice Troll", "count": 3},
    "reward": {"gold": 80, "exp": 170}
    },
    {
    "id": 11,
    "name": "Phoenix Feather",
    "description": "Collect 1 Phoenix Feather from the Silent Ashes",
    "target": {"monster": "Phoenix", "count": 1},
    "reward": {"gold": 300, "exp": 500}
    },
    {
     "id": 12,
     "name": "Water Elemental",
     "description": "Defeat 2 Water Elementals in Long Shui Zhen",
     "target": {"monster": "Water Elemental", "count": 2},
     "reward": {"gold": 110, "exp": 220}
    }   
]

# Available professions with their bonuses
PROFESSIONS = {
    "Miner": {"gather_bonus": ["Iron Ore", "Gold Ore"], "craft_bonus": ["weapons"]},
    "Herbalist": {"gather_bonus": ["Red Herb"], "craft_bonus": ["potions"]},
    "Blacksmith": {"gather_bonus": ["Iron Ore"], "craft_bonus": ["armor"]},
    "Alchemist": {"gather_bonus": ["Red Herb"], "craft_bonus": ["potions"]},
    "Hunter": {"gather_bonus": ["Leather"], "craft_bonus": ["bows"]},
    "Woodcutter": {"gather_bonus": ["Wood"], "craft_bonus": ["staves"]},
    "Fisher": {"gather_bonus": ["Fish"], "craft_bonus": ["fishing gear"]},
    "Archaeologist": {"gather_bonus": ["Ancient Relic"], "craft_bonus": ["artifacts"]},
    "Enchanter": {"gather_bonus": ["Magic Crystal"], "craft_bonus": ["enchanted items"]},
}

# Initialize user data with proper typing
user_data: Dict = {
    "class": None,
    "profession": None,
    "has_chosen_profession": False,
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
    "current_area": "Greenwood Village"
}

# Shop items
shop_items = [
    # === Basic Equipment ===
    {"name": "Wooden Sword", "type": "weapon", "effect": 5, "price": 30},
    {"name": "Iron Sword", "type": "weapon", "effect": 10, "price": 80},
    {"name": "Steel Sword", "type": "weapon", "effect": 15, "price": 150},
    {"name": "Bone Armor", "type": "armor", "effect": 5, "price": 40},
    {"name": "Iron Armor", "type": "armor", "effect": 10, "price": 100},
    {"name": "Steel Armor", "type": "armor", "effect": 15, "price": 180},
    {"name": "Bronze Dagger", "type": "weapon", "effect": 7, "price": 50},
    {"name": "Chainmail", "type": "armor", "effect": 8, "price": 75},
    
    # === Consumables ===
    {"name": "Healing Potion", "type": "consumable", "effect": 30, "price": 20},
    {"name": "Greater Healing Potion", "type": "consumable", "effect": 60, "price": 50},
    {"name": "Antidote", "type": "consumable", "effect": "cure_poison", "price": 25},
    {"name": "Mega Healing Potion", "type": "consumable", "effect": 60, "price": 50},
    {"name": "Mana Potion", "type": "consumable", "effect": 40, "price": 35},
    {"name": "Stamina Elixir", "type": "consumable", "effect": "restore_stamina", "price": 30},
    {"name": "Revival Herb", "type": "consumable", "effect": "revive", "price": 100},
    {"name": "Energy Drink", "type": "consumable", "effect": 25, "price": 15},
    
    # === Special Equipment ===
    {"name": "Magic Staff", "type": "weapon", "effect": 12, "price": 200},
    {"name": "Shadow Cloak", "type": "armor", "effect": 8, "price": 90},
    {"name": "Flame Dagger", "type": "weapon", "effect": 12, "price": 130},
    {"name": "Leather Armor", "type": "armor", "effect": 7, "price": 70},
    {"name": "Bow of the Eagle", "type": "weapon", "effect": 14, "price": 160},
    {"name": "Throwing Knife", "type": "weapon", "effect": 6, "price": 45},
    {"name": "Obsidian Greatsword", "type": "weapon", "effect": 18, "price": 220},
    {"name": "Dragonhide Vest", "type": "armor", "effect": 12, "price": 150},
    {"name": "Silver Rapier", "type": "weapon", "effect": 16, "price": 190},
    {"name": "Enchanted Robes", "type": "armor", "effect": 10, "price": 120},
    {"name": "Crossbow", "type": "weapon", "effect": 13, "price": 140},
    {"name": "Tower Shield", "type": "armor", "effect": 14, "price": 170},

    # === Exotic Equipment === 
    {"name": "Vorpal Blade", "type": "weapon", "effect": 25, "price": 500, "special": "Ignores armor"},
    {"name": "Phoenix Plate", "type": "armor", "effect": 20, "price": 600, "special": "Self-repair over time"},
    {"name": "Elder Wand", "type": "weapon", "effect": 30, "price": 800, "special": "Chance to cast spells for free"},
    {"name": "Cloak of Invisibility", "type": "armor", "effect": 15, "price": 700, "special": "Temporary stealth on use"},
    {"name": "Mjolnir", "type": "weapon", "effect": 35, "price": 1000, "special": "Lightning strikes on critical hits"},
    {"name": "Aegis of the Gods", "type": "armor", "effect": 25, "price": 900, "special": "Blocks all critical hits"},
    
    # === More Exotic Items from Monster Drops ===
    {"name": "Crimson Cutlass", "type": "weapon", "effect": 28, "price": 750, "special": "Bleeds enemies over time", "source": "Dreadlord Varkhull"},
    {"name": "Dragon Armor", "type": "armor", "effect": 22, "price": 850, "special": "Resistant to fire/ice/lightning", "source": "Dragon Knight"},
    {"name": "Undead Blade", "type": "weapon", "effect": 30, "price": 900, "special": "Life steal (10% of damage)", "source": "Undead Knight"},
    {"name": "Jade Crown", "type": "armor", "effect": 25, "price": 1200, "special": "+20% max HP", "source": "Jade Emperor"},
    {"name": "Shadow Blade", "type": "weapon", "effect": 32, "price": 950, "special": "Critical hits deal 3x damage", "source": "Shadow Samurai"},
    {"name": "Phoenix Feather", "type": "consumable", "effect": "full_revive", "price": 800, "special": "Revives with full HP", "source": "Phoenix"},
    {"name": "Cursed Katana", "type": "weapon", "effect": 40, "price": 1500, "special": "Deals self-damage (5% per hit)", "source": "Possessed Katana"},
    {"name": "Samurai Armor", "type": "armor", "effect": 30, "price": 1300, "special": "Counterattacks when hit", "source": "The Shogun"},
    {"name": "Kitsune Mask", "type": "armor", "effect": 18, "price": 700, "special": "Illusionary clones confuse enemies", "source": "Kitsune Warrior"},
    {"name": "Storm Eye", "type": "consumable", "effect": "summon_storm", "price": 600, "special": "Calls lightning on enemies (3 uses)", "source": "Vision of the Thunder"},
    {"name": "Frozen Soul", "type": "consumable", "effect": "freeze_enemies", "price": 500, "special": "Freezes all enemies for 1 turn", "source": "Hatred frozen soul"},
]


monsters: List[Dict] = [
    # Greenwood Village Monsters (Level 1-2)
    {"name": "Goblin", "level": 1, "health": 50, "attack": 10, "drops": ["Gold Coin", "Wooden Sword"]},
    {"name": "Wolf", "level": 2, "health": 60, "attack": 12, "drops": ["Wolf Pelt", "Gold Coin"]},
    {"name": "Forest Spider", "level": 1, "health": 45, "attack": 8, "drops": ["Spider Silk", "Gold Coin"]},
    {"name": "Bandit", "level": 2, "health": 65, "attack": 14, "drops": ["Leather Armor", "Gold Coin"]},
    {"name": "Dire Wolf", "level": 2, "health": 70, "attack": 15, "drops": ["Wolf Fang", "Gold Coin"]},
    {"name": "Goblin Shaman", "level": 2, "health": 55, "attack": 13, "drops": ["Goblin Staff", "Gold Coin"]},

    # Stormhaven Monsters (Level 2-3)
    {"name": "Skeleton", "level": 2, "health": 75, "attack": 15, "drops": ["Gold Coin", "Bone Armor"]},
    {"name": "Ghost", "level": 3, "health": 70, "attack": 18, "drops": ["Spirit Essence", "Gold Coin"]},
    {"name": "Storm Elemental", "level": 3, "health": 85, "attack": 20, "drops": ["Storm Crystal", "Gold Coin"]},
    {"name": "Pirate Scout", "level": 2, "health": 70, "attack": 16, "drops": ["Cutlass", "Gold Coin"]},
    {"name": "Haunted Armor", "level": 3, "health": 80, "attack": 22, "drops": ["Cursed Shield", "Gold Coin"]},
    {"name": "Sea Serpent", "level": 3, "health": 90, "attack": 25, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Dreadlord Varkhull, the Crimson Abyss Pirate Captain", "level": 5, "health": 150, "attack": 30, "drops": ["Crimson Cutlass", "Gold Coin"]},

    # Dragon's Peak Monsters (Level 5-6)
    {"name": "Fire Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Flame Sword"]},
    {"name": "Ice Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Ice Sword"]},
    {"name": "Electrical Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Lightning Sword"]},
    {"name": "Plant Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Nature Sword"]},
    {"name": "Earth Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Earth Sword"]},
    {"name": "Wind Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Wind Sword"]},
    {"name": "Water Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Water Sword"]},
    {"name": "Fire Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ice Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Earth Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Dragon Knight", "level": 5, "health": 150, "attack": 28, "drops": ["Dragon Armor", "Gold Coin"]},
    {"name": "Water Wyvern", "level": 5, "health": 160, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"]},

    # Crystal Cave Monsters (Level 3-4)
    {"name": "Crystal Golem", "level": 4, "health": 120, "attack": 25, "drops": ["Crystal Shard", "Gold Coin"]},
    {"name": "Cave Troll", "level": 4, "health": 130, "attack": 28, "drops": ["Troll Hide", "Gold Coin"]},
    {"name": "Crystal Spider", "level": 3, "health": 90, "attack": 22, "drops": ["Crystal Web", "Gold Coin"]},
    {"name": "Rock Elemental", "level": 4, "health": 140, "attack": 26, "drops": ["Earth Stone", "Gold Coin"]},
    {"name": "Cave Bat", "level": 3, "health": 80, "attack": 20, "drops": ["Bat Wing", "Gold Coin"]},
    {"name": "Crystal Tarantula", "level": 4, "health": 110, "attack": 24, "drops": ["Crystal Fang", "Gold Coin"]},
    {"name": "Crystal Giant Tarantula", "level": 7, "health": 200, "attack": 40, "drops": ["Crystal Eye", "Gold Coin"]},
    {"name": "Crystal Serpent", "level": 4, "health": 110, "attack": 24, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Corrupted Miner", "level": 4, "health": 115, "attack": 25, "drops": ["Miner's Pickaxe", "Gold Coin"]},

    # Shadowmere Monsters (Level 4-5)
    {"name": "Shadow Beast", "level": 4, "health": 110, "attack": 24, "drops": ["Shadow Essence", "Gold Coin"]},
    {"name": "Dark Knight", "level": 5, "health": 140, "attack": 28, "drops": ["Dark Armor", "Gold Coin"]},
    {"name": "Wraith", "level": 5, "health": 120, "attack": 30, "drops": ["Soul Gem", "Gold Coin"]},
    {"name": "Night Stalker", "level": 4, "health": 100, "attack": 26, "drops": ["Night Blade", "Gold Coin"]},
    {"name": "Shadow Assassin", "level": 5, "health": 130, "attack": 32, "drops": ["Assassin's Dagger", "Gold Coin"]},
    {"name": "Vampire", "level": 5, "health": 150, "attack": 35, "drops": ["Vampire Fang", "Gold Coin"]},
    {"name": "Undead Knight", "level": 5, "health": 160, "attack": 38, "drops": ["Undead Blade", "Gold Coin"]},
    {"name": "Undead Army General","level": 7, "health": 200, "attack": 40, "drops": ["Undead Armor", "Gold Coin"]},
    {"name": "Undead Army Commander","level": 8, "health": 250, "attack": 50, "drops": ["Undead's Blade", "Gold Coin"]},

    # Frostvale Monsters (Level 3-4)
    {"name": "Ice Troll", "level": 4, "health": 125, "attack": 26, "drops": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost Giant", "level": 4, "health": 140, "attack": 28, "drops": ["Giant's Club", "Gold Coin"]},
    {"name": "Snow Wolf", "level": 3, "health": 95, "attack": 20, "drops": ["Frost Pelt", "Gold Coin"]},
    {"name": "Ice Elemental", "level": 4, "health": 115, "attack": 24, "drops": ["Ice Crystal", "Gold Coin"]},
    {"name": "Frost Wraith", "level": 4, "health": 130, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"]},
    {"name": "Hatred frozen soul", "level": 5, "health": 150, "attack": 35, "drops": ["Frozen Soul", "Gold Coin"]},
    {"name": "Ice Revenant", "level": 5, "health": 160, "attack": 32, "drops": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost vengeful eye of the snow", "level": 7, "health": 200, "attack": 40, "drops": ["Frost Eye", "Gold Coin"]},

    # Long Shui Zhen Monsters (Level 4-8)
    {"name": "Dragon Spirit", "level": 5, "health": 130, "attack": 28, "drops": ["Spirit Pearl", "Gold Coin"]},
    {"name": "Water Elemental", "level": 4, "health": 110, "attack": 24, "drops": ["Water Essence", "Gold Coin"]},
    {"name": "Jade Warrior", "level": 5, "health": 140, "attack": 26, "drops": ["Jade Sword", "Gold Coin"]},
    {"name": "Jade General", "level": 5, "health": 150, "attack": 30, "drops": ["Jade Armor", "Gold Coin"]},
    {"name": "Jade soldier", "level": 4, "health": 120, "attack": 22, "drops": ["Jade Shield", "Gold Coin"]},
    {"name": "Jade Emperor's Guard", "level": 6, "health": 160, "attack": 32, "drops": ["Jade Shield", "Gold Coin"]},
    {"name": "Jade Emperor", "level": 8, "health": 390, "attack": 65, "drops": ["Jade Crown", "Gold Coin"]},

    # Jade Lotus Village Monsters (Level 2-3)
    {"name": "Lotus Spirit", "level": 3, "health": 85, "attack": 18, "drops": ["Lotus Petal", "Gold Coin"]},
    {"name": "Pond Serpent", "level": 2, "health": 70, "attack": 16, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Garden Guardian", "level": 3, "health": 90, "attack": 20, "drops": ["Sacred Charm", "Gold Coin"]},
    {"name": "Lotus Guardian", "level": 3, "health": 95, "attack": 22, "drops": ["Lotus Shield", "Gold Coin"]},
    {"name": "Koi Empress", "level": 3, "health": 100, "attack": 24, "drops": ["Koi Scale", "Gold Coin"]},

    # Silent Ashes Monsters (Level 5-6)
    {"name": "Ash Revenant", "level": 6, "health": 160, "attack": 32, "drops": ["Revenant Ash", "Gold Coin"]},
    {"name": "Cursed Wanderer", "level": 5, "health": 140, "attack": 28, "drops": ["Cursed Relic", "Gold Coin"]},
    {"name": "Phoenix", "level": 6, "health": 180, "attack": 34, "drops": ["Phoenix Feather", "Gold Coin"]},
    {"name": "Ash Wraith", "level": 5, "health": 150, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"]},
    {"name": "Burnt Guardian", "level": 5, "health": 145, "attack": 29, "drops": ["Guardian's Ash", "Gold Coin"]},
    {"name": "Magmatic Knight,The fallen knight of the ashes", "level": 6, "health": 200, "attack": 40, "drops": ["Knight's Ash", "Gold Coin"]},

    # Thundercliff Hold Monsters (Level 4-5)
    {"name": "Thunder Elemental", "level": 5, "health": 130, "attack": 28, "drops": ["Storm Crystal", "Gold Coin"]},
    {"name": "Rock Wyvern", "level": 4, "health": 120, "attack": 26, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Storm Hawk", "level": 4, "health": 110, "attack": 24, "drops": ["Hawk Feather", "Gold Coin"]},
    {"name": "Storm Wyvern", "level": 5, "health": 140, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Thunder Mage", "level": 5, "health": 150, "attack": 32, "drops": ["Thunder Staff", "Gold Coin"]},
    {"name": "Storm Guardian", "level": 5, "health": 160, "attack": 34, "drops": ["Guardian's Storm", "Gold Coin"]},
    {"name": "Vision of the Thunder,the core of the storm", "level": 5, "health": 150, "attack": 32, "drops": ["Storm Eye", "Gold Coin"]},

    # Shogunate Of Shirui Monsters (Level 5-9)
    {"name": "The Shogun", "level": 9, "health": 400, "attack": 70, "drops": ["Samurai Armor", "Gold Coin"]},
    {"name": "Shogun's Guard", "level": 8, "health": 350, "attack": 60, "drops": ["Shogun's Blade", "Gold Coin"]},
    {"name": "Jade Samurai", "level": 7, "health": 300, "attack": 50, "drops": ["Jade Armor", "Gold Coin"]},
    {"name": "Kitsune Warrior", "level": 6, "health": 250, "attack": 40, "drops": ["Kitsune Mask", "Gold Coin"]},
    {"name": "Tengu Warrior", "level": 6, "health": 240, "attack": 38, "drops": ["Tengu Feather", "Gold Coin"]},
    {"name": "Kappa Guardian", "level": 5, "health": 220, "attack": 35, "drops": ["Kappa Shell", "Gold Coin"]},
    {"name": "Oni Berserker", "level": 7, "health": 280, "attack": 45, "drops": ["Oni Mask", "Gold Coin"]},
    {"name": "Corrupted Ninja", "level": 5, "health": 200, "attack": 30, "drops": ["Ninja Star", "Gold Coin"]},
    {"name": "Shadow Samurai", "level": 6, "health": 260, "attack": 42, "drops": ["Shadow Blade", "Gold Coin"]},
    {"name": "Possessed Katana", "level": 5, "health": 210, "attack": 36, "drops": ["Cursed Katana", "Gold Coin"]},
]


# Dungeons with monsters and loot
dungeons: List[Dict] = [
    # Greenwood Village Dungeons
    {"name": "Goblin's Hideout", "monsters": ["Goblin", "Wolf"], "loot": ["Wooden Sword", "Wolf Pelt", "Gold Coin"]},
    {"name": "Bandit Camp", "monsters": ["Bandit"], "loot": ["Leather Armor", "Gold Coin"]},
    {"name": "Forest Spider Den", "monsters": ["Forest Spider"], "loot": ["Spider Silk", "Gold Coin"]},
    {"name": "Ancient Ruins", "monsters": ["Forest Spider", "Goblin"], "loot": ["Ancient Relic", "Gold Coin"]},
    {"name": "Goblin Fortress", "monsters": ["Goblin", "Dire Wolf"], "loot": ["Goblin Staff", "Gold Coin"]},
    {"name": "Cave of Shadows", "monsters": ["Goblin Shaman"], "loot": ["Gold Coin", "Goblin Staff"]},
    
    # Stormhaven Dungeons
    {"name": "Haunted Crypt", "monsters": ["Skeleton", "Ghost"], "loot": ["Bone Armor", "Spirit Essence", "Gold Coin"]},
    {"name": "Pirate's Cove", "monsters": ["Pirate Scout"], "loot": ["Cutlass", "Gold Coin"]},
    {"name": "Storm Fortress", "monsters": ["Storm Elemental"], "loot": ["Storm Crystal", "Gold Coin"]},
    {"name": "Cursed Shipwreck", "monsters": ["Haunted Armor"], "loot": ["Cursed Shield", "Gold Coin"]},
    {"name": "Ghost Ship", "monsters": ["Sea Serpent"], "loot": ["Serpent Scale", "Gold Coin"]},
    {"name": "Dreadlord's Sunken Ship", "monsters": ["Dreadlord Varkhull, the Crimson Abyss Pirate Captain"], "loot": ["Crimson Cutlass", "Gold Coin"]},
    {"name": "Cursed Lighthouse", "monsters": ["Haunted Armor", "Ghost"], "loot": ["Cursed Shield", "Gold Coin"]},
    {"name": "Cursed Graveyard", "monsters": ["Skeleton", "Ghost"], "loot": ["Bone Armor", "Spirit Essence", "Gold Coin"]},
    
    # Dragon's Peak Dungeons
    {"name": "Fire Dragon's Lair", "monsters": ["Fire Dragon"], "loot": ["Dragon Scale", "Flame Sword", "Gold Coin"]},
    {"name": "Ice Dragon's Nest", "monsters": ["Ice Dragon"], "loot": ["Dragon Scale", "Ice Sword", "Gold Coin"]},
    {"name": "Electrical Dragon's Roost", "monsters": ["Electrical Dragon"], "loot": ["Dragon Scale", "Lightning Sword", "Gold Coin"]},
    {"name": "Plant Dragon's Grove", "monsters": ["Plant Dragon"], "loot": ["Dragon Scale", "Nature Sword", "Gold Coin"]},
    {"name": "Earth Dragon's Cavern", "monsters": ["Earth Dragon"], "loot": ["Dragon Scale", "Earth Sword", "Gold Coin"]},
    {"name": "Wind Dragon's Summit", "monsters": ["Wind Dragon"], "loot": ["Dragon Scale", "Wind Sword", "Gold Coin"]},
    {"name": "Water Dragon's Abyss", "monsters": ["Water Dragon"], "loot": ["Dragon Scale", "Water Sword", "Gold Coin"]},
    {"name": "Fire Wyvern Nest", "monsters": ["Fire Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ice Wyvern Cave", "monsters": ["Ice Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Wyvern Peak", "monsters": ["Thunder Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Earth Wyvern Den", "monsters": ["Earth Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Dragon Knight's Fortress", "monsters": ["Dragon Knight"], "loot": ["Dragon Armor", "Gold Coin"]},
    {"name": "Water Wyvern Lagoon", "monsters": ["Water Wyvern"], "loot": ["Wyvern Wing", "Gold Coin"]},
    
    # Crystal Cave Dungeons
    {"name": "Crystal Depths", "monsters": ["Crystal Golem", "Cave Troll"], "loot": ["Crystal Shard", "Troll Hide", "Gold Coin"]},
    {"name": "Cave of Echoes", "monsters": ["Crystal Spider", "Rock Elemental"], "loot": ["Crystal Web", "Earth Stone", "Gold Coin"]},
    {"name": "Crystal Cavern", "monsters": ["Cave Bat", "Crystal Tarantula"], "loot": ["Bat Wing", "Crystal Fang", "Gold Coin"]},
    {"name": "Crystal Golem's Lair", "monsters": ["Crystal Giant Tarantula"], "loot": ["Crystal Eye", "Gold Coin"]},
    {"name": "Serpent's Lair", "monsters": ["Crystal Serpent"], "loot": ["Serpent Scale", "Gold Coin"]},
    {"name": "Corrupted Miner's Hideout", "monsters": ["Corrupted Miner"], "loot": ["Miner's Pickaxe", "Gold Coin"]},
    {"name": "Crystal Cavern", "monsters": ["Crystal Golem", "Cave Troll"], "loot": ["Crystal Shard", "Troll Hide", "Gold Coin"]},
    
    # Shadowmere Dungeons
    {"name": "Shadow Keep", "monsters": ["Shadow Beast", "Dark Knight"], "loot": ["Shadow Essence", "Dark Armor", "Gold Coin"]},
    {"name": "Wraith's Lair", "monsters": ["Wraith"], "loot": ["Soul Gem", "Gold Coin"]},
    {"name": "Night Stalker Den", "monsters": ["Night Stalker"], "loot": ["Night Blade", "Gold Coin"]},
    {"name": "Assassin's Hideout", "monsters": ["Shadow Assassin"], "loot": ["Assassin's Dagger", "Gold Coin"]},
    {"name": "Dark Fortress", "monsters": ["Dark Knight"], "loot": ["Dark Armor", "Gold Coin"]},
    {"name": "Vampire's Crypt", "monsters": ["Vampire"], "loot": ["Vampire Fang", "Gold Coin"]},
    {"name": "Undead Fortress", "monsters": ["Undead Knight"], "loot": ["Undead Blade", "Gold Coin"]},
    {"name": "Undead Army Base", "monsters": ["Undead Army General","Undead Army Commander"], "loot": ["Undead Armor", "Gold Coin"]},
    
    # Frostvale Dungeons
    {"name": "Frozen Halls", "monsters": ["Ice Troll", "Frost Giant"], "loot": ["Frozen Heart", "Giant's Club", "Gold Coin"]},
    {"name": "Snowy Cavern", "monsters": ["Snow Wolf", "Ice Elemental"], "loot": ["Frost Pelt", "Ice Crystal", "Gold Coin"]},
    {"name": "Frost Wraith's Lair", "monsters": ["Frost Wraith"], "loot": ["Wraith Essence", "Gold Coin"]},
    {"name": "Troll's Den", "monsters": ["Ice Troll"], "loot": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost Revenant", "monsters": ["Ice Revenant"], "loot": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frozen Eye Cave", "monsters": ["Frost vengeful eye of the snow"], "loot": ["Frost Eye", "Gold Coin"]},

    # Silent Ashes Dungeons
    {"name": "Ash Ruins", "monsters": ["Ash Revenant", "Cursed Wanderer"], "loot": ["Ancient Relic", "Cursed Gem", "Gold Coin"]},
    {"name": "Phoenix Nest", "monsters": ["Phoenix"], "loot": ["Phoenix Feather", "Gold Coin"]},
    {"name": "Ash Wraith's Den", "monsters": ["Ash Wraith"], "loot": ["Wraith Essence", "Gold Coin"]},
    {"name": "Guardian's Ash Fortress", "monsters": ["Burnt Guardian"], "loot": ["Guardian's Ash", "Gold Coin"]},
    {"name": "Magmatic Knight's Lair", "monsters": ["Magmatic Knight,The fallen knight of the ashes"], "loot": ["Knight's Ash", "Gold Coin"]},
    {"name": "Vision of the Thunder Cave", "monsters": ["Vision of the Thunder,the core of the storm"], "loot": ["Storm Eye", "Gold Coin"]},

    # Long Shui Zhen Dungeons
    {"name": "Water Palace", "monsters": ["Water Elemental", "Jade Warrior"], "loot": ["Water Essence", "Jade Sword", "Gold Coin"]},
    {"name": "Dragon Temple", "monsters": ["Dragon Spirit"], "loot": ["Spirit Pearl", "Gold Coin"]},
    {"name": "Jade General's Fortress", "monsters": ["Jade General","Jade Soldier"], "loot": ["Jade Armor", "Gold Coin"]},
    {"name": "Jade Emperor's Chamber", "monsters": ["Jade Emperor", "Jade Emperor's Guard"], "loot": ["Jade Crown", "Gold Coin"]},

    # Jade Lotus Village Dungeons
    {"name": "Lotus Sanctuary", "monsters": ["Lotus Spirit", "Pond Serpent"], "loot": ["Lotus Petal", "Serpent Scale", "Gold Coin"]},
    {"name": "Garden of Spirits", "monsters": ["Garden Guardian"], "loot": ["Sacred Charm", "Gold Coin"]},
    {"name": "Lotus Shrine", "monsters": ["Lotus Guardian"], "loot": ["Lotus Shield", "Gold Coin"]},
    {"name": "Koi Pond", "monsters": ["Koi Empress"], "loot": ["Koi Scale", "Gold Coin"]},

    # Thundercliff Hold Dungeons
    {"name": "Storm Fortress", "monsters": ["Thunder Elemental", "Rock Wyvern"], "loot": ["Storm Crystal", "Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Mage's Tower", "monsters": ["Thunder Mage"], "loot": ["Thunder Staff", "Gold Coin"]},
    {"name": "Storm Wyvern Nest", "monsters": ["Storm Wyvern"], "loot": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Storm Guardian's Keep", "monsters": ["Storm Guardian"], "loot": ["Guardian's Storm", "Gold Coin"]},

    # Ember Hollow Dungeons
    {"name": "Lava Cavern", "monsters": ["Lava Hound", "Molten Wraith"], "loot": ["Lava Stone", "Gold Coin"]},
    {"name": "Ember Fortress", "monsters": ["Fire Elemental"], "loot": ["Ember Crystal", "Gold Coin"]},
    {"name": "Ashen Ruins", "monsters": ["Ash Elemental"], "loot": ["Ashen Gem", "Gold Coin"]},
    {"name": "Fire Wyvern Nest", "monsters": ["Fire Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ember Dragon's Lair", "monsters": ["Ember Dragon"], "loot": ["Dragon Scale", "Gold Coin"]},

    # Shogunate Of Shirui Dungeons
    {"name": "Shogun's Fortress", "monsters": ["The Shogun", "Shogun's Guard"], "loot": ["Samurai Armor", "Shogun's Blade", "Gold Coin"]},
    {"name": "Kitsune Shrine", "monsters": ["Kitsune Warrior"], "loot": ["Kitsune Mask", "Gold Coin"]},
    {"name": "Jade Temple", "monsters": ["Jade Samurai"], "loot": ["Jade Armor", "Gold Coin"]},
    {"name": "Tengu's Nest", "monsters": ["Tengu Warrior"], "loot": ["Tengu Feather", "Gold Coin"]},
    {"name": "Kappa's Cave", "monsters": ["Kappa Guardian"], "loot": ["Kappa Shell", "Gold Coin"]},
    {"name": "Oni's Lair", "monsters": ["Oni Berserker"], "loot": ["Oni Mask", "Gold Coin"]},
    {"name": "Corrupted Ninja's Hideout", "monsters": ["Corrupted Ninja"], "loot": ["Ninja Star", "Gold Coin"]},
    {"name": "Shadow Samurai's Fortress", "monsters": ["Shadow Samurai"], "loot": ["Shadow Blade", "Gold Coin"]},
    {"name": "Possessed Katana's Lair", "monsters": ["Possessed Katana"], "loot": ["Cursed Katana", "Gold Coin"]},
]

# Function to display headers
def print_header(title: str) -> None:
    print("\n" + "=" * 40)
    print(f"{title}")
    print("=" * 40)

# Show the help menu
def show_help() -> None:
    print("""
TEXTRP CLI - COMMANDS

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
        "/search": search_resources,
        "/location_check": check_location,
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
        with open("savegame.json", "r", encoding='utf-8') as f:
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
    if user_data["class"] is not None:
        print("You have already created a character!")
        return
        
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
    {"name": "Riverbend", "population": 120, "special_items": ["Fishing Rod", "Water Flask"]},
    {"name": "Snowpeak", "population": 80, "special_items": ["Warm Cloak", "Ice Pick"]},
    {"name": "Emberfall", "population": 100, "special_items": ["Firestarter", "Lava Stone"]},
    {"name": "Thundercliff", "population": 90, "special_items": ["Lightning Rod", "Storm Cloak"]},
    {"name": "Jade Lotus", "population": 110, "special_items": ["Lotus Blossom", "Jade Pendant"]},
    {"name": "Shogunate of Shirui", "population": 130, "special_items": ["Samurai Armor", "Katana"]},
    {"name": "Long Shui Zhen", "population": 140, "special_items": ["Dragon Scale", "Water Orb"]},
]

# Sample biomes (added for completeness)
biomes = [
{
   "name":"Forest",
   "description":"A lush green area filled with trees and wildlife."
},
{
   "name":"Desert",
   "description":"A vast sandy area with scarce resources."
},
{
   "name":"Cave",
   "description":"A dark underground area with hidden treasures."
},
{
   "name":"Snowy Peaks",
   "description":"A cold mountainous region with snow-covered terrain."
},
{
   "name":"Volcanic Region",
   "description":"A hot area with lava flows and volcanic activity."
},
{
   "name":"Swamp",
   "description":"A murky area filled with water and strange creatures."
},
{
   "name":"Ocean",
   "description":"A vast body of water with islands and sea monsters."
},
{
   "name":"Sky Islands",
   "description":"Floating islands high in the sky, accessible by air."
},
{
   "name":"Crystal Caverns",
   "description":"A cave filled with sparkling crystals and rare minerals."
},
{
   "name":"Jungle",
   "description":"A dense and tropical area filled with towering trees, exotic plants, and wild animals."
},
{
   "name":"Tundra",
   "description":"A cold, barren landscape with little vegetation, covered in permafrost and snow."
},
{
   "name":"Savannah",
   "description":"A vast grassy plain with scattered trees, home to many herds of animals."
},
{
   "name":"Fungal Forest",
   "description":"A damp, dark forest where giant fungi dominate the landscape instead of trees."
},
{
   "name":"Mountain Range",
   "description":"A towering series of mountains, often with dangerous cliffs and peaks, and home to hardy creatures."
},
{
   "name":"Rainforest",
   "description":"A hot, humid area with dense foliage, continuous rainfall, and diverse wildlife."
},
{
   "name":"Barren Wasteland",
   "description":"An empty, desolate region with little to no life, plagued by sandstorms and harsh winds."
},
{
   "name":"Underwater Ruins",
   "description":"Sunken cities and forgotten structures beneath the ocean, filled with ancient artifacts and dangers."
},
{
   "name":"Meadow",
   "description":"A peaceful, open field filled with colorful flowers, tall grasses, and peaceful wildlife."
},
{
   "name":"Mystic Forest",
   "description":"A magical forest filled with glowing plants, enchanted creatures, and hidden secrets."
},
{
   "name":"Twilight Grove",
   "description":"A mysterious forest where the sun never fully sets, creating a perpetual twilight with bioluminescent plants and glowing creatures."
},
{
   "name":"Corrupted Land",
   "description":"A dark and twisted environment where the very soil is tainted, giving rise to dangerous, mutated creatures and toxic flora."
},
{
   "name":"Icy Wastes",
   "description":"A barren, freezing expanse filled with endless ice fields, glaciers, and the occasional frozen lake hiding ancient secrets."
},
{
   "name":"Oasis",
   "description":"A rare, fertile area in the desert, featuring a small pool of water surrounded by palm trees and desert wildlife."
},
{
   "name":"Lush Highlands",
   "description":"A rolling green landscape with gentle hills, fertile soil, and peaceful wildlife, perfect for farming or settling."
},
{
   "name":"Boreal Forest",
   "description":"A cold and dense forest filled with evergreens and snow, inhabited by resilient wildlife adapted to the harsh conditions."
},
{
   "name":"Sunken Abyss",
   "description":"An underwater trench deep in the ocean, home to strange abyssal creatures and ancient, sunken ruins."
},
{
   "name":"Shroom Cavern",
   "description":"A vast underground network filled with towering mushrooms, glowing spores, and rare fungal lifeforms."
},
{
   "name":"Frostbitten Tundra",
   "description":"An arctic wasteland where the air is frozen, and snowstorms are a constant threat, with dangerous wildlife adapted to the extreme cold."
},
{
   "name":"Radiant Plains",
   "description":"A glowing meadow where flowers and grasses emit light, creating a serene and ethereal landscape filled with beauty and tranquility."
},
{
   "name":"Ashen Wastes",
   "description":"A scorched, desolate plain left behind by ancient fires, where the ground is cracked, and the air is thick with ash and smoke."
},
{
   "name":"Celestial Peaks",
   "description":"Towering mountain ranges that reach beyond the clouds, where the air is thin, and the environment is home to rare celestial beings."
},
{
   "name":"Mystic Marsh",
   "description":"A foggy and swampy area filled with enchanted waters, strange will-o'-the-wisps, and ancient trees with whispered secrets."
},
{
   "name":"Crystal Fields",
   "description":"Vast plains where the earth itself is covered with shimmering crystals, creating a dazzling landscape that’s both beautiful and treacherous."
},
{
   "name":"Vibrant Reef",
   "description":"A colorful underwater biome teeming with vibrant corals, exotic fish, and rare underwater plants, but also home to deadly sea predators."
},
{
   "name":"Sandstorm Flats",
   "description":"A vast desert landscape constantly ravaged by powerful sandstorms, leaving only remnants of ancient structures buried beneath the dunes."
},
{
   "name":"The Nether",
   "description":"A fiery, chaotic dimension filled with volcanic terrain, strange creatures, and hostile environments, with a constant threat of fire and lava."
},
{
   "name":"Skyward Cavern",
   "description":"A network of caves suspended in the sky, connected by floating platforms and filled with rare ores and aerial creatures."
}


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

def check_location() -> None:
    print_header("Location Information")
    current = user_data["current_area"]
    
    print("Current Location:", current)
    if current in LOCATIONS:
        loc_info = LOCATIONS[current]
        print(f"\nType: {loc_info['type']}")
        print(f"Description: {loc_info['description']}")
        if 'shops' in loc_info:
            print(f"Available Shops: {', '.join(loc_info['shops'])}")
        if 'monsters' in loc_info:
            print(f"Local Monsters: {', '.join(loc_info['monsters'])}")
    
    print("\nAll Available Locations:")
    for name, info in LOCATIONS.items():
        print(f"\n{name}:")
        print(f"  Type: {info['type']}")
        print(f"  Description: {info['description']}")
    
    print("\nAvailable Dungeons:")
    for dungeon in dungeons:
        print(f"\n{dungeon['name']}:")
        print(f"  Monsters: {', '.join(dungeon['monsters'])}")
        print(f"  Possible Loot: {', '.join(dungeon['loot'])}")

def search_resources() -> None:
    print_header("Resource Search")
    search_type = random.choice(["monster", "material"])
    
    if search_type == "monster":
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(user_data["current_area"], {}).get("monsters", [])]
        if area_monsters:
            monster = random.choice(area_monsters)
            print(f"You found a {monster['name']}!")
            print(f"Level: {monster['level']}")
            print(f"Health: {monster['health']}")
            print(f"Attack: {monster['attack']}")
            print(f"Possible drops: {', '.join(monster['drops'])}")
        else:
            print("No monsters found in this area.")
    else:
        available_materials = [name for name, info in MATERIALS.items() 
                             if user_data["current_area"] in info["areas"]]
        if available_materials:
            material = random.choice(available_materials)
            tool_required = MATERIALS[material]["tool_required"]
            print(f"You found {material}!")
            if tool_required:
                print(f"Tool required: {tool_required}")
            if tool_required in user_data["tools"]:
                print("You have the right tool to gather this!")
            elif tool_required:
                print("You need the right tool to gather this.")
        else:
            print("No materials found in this area.")

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
    
    if user_data["has_chosen_profession"]:
        print(f"Your current profession: {user_data['profession']}")
        if user_data["profession"] in PROFESSIONS:
            bonuses = PROFESSIONS[user_data["profession"]]
            print("\nProfession bonuses:")
            print(f"Gathering bonus for: {', '.join(bonuses['gather_bonus'])}")
            print(f"Crafting bonus for: {', '.join(bonuses['craft_bonus'])}")
        return
        
    print("Available professions:")
    for prof, bonuses in PROFESSIONS.items():
        print(f"\n{prof}:")
        print(f"  Gathering bonus: {', '.join(bonuses['gather_bonus'])}")
        print(f"  Crafting bonus: {', '.join(bonuses['craft_bonus'])}")
    
    choice = input("\nChoose a profession (or press Enter to skip): ").capitalize()
    if choice in PROFESSIONS:
        user_data["profession"] = choice
        user_data["has_chosen_profession"] = True
        print(f"\nYou are now a {choice}!")
    elif choice:
        print("Invalid profession choice.")
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

