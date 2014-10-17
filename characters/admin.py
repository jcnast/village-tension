from django.contrib import admin
from characters.models import *

class CharacterAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name']

class OpinionAdmin(admin.ModelAdmin):
	fields = ['character__first_name', 'character__last_name', 'care']

class RelationshipAdmin(admin.ModelAdmin):
	fields = ['opinion__character__first_name', 'opinion__character__last_name', 'aquaintance__first_name', 'aquaintance__last_name']

admin.site.register(Character)
admin.site.register(Opinion)
admin.site.register(Relationship)