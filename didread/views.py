from didread.models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import datetime

import didread.controller


def recent(request) :
    #user is me
    latest_reads = Article.objects.all().order_by('-read_date')

    return render_to_response('didread/recent.html', {'recent_reads' : latest_reads})



# This is the call to add a new article
def add_article(request) :
    # deal with the user for real...
    user = User.objects.get(username__exact='macrael')

    try :
        #url = models.URLField()
        #user = models.ForeignKey(User)

        #title = models.CharField(max_length = 200)
        #author = models.ForeignKey(Author)
        #pub_date = models.DateTimeField('date published')
        #read_date = models.DateTimeField('date read')
        #vote = models.IntegerField()

        params = request.GET
        scrape_params = []

        print "-------------------Adding New Article"


        if 'url' in params :
            # Find url if it has been saved before.
            try: 
                new_article = Article.objects.get(user=user,url=params['url'])
                print "OLD HAT"
            except (Article.DoesNotExist) :
                print "This Article Has Not Been Seen Before"
                new_article = Article()
                new_article.url = params['url']
        else :
            raise Http404

        if 'vote' in params :
            vote = int(params['vote'])
            if 1 >= vote and -1 <= vote :
                new_article.vote = vote
            else :
                new_article.vote = 0
                print "bad vote"
        else :
            print "bad vote"
            new_article.vote = 0

        if 'title' in params :
            new_article.title = params['title']
        else :
            print "bad title"
            new_article.title = params['url']
            scrape_params.append('title')

        if 'pub_date' in params :
            new_article.pub_date = datetime.datetime.strptime(params['pub_date'],"%Y-%m-%d")
        else :
            print "bad pub_date"
            new_article.pub_date = datetime.date.today()
            scrape_params.append('pub_date')

        if 'read_date' in params :
            new_article.read_date = datetime.datetime.strptime(params['read_date'],"%Y-%m-%d")
        else :
            print "no read_date"
            new_article.read_date = datetime.date.today()

        author_name = ""
        if 'author_name' in params :
            author_name = params['author_name']
        else :
            print "No Author Name"


        new_article.user = user

        print new_article
        print new_article.url
        print new_article.title
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
    
    return HttpResponse("successfully added the thing.")

def related_articles(request) :
    return HttpResponse("NO")
