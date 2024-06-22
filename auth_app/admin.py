from django.contrib import admin
from .models import Profile, Favourite, Visited

class ProfileAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "get_email", "paid", "pageview", "customer_id")

	@admin.display(description="email")
	def get_email(self, obj):
		return f"{obj.user.email}"

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Favourite)
admin.site.register(Visited)