from django.contrib import admin
from affiliates.models import Visit, Affiliate
from django.core.urlresolvers import reverse

class AffiliateOptions(admin.ModelAdmin):
    
    list_display = (
        'name',
        'query_string',
        'anon_visits',
        'auth_visits',
        'total_visits',
    )
    
    def name(self, obj):
        return obj.name
    name.short_description = 'Affiliate Name'
    
    def query_string(self, obj):
        return "?affiliate="+obj.slug
    query_string.short_description = "Query String"
    
    def anon_visits(self, obj):
        return obj.visit_set.filter(user=None).count()
    anon_visits.short_description = "Anonymous Visits"
    
    def auth_visits(self, obj):
        return obj.visit_set.exclude(user=None).count()
    auth_visits.short_description = "Authenticated Visits"
    
    def total_visits(self, obj):
        return obj.visit_set.all().count()
    total_visits.short_description = "Total Visits"

admin.site.register(Visit)
admin.site.register(Affiliate, AffiliateOptions)
