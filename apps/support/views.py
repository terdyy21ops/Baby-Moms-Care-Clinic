from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def support_dashboard(request):
    return render(request, 'support/dashboard.html', {})


def emergency_contacts(request):
    return render(request, 'support/emergency.html', {})


@login_required
def contact_list(request):
    messages.info(request, 'Contact management feature coming soon!')
    return redirect('support:dashboard')


@login_required
def contact_create(request):
    messages.info(request, 'Contact creation feature coming soon!')
    return redirect('support:dashboard')


@login_required
def contact_detail(request, pk):
    messages.info(request, 'Contact details feature coming soon!')
    return redirect('support:dashboard')


@login_required
def contact_update(request, pk):
    messages.info(request, 'Contact editing feature coming soon!')
    return redirect('support:dashboard')


@login_required
def contact_delete(request, pk):
    messages.info(request, 'Contact deletion feature coming soon!')
    return redirect('support:dashboard')


@login_required
def ticket_list(request):
    messages.info(request, 'Support tickets feature coming soon!')
    return redirect('support:dashboard')


@login_required
def ticket_create(request):
    messages.info(request, 'Ticket creation feature coming soon!')
    return redirect('support:dashboard')


@login_required
def ticket_detail(request, pk):
    messages.info(request, 'Ticket details feature coming soon!')
    return redirect('support:dashboard')


@login_required
def ticket_reply(request, pk):
    messages.info(request, 'Ticket reply feature coming soon!')
    return redirect('support:dashboard')


def faq_list(request):
    return render(request, 'support/faq.html', {})


@login_required
def faq_vote(request, pk):
    messages.info(request, 'FAQ voting feature coming soon!')
    return redirect('support:faq')


def resource_list(request):
    return render(request, 'support/resources.html', {})


@login_required
def chat_view(request):
    return render(request, 'support/chat.html', {})


@login_required
def send_message(request):
    messages.info(request, 'Chat feature coming soon!')
    return redirect('support:chat')
