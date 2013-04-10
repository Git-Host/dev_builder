#python imports
from datetime import datetime

#django imports
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# affiliate imports
from affiliates.models import Affiliate, Visit


def _delete_visit_from_session(request):
    try:
        del request.session['visit_id']
    except KeyError:
        pass


def _get_visit_from_request(request):
    try:
        visit = Visit.objects.get(pk=request.session['visit_id'])
    except Visit.DoesNotExist:
        visit = None
    return visit


class AffiliateMiddleware(object):
    
    """
    Affiliate Middleware takes a get parameter, records as a Visit instance.
    If a user is logged in or logs later it assocaites the user.
    
    AffiliateMiddleware's current philosophy  is that only the first
    affiliate that brings in an authenticated user should get the credit.
    This might be optional in future versions depending on demand for
    alternative philosophies.
    
    For now, there is no unique=True constraint for users, although
    uniqueness is enforced in the middleware.
    """
    
    def process_request(self, request):
        
        #if there already is a visit_id in the session
        if 'visit_id' in request.session:
            if request.user.is_authenticated():
                if Visit.objects.filter(user=request.user).count() == 0:
                    # Add the user to the visit
                    visit = _get_visit_from_request(request)
                    if visit:
                        visit.user = request.user
                        visit.save()

                #If there is an anonomous visit, but the user already has a visit delete the anon visit.
                else:
                    visit = _get_visit_from_request(request)
                    if visit:
                        visit.delete()
    
                _delete_visit_from_session(request)

        #if there is no visit for this session or user (and implictly no visit_id in the session)
        elif request.method == 'GET' and Visit.objects.filter(session_key=request.session.session_key).count() == 0:
            if 'affiliate' in request.GET:
                try:
                    affiliate = Affiliate.objects.get(slug=request.GET['affiliate'])
                except Affiliate.DoesNotExist:
                    affiliate = None
                    
                if affiliate:
                    if request.user.is_authenticated():
                        if Visit.objects.filter(user=request.user).count() == 0:
                            #associate the user with the affiliate
                            visit = Visit(user=request.user)
                            #add the session key
                            visit.session_key=request.session.session_key
                            #add the affiliate
                            visit.affiliate=affiliate
                            visit.date = datetime.now()
                            visit.save()
                    else:
                        #record the affiliate link visit
                        visit = Visit(session_key=request.session.session_key)
                        #add the affiliate
                        visit.affiliate=affiliate
                        visit.date = datetime.now()
                        visit.save()
                        #record the visit id in the session for future matching with authenticated user
                        request.session['visit_id']=visit.pk

        #Forwarding so that the affiliate get parameter isn't making things ugly for the user.
        if request.method == 'GET':
            if 'affiliate' in request.GET:
                #preserve other get parameters during redirect
                q = request.GET.urlencode().replace('affiliate='+request.GET['affiliate'],'').replace('&&','&').rstrip('&').lstrip('&')
                if len(q) > 0:
                    return HttpResponseRedirect(request.path_info+"?"+q)
                else:
                    return HttpResponseRedirect(request.path_info)
