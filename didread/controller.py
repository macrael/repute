# A place for controller methods
from urlparse import urlparse
from didread.models import *
from django.contrib.auth.models import User

# Find associate and return || DOES NOT SAVE!
def author_for_article(article,name) :
    print article.url
    parsed = urlparse(article.url)

    consider = []

    if name :
        for author in article.user.author_set.all() :
            if author.name.downcase() == name.downcase() :
                consider.append(author)

        if len(consider) == 0 :
            author = Author()
            author.user = article.user
            author.name = name
            author.url = "http://" + urlparse(article.url).netloc
            author.save()
            consider.append(author)

        if len(consider) > 1 :
            for author in consider :
                if urlparse(author.url).netloc != urlparse(article.url).netloc :
                    consider.remove(author)

        if len(consider) == 1 :
            article.author = consider[0]
            print "Found Author: " + consider[0].name
            return consider[0]

    consider = []
    for author in article.user.author_set.all() :
        if urlparse(author.url).netloc == urlparse(article.url).netloc :
            consider.append(author)

    if len(consider) == 0 :
        author = Author()
        author.user = article.user
        author.name = name
        author.url = "http://" + urlparse(article.url).netloc
        author.save()
        consider.append(author)

    # This is all pretty ugly. Probably should go by author name alone?
    # At some point, should check the super article and super author.
    # At some point, should prompt for new information? only check the urls if
    # the name is not provided? 
    # maybe rig up something for sites that don't silo this stuff. 

    if len(consider) == 1 :
        article.author = consider[0]
        print "Found Author: " + consider[0].name
        return consider[0]


    print "WE HAVE MULTIPLE CANDIDATES FOR THIS AUTHOR. WHAT SHOULD I DO?"
    print consider

    return None
