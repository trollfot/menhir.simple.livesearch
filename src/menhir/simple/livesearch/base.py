# -*- coding: utf-8 -*-

import grok
from megrok import resource

from dolmen.app.layout.master import Header
from hurry.jquery import jquery

from zope.interface import Interface
from zope.component import getMultiAdapter

grok.templatedir("templates")


class LiveSearchResources(resource.ResourceLibrary):
    grok.path('resources')
    resource.resource('jquery.dimensions.js', depends=[jquery])
    resource.resource('livesearch.js')
    resource.resource('livesearch.css')


class LiveSearch(grok.Viewlet):
    grok.name("livesearch")
    grok.context(Interface)
    grok.viewletmanager(Header)

    def render(self):
        return u"""
        <script>
        $(document).ready(function(){
          $('#search-widget').liveSearch({
             ajaxURL: '%s/livesearch?search_term='
           });
        });
        </script>
        """ % self.view.url(self.context)

    def update(self):
        LiveSearchResources.need()


class MyQuery(grok.View):
    grok.name("livesearch")
    grok.context(Interface)

    def update(self):
        self.search = getMultiAdapter(
            (self.context, self.request), name="search.result")
        self.search.update()

    def render(self):
        return self.search.content()
