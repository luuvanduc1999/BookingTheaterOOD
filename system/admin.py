from django.contrib import admin
from .models import dashboard, Movie, Room, Ticket

class dashboardAdmin(admin.ModelAdmin):
	class Meta:
		model = dashboard
admin.site.register(dashboard,dashboardAdmin)
# Register your models here.

class dashboardAdmin(admin.ModelAdmin):
	class Meta:
		model = Movie
admin.site.register(Movie)


class dashboardAdmin(admin.ModelAdmin):
	class Meta:
		model = Room
admin.site.register(Room)


class dashboardAdmin(admin.ModelAdmin):
	class Meta:
		model = Ticket
admin.site.register(Ticket)
