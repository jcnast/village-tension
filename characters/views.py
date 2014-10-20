from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from characters.models import *

import random

def test(request):
	return render(request, 'default_options.html')

def default_people(request):

	first_names = ['Thalk', 'Morden', 'Laena', 'Crysten']
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

	return HttpResponse('people created')

def default_opinions(request):

	people = Character.objects.all()

	cares = ['race', 'religion', 'politics', 'family']

	targets_race = ['black', 'white', 'asian']
	targets_religion = ['catholics', 'muslims', 'athiests']
	targets_politics = ['conservative', 'republican', 'other']
	targets_family = ['theirs']

	for person in people:

		for care in cares:

			if care == 'race':
				target = random.choice(targets_race)
			elif care == 'religion':
				target = random.choice(targets_religion)
			elif care == 'politics':
				target = random.choice(targets_politics)
			elif care == 'family':
				target = random.choice(targets_family)

			opinion = Opinion(character=person, care=care, target=target,
				ramp=random.randrange(0,10,1)/10, tolerance=random.randrange(1,50,2)/10, enjoyment=random.randrange(-50,-10, 1)/10)
			opinion.save()

	return HttpResponse('opinions created')

def default_relations(request):

	people = Character.objects.all()

	for person in people:

		opinions = Opinion.objects.filter(character=person)

		for opinion in opinions:

			for aquaintance in people:

				if aquaintance != person:

					relationship = Relationship(opinion=opinion, aquaintance=aquaintance, impact='false')
					relationship.save()

	return HttpResponse('relations created')

def interaction(request, aquaintance, character, care, impact):
	
	interaction = Relationship.objects.get(aquaintance=aquaintance,
									opinion__character=character, opinion=care)

	interaction.impact = impact
	interaction.save()
	interaction.update()