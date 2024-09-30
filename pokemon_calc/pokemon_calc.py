import random

import pokebase as pb

effectiveness = {
    "super_effective": 2,
    "not_very_effective": 0.5,
    "no_effect": 0,
}

type_chart = {
    "normal": {
        "rock": effectiveness["not_very_effective"],
        "ghost": effectiveness["no_effect"],
        "steel": effectiveness["not_very_effective"],
    },
    "fire": {
        "fire": effectiveness["not_very_effective"],
        "water": effectiveness["not_very_effective"],
        "grass": effectiveness["super_effective"],
        "ice": effectiveness["super_effective"],
        "bug": effectiveness["super_effective"],
        "rock": effectiveness["not_very_effective"],
        "dragon": effectiveness["not_very_effective"],
        "steel": effectiveness["super_effective"],
    },
    "water": {
        "fire": effectiveness["super_effective"],
        "water": effectiveness["not_very_effective"],
        "grass": effectiveness["not_very_effective"],
        "ground": effectiveness["super_effective"],
        "rock": effectiveness["super_effective"],
        "dragon": effectiveness["not_very_effective"],
    },
    "grass": {
        "fire": effectiveness["not_very_effective"],
        "water": effectiveness["super_effective"],
        "grass": effectiveness["not_very_effective"],
        "poison": effectiveness["not_very_effective"],
        "ground": effectiveness["super_effective"],
        "flying": effectiveness["not_very_effective"],
        "bug": effectiveness["not_very_effective"],
        "rock": effectiveness["super_effective"],
        "dragon": effectiveness["not_very_effective"],
        "steel": effectiveness["not_very_effective"],
    },
    "electric": {
        "water": effectiveness["super_effective"],
        "grass": effectiveness["not_very_effective"],
        "electric": effectiveness["not_very_effective"],
        "ground": effectiveness["no_effect"],
        "flying": effectiveness["super_effective"],
        "dragon": effectiveness["not_very_effective"],
    },
    "ice": {
        "fire": effectiveness["not_very_effective"],
        "water": effectiveness["not_very_effective"],
        "grass": effectiveness["super_effective"],
        "ice": effectiveness["not_very_effective"],
        "ground": effectiveness["super_effective"],
        "flying": effectiveness["super_effective"],
        "dragon": effectiveness["super_effective"],
        "steel": effectiveness["not_very_effective"],
    },
    "fighting": {
        "normal": effectiveness["super_effective"],
        "ice": effectiveness["super_effective"],
        "rock": effectiveness["super_effective"],
        "dark": effectiveness["super_effective"],
        "steel": effectiveness["super_effective"],
        "poison": effectiveness["not_very_effective"],
        "flying": effectiveness["not_very_effective"],
        "psychic": effectiveness["not_very_effective"],
        "bug": effectiveness["not_very_effective"],
        "fairy": effectiveness["not_very_effective"],
        "ghost": effectiveness["no_effect"],
    },
    "poison": {
        "grass": effectiveness["super_effective"],
        "poison": effectiveness["not_very_effective"],
        "ground": effectiveness["not_very_effective"],
        "rock": effectiveness["not_very_effective"],
        "ghost": effectiveness["not_very_effective"],
        "steel": effectiveness["no_effect"],
        "fairy": effectiveness["super_effective"],
    },
    "ground": {
        "fire": effectiveness["super_effective"],
        "electric": effectiveness["super_effective"],
        "grass": effectiveness["not_very_effective"],
        "ice": effectiveness["not_very_effective"],
        "poison": effectiveness["super_effective"],
        "flying": effectiveness["no_effect"],
        "bug": effectiveness["not_very_effective"],
        "rock": effectiveness["super_effective"],
        "steel": effectiveness["super_effective"],
    },
    "flying": {
        "electric": effectiveness["not_very_effective"],
        "grass": effectiveness["super_effective"],
        "fighting": effectiveness["super_effective"],
        "bug": effectiveness["super_effective"],
        "rock": effectiveness["not_very_effective"],
        "steel": effectiveness["not_very_effective"],
    },
    "psychic": {
        "fighting": effectiveness["super_effective"],
        "poison": effectiveness["super_effective"],
        "psychic": effectiveness["not_very_effective"],
        "dark": effectiveness["no_effect"],
        "steel": effectiveness["not_very_effective"],
    },
    "bug": {
        "fire": effectiveness["not_very_effective"],
        "grass": effectiveness["super_effective"],
        "fighting": effectiveness["not_very_effective"],
        "poison": effectiveness["not_very_effective"],
        "flying": effectiveness["not_very_effective"],
        "psychic": effectiveness["super_effective"],
        "ghost": effectiveness["not_very_effective"],
        "steel": effectiveness["not_very_effective"],
        "fairy": effectiveness["not_very_effective"],
    },
    "rock": {
        "fire": effectiveness["super_effective"],
        "ice": effectiveness["super_effective"],
        "fighting": effectiveness["not_very_effective"],
        "ground": effectiveness["not_very_effective"],
        "flying": effectiveness["super_effective"],
        "bug": effectiveness["super_effective"],
        "steel": effectiveness["not_very_effective"],
    },
    "ghost": {
        "normal": effectiveness["no_effect"],
        "psychic": effectiveness["super_effective"],
        "ghost": effectiveness["super_effective"],
        "dark": effectiveness["not_very_effective"],
    },
    "dragon": {
        "dragon": effectiveness["super_effective"],
        "steel": effectiveness["not_very_effective"],
        "fairy": effectiveness["super_effective"],
    },
    "dark": {
        "fighting": effectiveness["not_very_effective"],
        "psychic": effectiveness["super_effective"],
        "ghost": effectiveness["super_effective"],
        "dark": effectiveness["not_very_effective"],
        "fairy": effectiveness["not_very_effective"],
    },
    "steel": {
        "fire": effectiveness["not_very_effective"],
        "water": effectiveness["not_very_effective"],
        "electric": effectiveness["not_very_effective"],
        "ice": effectiveness["super_effective"],
        "rock": effectiveness["super_effective"],
        "steel": effectiveness["not_very_effective"],
        "fairy": effectiveness["super_effective"],
    },
    "fairy": {
        "fire": effectiveness["not_very_effective"],
        "fighting": effectiveness["super_effective"],
        "poison": effectiveness["not_very_effective"],
        "dragon": effectiveness["super_effective"],
        "dark": effectiveness["super_effective"],
        "steel": effectiveness["not_very_effective"],
    },
}


class pokemon_calc:
    def __init__(
        self, pokemon_attacker, pokemon_defender, level, attack, defence
    ):
        self.pokemon_attacker = pokemon_attacker
        self.pokemon_defender = pokemon_defender

        self.level = level  # attacking pokemons level
        self.attack = attack  # attack stat of attacking pokemons attack
        self.defence = defence  # defence stat of defending pokemon
        self.targets = 1
        self.pb = 1
        self.weather = 1
        self.critical = 1
        self.random = (random.randint(85, 100)) / 100
        self.stab = 1  # same type attack bonus
        self.type_effect = 1

    def get_effectiveness(self, move_type: str):
        multiplier = 1
        defending_pokemon = pb.pokemon(self.pokemon_defender).types

        for types in defending_pokemon:
            defender_type = str(types.type)
            if defender_type in type_chart.get(move_type, {}):

                multiplier *= type_chart[move_type][defender_type]
            else:

                multiplier *= 1
        return multiplier

    def move_damage(self, move):
        move_type = str(pb.move(move).type)
        return self.get_effectiveness(move_type)   

p = pokemon_calc("charizard", "blastoise", 100, 323, 80)
p = p.move_damage("flamethrower")
