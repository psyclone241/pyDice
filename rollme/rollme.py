#!/usr/bin/env python
import random
import argparse
import inflect
import json

class rollmeConfig:
    def __init__(self):
        self.dice_action = None
        self.dice_type = None
        self.low_range = None
        self.high_range = None
        self.custom_config = {}
        self.override_defaults = None
        self.dice_groups = None
        self.dice_labels = None
        self.output = None
        self.dice_group_type = None
        self.dice_label_type = None
        self.default_dice_types = None

class rollme:
    def __init__(self, input_config_object=False):
        if input_config_object:
            self.config_object = rollmeConfig()

            self.config_object.dice_action = input_config_object.dice_action
            self.config_object.dice_type = input_config_object.dice_type
            self.config_object.low_range = input_config_object.high_range
            self.config_object.high_range = input_config_object.low_range
            self.config_object.custom_config = input_config_object.custom_config
            self.config_object.override_defaults = input_config_object.override_defaults
            self.config_object.dice_groups = input_config_object.dice_groups
            self.config_object.dice_labels = input_config_object.dice_labels
            self.config_object.output = input_config_object.output

            self.config_object.dice_group_type = None
            self.config_object.dice_label_type = None
            self.config_object.default_dice_types = {
                '4': { 'low': 1, 'high': 4 },
                '6': { 'low': 1, 'high': 6 },
                '8': { 'low': 1, 'high': 8 },
                '10': { 'low': 1, 'high': 10 },
                '12': { 'low': 1, 'high': 12 },
                '20': { 'low': 1, 'high': 20 },
                'custom': { 'low': self.config_object.low_range, 'high': self.config_object.high_range }
            }
        else:
            parser = argparse.ArgumentParser(description='Generate a random number from some parameters')
            parser.add_argument('-a', action="store", dest="action", default='standard', help="Type of Dice Action, defaults to 'standard'")
            parser.add_argument('-t', action="store", dest="type", default='standard', help="Type of Dice, defaults to 'standard'")
            parser.add_argument('-x', action="store", dest="highrange", type=int, required=False, help="High Range")
            parser.add_argument('-y', action="store", dest="lowrange", type=int, required=False, help="Low Range")
            parser.add_argument('-c', action="store", dest="custom_config", required=False, help="Custom configuration file path")
            parser.add_argument('-z', action="store_true", dest="override_defaults", default=False, required=False, help="Override dice types with custom types")
            parser.add_argument('-g', action="store", dest="groups", required=False, help="Groups of Dice, example: 6,4,8")
            parser.add_argument('-l', action="store", dest="labels", default='', required=False, help="Label your Groups of Dice, example: Six,Four,Eight")
            parser.add_argument('-o', action="store", dest="output", default='print', required=False, help="What kind of output do you want?")

            args = parser.parse_args()

            self.config_object = rollmeConfig()

            self.config_object.dice_action = args.action
            self.config_object.dice_type = args.type
            self.config_object.low_range = args.highrange
            self.config_object.high_range = args.lowrange
            self.config_object.custom_config = args.custom_config
            self.config_object.override_defaults = args.override_defaults
            self.config_object.dice_groups = args.groups
            self.config_object.dice_labels = args.labels
            self.config_object.output = args.output

            self.config_object.dice_group_type = None
            self.config_object.dice_label_type = None
            self.config_object.default_dice_types = {
                '4': { 'low': 1, 'high': 4 },
                '6': { 'low': 1, 'high': 6 },
                '8': { 'low': 1, 'high': 8 },
                '10': { 'low': 1, 'high': 10 },
                '12': { 'low': 1, 'high': 12 },
                '20': { 'low': 1, 'high': 20 },
                'custom': { 'low': self.config_object.low_range, 'high': self.config_object.high_range }
            }

            if self.config_object.dice_groups:
                dash = self.config_object.dice_groups.find('-')
                if dash > -1:
                    self.config_object.dice_groups = self.config_object.dice_groups.split('-')
                    self.config_object.dice_group_type = 'block'
                else:
                    self.config_object.dice_groups = self.config_object.dice_groups.split(',')
                    self.config_object.dice_group_type = 'list'

            if self.config_object.dice_labels:
                dash = self.config_object.dice_labels.find('-')
                comma = self.config_object.dice_labels.find(',')
                if dash > -1:
                    self.config_object.dice_labels = self.config_object.dice_labels.split('-')
                    self.config_object.dice_label_type = 'block'
                elif comma > -1:
                    self.config_object.dice_labels = self.config_object.dice_labels.split(',')
                    self.config_object.dice_label_type = 'list'
                else:
                    if self.config_object.dice_labels == 'blank':
                        self.config_object.dice_label_type = 'blank'
                    else:
                        self.config_object.dice_labels = None
                        self.config_object.dice_label_type = 'default'

            if self.config_object.dice_type == 'standard' and (self.config_object.low_range and self.config_object.high_range):
                self.config_object.dice_type = 'custom'

            if self.config_object.custom_config:
                try:
                    with open(self.config_object.custom_config, 'r') as config_file:
                        self.config_object.custom_config = config_file.read()
                        self.config_object.custom_config = json.loads(self.config_object.custom_config)

                        for custom_dice in self.config_object.custom_config['dice_types']:
                            this_name = custom_dice['name']
                            if this_name in self.config_object.default_dice_types:
                                if self.config_object.override_defaults:
                                    self.config_object.default_dice_types[this_name]['low'] = custom_dice['low']
                                    self.config_object.default_dice_types[this_name]['high'] = custom_dice['high']
                except:
                    self.config_object.custom_config = None
                    pass
    def showConfiguration(self):
        print(self.config_object)

    def makeObject(self, data, is_error):
        break_on_comma = data.split(',')
        counter = 0
        for entry in break_on_comma:
            parts = entry.split(':')

            try:
                value = int(parts[2])
                roll = parts[2]
                error = None
            except:
                roll = None
                error = parts[2]

            new_data = {
                'label': parts[0],
                'type': parts[1],
                'roll': roll,
                'error': error
            }
            break_on_comma[counter] = new_data
            counter += 1

        return break_on_comma

    def makeJson(self, data):
        return json.dumps(data, indent=4)

    def makeOutput(self, value, is_error=False):
        if self.config_object.output == 'print':
            print(value)
        elif self.config_object.output == 'json':
            print(self.makeJson(self.makeObject(value, is_error)))
        elif self.config_object.output == 'object':
            return self.makeObject(value, is_error)
        else:
            return value

    def rollTheDice(self, low_range, high_range):
        if low_range and high_range:
            if low_range < high_range:
                return random.randint(int(low_range),int(high_range))
            else:
                return 'Low range must be lower than high range'
        else:
            return 'No range specified'

    def diceType(self, dice_type='standard', low_range=None, high_range=None):
        if dice_type:
            if dice_type == 'standard':
                dice_type = '6'
            for dice, range_info in self.config_object.default_dice_types.iteritems():
                if dice_type == dice:
                    if dice_type == 'custom':
                        if low_range and high_range:
                            return self.rollTheDice(range_info['low'], range_info['high'])
                        else:
                            return 'Both ranges (high & low) were not specified'
                    else:
                        return self.rollTheDice(range_info['low'], range_info['high'])
                else:
                    if self.config_object.custom_config:
                        if 'dice_types' in self.config_object.custom_config:
                            for custom_dice in self.config_object.custom_config['dice_types']:
                                if 'name' in custom_dice:
                                    custom_name = custom_dice['name']
                                    if custom_name == dice_type:
                                        if 'low' in custom_dice and 'high' in custom_dice:
                                            low = custom_dice['low']
                                            high = custom_dice['high']
                                            if low and low > 0 and high and high > 0:
                                                return self.rollTheDice(low, high)
                                            else:
                                                return 'Missing a low or high for custom dice: ' + custom_name
                                        else:
                                            return 'No low and high for custom dice: ' + custom_name

            return 'Dice type specified is not available'
        else:
            return 'No dice type specified'

    def main(self):
        if self.config_object.dice_action == 'standard':
            roll_value = self.diceType(self.config_object.dice_type, self.config_object.low_range, self.config_object.high_range)
            if roll_value:
                return self.makeOutput(roll_value)
        elif self.config_object.dice_action == 'group':
            if self.config_object.dice_groups:
                p = inflect.engine()
                roll_value = ''
                counter = 0
                if self.config_object.dice_group_type == 'list':
                    for entry in self.config_object.dice_groups:
                        entry_string = p.number_to_words(entry)
                        self.config_object.dice_groups[counter] = self.diceType(entry, self.config_object.low_range, self.config_object.high_range)
                        label = entry_string.capitalize()
                        if self.config_object.dice_labels:
                            if 0 <= counter and counter < len(self.config_object.dice_labels):
                                label = self.config_object.dice_labels[counter]
                        if counter > 0:
                            roll_value += ','

                        if self.config_object.dice_label_type == 'blank':
                            roll_value += "{}"
                        else:
                            roll_value += label + ':' + entry + ':{}'

                        counter += 1

                    roll_value = roll_value.format(*self.config_object.dice_groups)
                    return self.makeOutput(roll_value)
                elif self.config_object.dice_group_type == 'block':
                    dice_type = self.config_object.dice_groups[1]
                    range_high = (int(self.config_object.dice_groups[0])+1)
                    self.config_object.dice_groups = []
                    for entry in range(1, range_high):
                        entry_string = p.number_to_words(entry)
                        self.config_object.dice_groups.insert(counter, self.diceType(dice_type, self.config_object.low_range, self.config_object.high_range))
                        label = entry_string.capitalize()
                        if self.config_object.dice_labels:
                            if 0 <= counter and counter < len(self.config_object.dice_labels):
                                label = self.config_object.dice_labels[counter]
                        if counter > 0:
                            roll_value += ','

                        if self.config_object.dice_label_type == 'blank':
                            roll_value += "{}"
                        else:
                            roll_value += label + ':' + self.dice_type + ':{}'
                        counter += 1

                    roll_value = roll_value.format(*self.config_object.dice_groups)
                    return self.makeOutput(roll_value)
            else:
                return 'No dice'

if __name__ == '__main__':
    myapp = rollme()
    myapp.main()
