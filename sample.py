#!/usr/bin/env python

from rollme import rollme

app = rollme.rollme()

print('\n')
print('Single 20-sided Die')
print('Returning single value')
app.output = 'return'
print('-----------------------------')
app.dice_action = 'standard'
app.dice_type = '20'
return_value = app.main()
print(return_value)

print('\n')
print('Eight Custom Labeled Dice')
print('Returning an object')
print('-----------------------------')
app.output = 'object'
app.dice_action = 'group'
app.dice_groups = ['4','6','8','10','12','20','6','custom']
app.dice_group_type = 'list'
app.dice_labels = ['four','six','eight','10','twelve','twenty','six','custom']
app.dice_label_type = 'group'
app.low_range = 1
app.high_range = 99
return_value = app.main()
print(return_value)
print('\n')
