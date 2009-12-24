# -*- coding: utf-8 -*-

import grok
import megrok.resourcelibrary

from dolmen.app.layout.master import Header
from menhir.library.jquery import JQueryBase

from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from zope.catalog.interfaces import ICatalog
from zope.app.form.browser.widget import renderElement

grok.templatedir("templates")


class LiveSearchLibrary(megrok.resourcelibrary.ResourceLibrary):
    grok.name("menhir.simple.livesearch")
    megrok.resourcelibrary.depend(JQueryBase)
    megrok.resourcelibrary.directory('resources')
    megrok.resourcelibrary.include('jquery.dimensions.js')
    megrok.resourcelibrary.include('livesearch.js')
    megrok.resourcelibrary.include('livesearch.css')


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
        LiveSearchLibrary.need()


class MyQuery(grok.View):
    grok.name("livesearch")
    grok.context(Interface)

    def update(self):
        self.search = getMultiAdapter(
            (self.context, self.request), name="search.result")
        self.search.update()

    def render(self):
        return self.search.content()
