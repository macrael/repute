# A place for controller methods
from urlparse import urlparse
from didread.models import *
from django.contrib.auth.models import User
from django import template
from django.template.loader import render_to_string
import settings
import re
import urllib

# Find associate and return || DOES NOT SAVE!
def author_for_article(article,name) :
    print "Entering Author Get"
    parsed = urlparse(article.url)

    consider = []

    if name :
        for author in article.user.author_set.all() :
            if author.name.lower() == name.lower() :
                consider.append(author)

        if len(consider) == 0 :
            print "creating a NEW author"
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




def bookmarklet_for_user(user) :
    
    rendered = render_to_string('didread/bookmarklet.js',{"root_url" :
    settings.MY_ROOT_URL , "user_prefix": user.id} )
    
    print rendered

    # regular expressions copied from
    # http://daringfireball.net/2007/03/javascript_bookmarklet_builder
    comments_re = re.compile('(^|\s+)//.+\n')
    tabs_re = re.compile('\t')
    spaces_re = re.compile('[ ]{2,}')
    lead_re = re.compile('^\s+')
    trail_re = re.compile('\s+$')
    newline_re = re.compile('\n')

    rendered = comments_re.sub("",rendered)
    rendered = tabs_re.sub(" ",rendered)
    rendered = spaces_re.sub(" ",rendered)
    rendered = lead_re.sub("",rendered)
    rendered = trail_re.sub("",rendered)
    rendered = newline_re.sub("",rendered)
    
    print rendered

    rendered = "javascript:" + urllib.quote(rendered,"():{}/;=,+")

    print rendered

    return rendered


def add_frame_contents() :

    rendered = render_to_string('didread/add_frame.html',{})

    tabs_re = re.compile('\t')
    spaces_re = re.compile('[ ]{2,}')
    lead_re = re.compile('^\s+')
    trail_re = re.compile('\s+$')
    newline_re = re.compile('\n')

    rendered = tabs_re.sub(" ",rendered)
    rendered = spaces_re.sub(" ",rendered)
    rendered = lead_re.sub("",rendered)
    rendered = trail_re.sub("",rendered)
    rendered = newline_re.sub("",rendered)

    print rendered

    return rendered

