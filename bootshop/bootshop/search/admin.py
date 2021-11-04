from django.contrib import admin
from .models import SearchTerm
from django.contrib import admin

# Register your models here.


class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ip_address', 'search_date')
    list_filter = ('ip_address', 'q')


admin.site.register(SearchTerm, SearchTermAdmin)
