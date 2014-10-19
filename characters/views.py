from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from characters.models import *

import random

def test(request):
	return render(request, 'skin.html')

def default_people():

	first_names = ['Thalk', 'Morden', 'Marissa', 'Laena', 'Jagger', 'Cryten']
	last_names = ['Smith', 'Stone', 'Seestern', 'Carp']

	cares = ['politics', 'religion', 'faimly', 'race']

	# Create characters with a first name and last name
	for name in first_names:
		character = Character(
				first_name = name,
				last_name = last_names[random.randint(0,3)]	
			)
		character.save()

	# Create families based on shared last names
	characters = Character.objects.all()
	for character in characters:
		for other in characters:
			if character != other:
				if other.last_name == character.last_name:
					character.family.add(other)
					character.save()

def interaction(aquaintance, character, care, impact):
	
	interaction = Relationship.objects.get(aquaintance=aquaintance,
									opinion__character=character, opinion=care)

	interaction.impact = impact
	interaction.save()
	interaction.update()