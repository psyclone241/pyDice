#!/usr/bin/env python
import random
import argparse
import inflect

parser = argparse.ArgumentParser(description='Generate a random number from some parameters')
parser.add_argument('-a', action="store", dest="action", default='standard', help="Type of Dice Action, defaults to 'standard'")
parser.add_argument('-t', action="store", dest="type", default='standard', help="Type of Dice, defaults to 'standard'")
parser.add_argument('-x', action="store", dest="highrange", type=int, required=False, help="High Range")
parser.add_argument('-y', action="store", dest="lowrange", type=int, required=False, help="Low Range")
parser.add_argument('-c', action="store", dest="count", type=int, required=False, help="Dice Count")
parser.add_argument('-g', action="store", dest="groups", required=False, help="Groups of Dice, example: 6,4,8")
parser.add_argument('-l', action="store", dest="labels", default='blank', required=False, help="Label your Groups of Dice, example: Six,Four,Eight")

args = parser.parse_args()

dice_action = args.action
dice_type = args.type
low_range = args.highrange
high_range = args.lowrange
dice_count = args.count
dice_groups = args.groups
dice_labels = args.labels

if dice_groups:
    dash = dice_groups.find('-')
    if dash > -1:
        dice_groups = dice_groups.split('-')
        dice_group_type = 'block'
    else:
        dice_groups = dice_groups.split(',')
        dice_group_type = 'list'

if dice_labels:
    dash = dice_labels.find('-')
    comma = dice_labels.find(',')
    if dash > -1:
        dice_labels = dice_labels.split('-')
        dice_label_type = 'block'
    elif comma > -1:
        dice_labels = dice_labels.split(',')
        dice_label_type = 'list'
    else:
        if dice_labels == 'blank':
            dice_label_type = 'blank'
        else:
            dice_labels = None
            dice_label_type = 'default'

if dice_type == 'standard' and (low_range and high_range):
    dice_type = 'custom'

def rollTheDice(low_range, high_range):
    if low_range and high_range:
        if low_range < high_range:
            return random.randint(int(low_range),int(high_range))
        else:
            print('Low range must be lower than high range')
    else:
        print('No range specified')

def diceType(dice_type, low_range=None, high_range=None):
    if dice_type:
        if dice_type == '4':
            return rollTheDice(1,4)
        elif dice_type == 'standard' or dice_type == '6':
            return rollTheDice(1,6)
        elif dice_type == '8':
            return rollTheDice(1,8)
        elif dice_type == '10':
            return rollTheDice(1,10)
        elif dice_type == '12':
            return rollTheDice(1,12)
        elif dice_type == '20':
            return rollTheDice(1,20)
        elif dice_type == 'custom':
            if low_range and high_range:
                return rollTheDice(low_range, high_range)
            else:
                print('Both ranges (high,low) were not specified')
        else:
            print('Dice type specified is not available')
    else:
        print('No dice type specified')

if dice_action == 'standard':
    roll_value = diceType(dice_type, low_range, high_range)
    if roll_value:
        print(roll_value)
elif dice_action == 'group':
    if dice_groups:
        p = inflect.engine()
        if dice_group_type == 'list':
            roll_value = ''
            counter = 0
            for entry in dice_groups:
                entry_string = p.number_to_words(entry)
                dice_groups[counter] = diceType(entry, low_range, high_range)
                label = entry_string.capitalize()
                if dice_labels:
                    if 0 <= counter and counter < len(dice_labels):
                        label = dice_labels[counter]
                if counter > 0:
                    roll_value += ','

                if dice_label_type == 'blank':
                    roll_value += "{}"
                else:
                    roll_value += label + ':' + entry + ':{}'

                counter += 1

            roll_value = roll_value.format(*dice_groups)
            print(roll_value)
        elif dice_group_type == 'block':
            roll_value = ''
            counter = 0
            dice_type = dice_groups[1]
            range_high = (int(dice_groups[0])+1)
            dice_groups = []
            for entry in range(1, range_high):
                entry_string = p.number_to_words(entry)
                dice_groups.insert(counter, diceType(dice_type, low_range, high_range))
                label = entry_string.capitalize()
                if dice_labels:
                    if 0 <= counter and counter < len(dice_labels):
                        label = dice_labels[counter]
                if counter > 0:
                    roll_value += ','

                if dice_label_type == 'blank':
                    roll_value += "{}"
                else:
                    roll_value += label + ':' + dice_type + ':{}'
                counter += 1

            roll_value = roll_value.format(*dice_groups)
            print(roll_value)
    else:
        print('No dice')
