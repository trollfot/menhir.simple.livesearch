# -*- coding: utf-8 -*-

import grok
import megrok.resourcelibrary
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from menhir.library.jquery import JQueryBase
from zope.app.catalog.interfaces import ICatalog
from zope.app.form.browser.widget import renderElement
from dolmen.app.layout.master import DolmenHeader


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
    grok.viewletmanager(DolmenHeader)

    def render(self):
        return u""

    def update(self):
        LiveSearchLibrary.need()


class MyQuery(grok.View):
    grok.name("livesearch")
    grok.context(Interface)

    def update(self):
        self.search = getMultiAdapter((self.context, self.request),
                                      name="searchresults")
        self.search.update()

    def render(self):
        return self.search.render()
