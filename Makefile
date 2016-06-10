# Helper script for setting up your apps local instance
# Contributors:
# Roy Keyes <keyes.roy@gmail.com>

help:
	@echo "Available tasks :"
	@echo "\tinstall - Install this app in a virtual environment"
	@echo "\tvenv - Make the virtual environment"
	@echo "\troll4 - Roll a four-sided die"
	@echo "\troll6 - Roll a six-sided die"
	@echo "\troll8 - Roll a eight-sided die"
	@echo "\troll10 - Roll a ten-sided die"
	@echo "\troll12 - Roll a twelve-sided die"
	@echo "\troll20 - Roll a twenty-sided die"
	@echo "\trollcustom - Roll a custom-sided die (X=1 Y=99)"
	@echo "\trollgroup - Roll a group of numbered die (GROUP=4,6,6,8 or GROUP=4-6)"
	@echo "\trollcustomgroup - Roll a group of numbered or custom-sided die (GROUP=4,6,6,custom or GROUP=4-custom with X=1 Y=99)"

install:
	@virtualenv venv
	@venv/bin/pip install -r requirements.txt

venv:
	@virtualenv venv

roll4:
	@python rollme.py -t 4

roll6:
	@python rollme.py -t 6

roll8:
	@python rollme.py -t 8

roll10:
	@python rollme.py -t 10

roll12:
	@python rollme.py -t 12

roll20:
	@python rollme.py -t 20

rollcustom:
	@python rollme.py -t custom -x $$X -y $$Y

rollgroup:
	@python rollme.py -a group -g $$GROUP

rollcustomgroup:
	@python rollme.py -a group -g $$GROUP -x $$X -y $$Y
