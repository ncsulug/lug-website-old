# -*- coding: utf-8 -*-
from .forms import EditForm
from .models import Page, Revision
from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden, Http404)
from django.shortcuts import render, redirect

def view_page(request, title, revision_id=None):
    title = title.replace("_", " ")
    try:
        page = Page.objects.get(title=title)
    except Page.DoesNotExist:
        page_list = Page.objects.filter(title__iexact=title).all()
        if len(page_list) != 0:
            return redirect("wiki_view", title=page_list[0].title )
        return render(request, "lug_wiki/not-found.html", {'title': title},
                      status=404)


    if revision_id:
        try:
            revision = page.revisions.get(id=int(revision_id))
        except Revision.DoesNotExist:
            raise Http404()
    else:
        revision = page.latest_revision

    if not page.user_may_view(request.user):
        return HttpResponseForbidden()

    if request.GET.get("raw", ""):
        response = HttpResponse(mimetype='text/plain')
        response['Content-Disposition'] = ('attachment; filename=%s.txt' %
                                           quote(title.encode('utf-8')))
        response.write(revision.content)
        return response

    return render(request, "lug_wiki/page.html", {
        'page': page, 'revision': revision,
        'editable': page.user_may_edit(request.user)
    })


def edit_page(request, title):
    title = title.replace("_", " ")

    try:
        page = Page.objects.get(title=title)
        last_revision = page.latest_revision
    except Page.DoesNotExist:
        page_list = Page.objects.filter(title__iexact=title).all()
        if len(page_list) != 0:
            return redirect("wiki_edit", title=page_list[0].title )
        page = Page(title=title)
        last_revision = None
    last_content = None if last_revision is None else last_revision.content

    if not page.user_may_edit(request.user):
        return HttpResponseForbidden()

    revision = Revision(page=page, author=request.user.get_profile())
    form = EditForm(request.POST or None, instance=revision, page=page,
                    initial={'content': last_content})
    preview_content = None

    if request.method == "POST":
        valid = form.is_valid()
        if request.POST.get('action') == 'preview':
            preview_content = form.preview_content
        elif valid:
            form.save()
            return HttpResponseRedirect(reverse('wiki_view', kwargs={
                'title': title.replace(" ", "_")
            }))

    return render(request, "lug_wiki/edit.html", {
        'form': form, 'page': page, 'last_revision': last_revision,
        'preview_content': preview_content
    })


def page_history(request, title):
    title = title.replace("_", " ")
    try:
        page = Page.objects.get(title=title)
    except Page.DoesNotExist:
        page_list = Page.objects.filter(title__iexact=title).all()
        if len(page_list) != 0:
            return redirect("wiki_history", title=page_list[0].title )
        raise Http404()

    if not page.user_may_view(request.user):
        return HttpResponseForbidden()

    return render(request, "lug_wiki/history.html", {
        'page': page, 'revisions': page.revisions.order_by("-timestamp").all()
    })
