from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^repute/', include('repute.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    (r'^$','didread.views.greet'),
    (r'^recent/$','didread.views.recent'),
    (r'^excellent/$','didread.views.excellent'),
    (r'^authors/$','didread.views.authors'),

    (r'^add/(?P<user_prefix>\d+)$','didread.views.add_article'),
    (r'^initial_add/(?P<user_prefix>\d+)$','didread.views.add_article'),


    (r'^article/(?P<article_id>\d+)/delete$','didread.views.delete_article'),

    (r'^login/$', 'django.contrib.auth.views.login',{'template_name':'didread/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^signup/$', 'didread.views.signup'),
    

)

