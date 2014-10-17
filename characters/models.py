from django.db import models

class Character(models.Model):

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)

	health = models.IntegerField(default=100)
	# other stats (dex, str, ...)

	allies = models.ManyToManyField('Character', related_name='like', null=True, blank=True)
	enemies = models.ManyToManyField('Character', related_name='hate', null=True, blank=True)
	family = models.ManyToManyField('Character', related_name='related', null=True, blank=True)

	# total amount of shit they can take
	tolerance_threshhold = models.FloatField(default=5.0)
	# the amount of in-between someone can be before they are an enemey or ally
	lee_way = models.FloatField(default=5.0)

	def __unicode__(self, *args, **kwargs):
		return self.first_name+' '+self.last_name

	def favour(aquaintance):

		# all their relationships with the specific person
		relationships = Relationship.objects.filter(aquaintance=aquaintance)

		# how much shit they are taking
		tolerance_level = 0
		for relationship in relationship:
			# if they are more aggravated than they can stand, the tolerance level increases
			if relationship.aggravation > relationships.opinion.tolerance:

				tolerance_level += relationship.aggravation / relationship.opinion.tolerance
			# if they are less aggravated than they want to be, the tolerance level decreases
			elif relationship.aggravation < relationship.opinion.enjoyment:

				tolerance_level -= relationship.aggravation / relationship.opinion.enjoyment

		# if tolerance_level is greter than tolerance_threshhold+lee_way they are an enemy
		if tolerance_level*len(relationships) > tolerance_threshhold+lee_way:
			if not(aquaintance in enemies):
				enemies.append(aquaintance)
		# if tolerance_level is less than tolerance_threshhold-lee_way they are an ally
		elif tolerance_level*len(relationships) < tolerance_threshhold-lee_way:
			if not(aquaintance in allies):
				allies.append(aquaintance)
		# else make sure the aquaintance is not in either list
		else:
			if aquaintance in enemies:
				enemies.remove(aquaintance)
			elif aquaintance in allies:
				allies.remove(aquaintance)

class Opinion(models.Model):

	# who has this care
	character = models.OneToOneField(Character)

	# what they care about (political party, crimes, race, religion, family...)
	care = models.CharField(max_length=50)

	# how slowly/quickly they hate you per time you piss them off
	ramp = models.FloatField(default=0.0) #set value (float between 0.0 and 1.0)

	# how high they can be aggravated before they are your enemy
	tolerance = models.FloatField(default=10.0) #set value (must be float)

	# how low their aggravation must be before they are your friend
	enjoyment = models.FloatField(default=-10.0) #set value (must be float)

	def __unicode__(self):
		return self.character.first_name+' '+self.character.last_name+': '+self.care

class Relationship(models.Model):

	opinion = models.ForeignKey(Opinion)

	# who the person affecting it is
	aquaintance = models.ForeignKey(Character)

	# how many times you have aggravated this person
	ticks = models.FloatField(default=0.0) #changing value

	# how angry they are at the moment
	# equation: aggravation += (1+ramp*ticks)
	aggravation = models.FloatField(default=0.0) #changing value

	def __unicode__(self):
		return self.character.first_name+' '+self.character.last_name+'/'+self.aquaintance.first_name+' '+self.aquaintance.last_name+' ('+self.opinion.care+')'

	def save(self, *args, **kwargs):

		self.ticks += 1
		self.aggravation += 1+self.opinion.ramp*self.ticks

		self.opinion.character.favour(self.aquaintance)

		super(Model, self).save(*args, **kwargs)