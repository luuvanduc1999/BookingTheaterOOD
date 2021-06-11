from django.db import models
from django.conf import settings
from django.db.models import Max
import re
import hashlib

# Create your models here.
class dashboard(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.CASCADE) #Note.imp.
	name = models.CharField(max_length=200, default = 'default about text')
	email = models.EmailField(null = True)
	age = models.IntegerField(null=False, default=0)
	
	def __str__(self):
		return str(self.user)

class Movie(models.Model):
	id = models.CharField(primary_key=True, editable=False, max_length=10)
	name = models.CharField(max_length=100)
	url = models.TextField(null= True)
	year = models.IntegerField(null=True)
	MY_CHOICES = [
        ('PG', 'PG'),
        ('PG13', 'PG-13'),
        ('G', 'G'),
        ('R', 'R'),
	]
	rate = models.CharField(max_length=4, choices=MY_CHOICES)

	def save(self, **kwargs):
		if not self.id:
			max = Movie.objects.aggregate(id_max=Max('id'))['id_max']
			max = int(re.search(r'\d+', max).group())+1
			self.id = "{}{:05d}".format('MV', max if max is not None else 1)
		super().save(*kwargs)

	def __str__(self):
		return self.id

class Room(models.Model):
	id = models.CharField(primary_key=True, editable=False, max_length=10)
	name = models.CharField(max_length=100)
	slot = models.IntegerField(null=True, default=0)

	def save(self, **kwargs):
		if not self.id:
			max = Room.objects.aggregate(id_max=Max('id'))['id_max']
			if max is None: max ="0"
			max = int(re.search(r'\d+', max).group())+ 1
			self.id = "{}{:03d}".format('R', max if max is not None else 1)
		super().save(*kwargs)

	def __str__(self):
		return self.id

class Ticket(models.Model):
	id = models.CharField(primary_key=True, editable=False, max_length=10)

	TIMES = [
        ('8h', '8:00'),
        ('11h', '11:00'),
        ('14h', '14:00'),
        ('17h', '17:00'),
		('20h','20:00'),
	]
	time =  models.CharField(max_length=4, choices=TIMES, default="8h")
	date = models.DateField( auto_now=False, auto_now_add=False)
	slot = models.IntegerField(null=True, default=0)
	STATUS= [ ('ON' , 'Active'), ('OFF' , 'Inactive') ]
	MY_CHOICES = (
        ('2D', '2D'),
        ('3D', '3D'),
    )
	type =  models.CharField(max_length=4, choices=MY_CHOICES)
	room = models.ForeignKey(Room,null=True,blank=True, on_delete=models.CASCADE) #Note.imp.
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default = "MV00001")
	status = models.CharField(max_length=4, choices=STATUS, default="ON")
	confirmed = models.CharField(max_length=4, choices=STATUS, default="OFF")
	confirm_code = models.CharField(max_length=8, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def save(self, **kwargs):
		if not self.id:
			max = Ticket.objects.aggregate(id_max=Max('id'))['id_max']
			if max is None: max ="0"
			max = int(re.search(r'\d+', max).group())+ 1
			self.id = "{}{:03d}".format('TK', max if max is not None else 1)
		if not self.confirm_code:
			self.confirm_code = str(abs(hash(self.id)) % (10 ** 8))
		super().save(*kwargs)

	class Meta:
		unique_together = ('room', 'time', 'date')
	
	def __str__(self):
		return self.id

