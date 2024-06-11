from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClassicRecordSubmissionForm, PlatformerRecordSubmissionForm
from .models import ClassicRecordSubmission, PlatformerRecordSubmission
from django.contrib import messages

# Create your views here.

@login_required
def submit_record(request, record_type):
    if not request.user.is_email_verified:
        messages.error(request, 'You need to activate your email in order to submit a record.')
        return redirect('player:profile', username=request.user.username)
    
    if record_type == 'classic':
        form_class = ClassicRecordSubmissionForm
    elif record_type == 'platformer':
        form_class = PlatformerRecordSubmissionForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.player = request.user
            record.save()
            messages.success(request, 'Record submitted successfully.')
            return redirect('player:profile', username=request.user.username)
    else:
        form = form_class()

    return render(request, 'recordsubmission/submitrecord.html', {'form': form, 'record_type': record_type})

@login_required
def submissions(request):
    classic_submissions = ClassicRecordSubmission.objects.filter(player=request.user)
    platformer_submissions = PlatformerRecordSubmission.objects.filter(player=request.user)
    
    context = {
        'classic_submissions': classic_submissions,
        'platformer_submissions': platformer_submissions,
    }
    
    return render(request, 'recordsubmission/submissions.html', context)