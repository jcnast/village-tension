from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from characters.models import *

import random

def test(request):
	characters = Character.objects.all()
	opinions = []
	for character in characters:
		cares = Opinion.objects.filter(character=character)
		relationships = []
		for care in cares:
			relationship = Relationship.objects.filter(opinion=care)
			relationships.append(relationship)
		opinions.append(zip(cares, relationships))
	context = {'characters': zip(characters, opinions), 'header': 'Character Stats'}
	return render(request, 'characters/default_options.html', context)

def default_people(request):

	first_names = ['Thalk', 'Morden']#, 'Laena', 'Crysten']
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
	targets_family = ['theirs', 'none']

	for person in people:
		print person
		for care in cares:
			print care
			if care == 'race':
				target1 = random.choice(targets_race)
				target2 = random.choice([x for x in targets_race if x != target1])
			elif care == 'religion':
				target1 = random.choice(targets_religion)
				target2 = random.choice([x for x in targets_religion if x != target1])
			elif care == 'politics':
				target1 = random.choice(targets_politics)
				target2 = random.choice([x for x in targets_politics if x != target1])
			elif care == 'family':
				target1 = random.choice(targets_family)
				target2 = random.choice([x for x in targets_family if x != target1])

			opinion = Opinion(character=person, care=care, likes=target1, dislikes=target2,
				ramp=(random.randrange(0,10,1)/10), tolerance=(random.randrange(10,50,2)/10), enjoyment=(random.randrange(-50,-10, 1)/10))
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

# figure out how the interaction will work
def random_interaction(request):

	people = Character.objects.all()

	cares = ['race', 'religion', 'politics', 'family']

	targets_race = ['black', 'white', 'asian']
	targets_religion = ['catholics', 'muslims', 'athiests']
	targets_politics = ['conservative', 'republican', 'other']
	targets_family = ['theirs']

	# pick a random person who 'did the action'
	aquaintance = random.choice(people)
	# pick an opinion they are affecting
	care = random.choice(cares)

	# pick a target based on what they are impacting
	if care == 'race':
		target = random.choice(targets_race)
	elif care == 'religion':
		target = random.choice(targets_religion)
	elif care == 'politics':
		target = random.choice(targets_politics)
	elif care == 'family':
		target = random.choice(targets_family)

	# if the target is what the character likes (their target), they have a positive impact on
	# others who share that target (as they likely did a good thing to it) and a negative on 
	# people who don't (since they don't care about it)
	aquaintance_opinion = Opinion.objects.get(character=aquaintance, care=care)
	if target == aquaintance_opinion.likes:
		impact = 'positive'
	elif target == aquaintance_opinion.dislikes:
		impact = 'negative'
	else:
		rand = random.randrange(0,2)
		if rand == 1:
			impact = 'positive'
		else:
			impact = 'negative'

	for character in people:
		if character != aquaintance:

			# if the person agrees with the aquaintance, the impact remains as intended
			# if they do not agree, the impact is reversed
			opinion = Opinion.objects.get(character=character, care=care)
			if opinion.likes == target:
				pass
			elif opinion.dislikes == target:
				if impact == 'positive':
					impact = 'negative'
				else:
					impact = 'positive'
			else: 
				'''
				could make it so that if the character has no like or dislikes for the target that they judge based on the
				person doing the action (enemy = negative, ally = positive) and then they could add that target to their list
				of likes/dislikes if this happens enough (add a counter for each opinion, once the counter passes their threshholds
				it gets added to one of the lists)
				'''
				impact = 'none'

			interact(aquaintance, character, care, impact)

	return HttpResponse('characters have randomly interacted')

def interaction(request, aquaintance, character, care, impact):

	interact(aquaintance, character, care, impact)

	return HttpResponse('characters have interacted')

def interact(aquaintance, character, care, impact):
	if impact != 'none':
		interaction = Relationship.objects.get(aquaintance=aquaintance, opinion__character=character, opinion__care=care)
		interaction.impact = impact
		interaction.save()
		interaction.update()
	else:
		pass