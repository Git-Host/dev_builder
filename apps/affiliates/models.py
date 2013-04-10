from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

def _check_for_dupes(slug):
    return Affiliate.objects.filter(slug=slug).count() != 0

"""
Affiliate model with auto slugify on save
"""
class Affiliate(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_candidate = slugify(self.name)
            length = len(slug_candidate)
            index = 0
            while _check_for_dupes(slug_candidate):
                index += 1
                slug_candidate = slug_candidate[:length] + str(index)
            self.slug = slug_candidate
        
        super(Affiliate, self).save(*args, **kwargs)
    
    def __unicode__(self):
        site = Site.objects.get_current()
        return self.name + " ?affiliate="+self.slug

"""
Model to log visits
"""
class Visit(models.Model):
    affiliate = models.ForeignKey(Affiliate, related_name="visit_set")
    user = models.ForeignKey(User, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=64, unique=True)
    
    def __unicode__(self):
        if self.user:
            return self.user.username
        else:
            return self.session_key
    
    class Meta:
        ordering = ('date',)
    
    def get_is_authenticated(self):
        return self.user != None
    is_authenticated = property(get_is_authenticated)
