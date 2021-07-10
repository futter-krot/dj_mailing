import threading
import time
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from shipment.models import Letter
from shipment.forms import LetterForm
from django.core.mail import send_mail, EmailMessage


# Create your views here.


class LetterTread(threading.Thread):

    def __init__(self, mail, postdate, let):
        self.mail = mail
        self.postdate = postdate
        self.let = let
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.postdate)
        print('time to go!')
        self.let.update(status='P')
        self.mail.send(fail_silently=False)


class AddLetter(CreateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('shipment:letter-list')
    template_name = 'shipment/cletter.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def letter_list(request):
    template_name = 'shipment/index.html'
    last = Letter.objects.all().order_by('-id')[:10]
    context = dict()
    context['last'] = last
    return render(request, template_name, context)


def contact(request):
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            sender = form.cleaned_data['sender']
            receiver = form.cleaned_data['receiver']
            postdate = form.cleaned_data['postdate']
            mail = EmailMessage('Django-mailing', text, sender, [receiver])
            form.save()
            let = Letter.objects.filter(id=form.save().id)
            LetterTread(mail, postdate, let).start()
        else:
            form = LetterForm(prefix='letters')
        return redirect('shipment:letter-list')
