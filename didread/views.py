from didread.models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.db import IntegrityError

import codecs
import datetime
import settings

import didread.controller


@login_required
def greet(request) :
    # this is the greeting page
    # the most important thing is to generate the bookmarklet

    # 2 distinct paths: 
    # if not logged in, offer login and signup
    # if logged in, offer bookmarklet.

    bookmarklet = didread.controller.bookmarklet_for_user(request.user)

    return render_to_response('didread/greet.html', {'bookmarklet' :bookmarklet}, context_instance=RequestContext(request))


def signup(request) :
    print "SIGING ON UP"
    params = request.POST
    print params
    # Check and see if the user has been created before, return error in that

    try :
        username = params["username"]
        email_address = params["email_address"]
        password = params["password"]
        first_name = params["first_name"]
        last_name = params["last_name"]
    except Exception :
        print "INCOMPLETE FORM"
        return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))

    # create the user
    try :
        new_user = User.objects.create_user(username,email_address,password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
    except IntegrityError :
        print "CAN'T DO. Can't have the same user twice"
        return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))

    user = authenticate(username=username, password=password)
    login(request,user)
    
    # redirect the user to /
    return HttpResponseRedirect('/')

@login_required
def recent(request) :
    # Test and see if we are really logged in.
    latest_reads = request.user.article_set.all().order_by('-read_date')

    return render_to_response('didread/recent.html', {'recent_reads' :latest_reads}, context_instance=RequestContext(request))

@login_required
def authors(request) :
    #user is me
    authors = request.user.author_set.all().order_by('name')
    
    return render_to_response('didread/authors.html', {'authors' : authors}, context_instance=RequestContext(request))


# This is the call to add a new article
def add_article(request,user_prefix) :
    print "We Enter The Add Call"
    print "USER IS: ",user_prefix
    # deal with the user for real...
    user = User.objects.get(pk=user_prefix)

    do_update = True
        
    try :
        #url = models.URLField()
        #user = models.ForeignKey(User)

        #title = models.CharField(max_length = 200)
        #author = models.ForeignKey(Author)
        #pub_date = models.DateTimeField('date published')
        #read_date = models.DateTimeField('date read') 
        #vote = models.IntegerField()

        print request.GET
        print "--"
        print request.POST

        params = request.GET
        scrape_params = []

        print "-------------------Adding New Article"


        if 'url' in params :
            # Find url if it has been saved before.
            try: 
                new_article = Article.objects.get(user=user,url=params['url'])
                if "initial_add" in request.path :
                    do_update = False
                print "OLD HAT"
            except (Article.DoesNotExist) :
                # Before doing anything else, append it to the file so we don't lose it
                print "writing to backup"
                backup = codecs.open('url_backup.txt','a', encoding='utf8')
                backup.write(params['url'] + '\n')
                backup.close()
                print "This Article Has Not Been Seen Before"
                new_article = Article()
                new_article.url = params['url']
        else :
            print "Well there isn't a url, so...."
            raise Http404
        
        print "TIme TO UPDATE?"
        if do_update:
            print "ALLUPDATING IN HERE"

            if 'vote' in params :
                vote = int(params['vote'])
                if 3 >= vote and 0 <= vote :
                    new_article.vote = vote
                else :
                    new_article.vote = 0
                    print "bad vote"
            else :
                print "bad vote"
                new_article.vote = 0

            if 'title' in params and params['title'] != "":
                new_article.title = params['title']
            else :
                print "bad title"
                new_article.title = params['url']
                scrape_params.append('title')

            if 'pub_date' in params :
                new_article.pub_date = datetime.datetime.strptime(params['pub_date'],"%Y-%m-%d")
            else :
                print "bad pub_date"
                new_article.pub_date = datetime.datetime.today()
                scrape_params.append('pub_date')

            if 'read_date' in params :
                new_article.read_date = datetime.datetime.strptime(params['read_date'],"%Y-%m-%d")
            else :
                print "no read_date"
                new_article.read_date = datetime.datetime.today()

            author_name = ""
            if 'author_name' in params and params['author_name'] != "":
                author_name = params['author_name']
            else :
                print "No Author Name"


            new_article.user = user

            print new_article
            print new_article.url.encode('utf-8')
            print new_article.title.encode('utf-8')
            print new_article.vote
            print new_article.pub_date
            print new_article.read_date
            print author_name
            print scrape_params

            # get the author for this url
            didread.controller.author_for_article(new_article,author_name)

            if not new_article.author : 
                print "There was no Author found here."


            # get other data from the page in the back thread...


            new_article.save()

    except (KeyError) :
        print "Poorly formatted submission."
        #404
        raise Http404

    print "Past the except"

    # if this came from "initial_add" (the bookmarklet) return the JS.
    # If it came from /add (the JS) then return some sort of success code

    print request.path.encode('utf-8')

    if "initial_add" in request.path :
        print "This was from the initial add"
        # This will be where we do logic to get the scraping js
        author_string = ""
        if new_article.author :
            author_string = new_article.author.name
        title_string = ""
        if new_article.title :
            title_string = new_article.title

        frame_string = didread.controller.add_frame_contents()

        context = { 'root_url' : settings.MY_ROOT_URL, 'url' : params['url'] , 'author' : author_string, 'title' : title_string, 'frame_contents' : frame_string, 'user_prefix': user_prefix}
        
        return render_to_response('didread/add_article.js', context)


    if "/add" in request.path:
        print "This came from the second add"
        return render_to_response('didread/kill_frame.js',{})

    return HttpResponse("How did you get here?")
    

def related_articles(request) :
    return HttpResponse("NO")

# This is super insecure. Can we check that the currently logged in user owns
# this?
@login_required
def delete_article(request, article_id) :
    # check and see if the user owns this, otherwise error
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

