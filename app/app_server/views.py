import pdb

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from haystack.views import SearchView

from os import system

from django.views.generic.edit import FormView

from apps.cserver_comm.cserver_communicator import get_search_json
from forms import ContactForm


"""
Main application views that do not nicely fit into an app, i.e. because they span
multiple apps or are app agnostic
"""

class MultiSearchView(SearchView):
    """
    Class that searches both content-based and application-based data
    """
    def extra_context(self):
        """
        Adds the concept search (list) results for a given query TODO we may want to move this funcitonality to the client (have their browser query the content server)
        """
        qstring = self.get_query()
        if len(qstring) == 0:
            search_data = None
            print 'WARNING: empty query parameter in get_search_view'
        else:
            search_data = get_search_json(qstring)

        return {"concepts_search_data": search_data, 'search_query': qstring}


class ContactView(FormView):
    template_name = 'feedback.html'
    form_class = ContactForm
    success_url = '/thanks'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

