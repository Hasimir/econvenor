from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from docs.models import Item
from meetings.forms import NewMeetingForm
from meetings.models import Meeting
from meetings.utils import archive_meeting, \
                           delete_meeting, \
                           unarchive_meeting
from utilities.commonutils import get_current_group


def meeting_add(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = NewMeetingForm(group, request.POST, label_suffix='')
        if form.is_valid() :
            # save the data
            meeting = form.save(group)
            # create a blank first agenda item and link it to the meeting
            first_item = Item(title='New item', item_no=1, group=group)
            meeting.item_set.add(first_item)
            # get the meeting id to enable the page redirect
            meeting_id = meeting.id
            return HttpResponseRedirect(reverse('agenda-edit',
                                                args=(meeting_id,)))
    else:
        form = NewMeetingForm(group, label_suffix='')

    menu = {'parent': 'meetings',
            'child': 'new_meeting',
            'tips': 'new_meeting'
            }
    return render(request, 'meeting_add.html', {
                  'menu': menu,
                  'form': form,
                  })


def meeting_list_current(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meetings = Meeting.lists.current_meetings().filter(group=group)
    page_heading = 'Current meetings'
    table_headings = ('Date',
                      'Meeting Number',
                      'Agenda sent',
                      'Minutes sent',
                      'Next action',
                      'Other actions',
                      )

    if request.method == "POST":
        if request.POST['button'][:6] == 'delete':
            delete_meeting(request, group)
        if request.POST['button'][:7] == 'archive':
            archive_meeting(request, group)
        meetings = Meeting.lists.current_meetings().filter(group=group)

    menu = {'parent': 'meetings',
            'child': 'current_meetings',
            'tips': 'current_meetings'
            }
    return render(request, 'meeting_list_current.html', {
                  'menu': menu,
                  'meetings': meetings,
                  'page_heading': page_heading,
                  'table_headings': table_headings
                  })


def meeting_list_archive(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meetings = Meeting.lists.archived_meetings().filter(group=group)
    page_heading = 'Archived meetings'
    table_headings = ('Date',
                      'Meeting Number',
                      'Meeting type',
                      '',
                      '',
                      '',
                      )

    if request.method == "POST":
        if request.POST['button'][:6] == 'delete':
            delete_meeting(request, group)
        if request.POST['button'][:9] == 'unarchive':
            unarchive_meeting(request, group)
        meetings = Meeting.lists.archived_meetings().filter(group=group)

    menu = {'parent': 'meetings',
            'child': 'archived_meetings',
            'tips': 'archived_meetings'
            }
    return render(request, 'meeting_list_archive.html', {
                  'menu': menu,
                  'meetings': meetings,
                  'page_heading': page_heading,
                  'table_headings': table_headings
                  })

