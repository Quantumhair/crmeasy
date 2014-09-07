from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .models import Contact
from .forms import ContactForm
from crmapp.accounts.models import Account


@login_required()
def contact_detail(request, uuid):

    contact = Contact.objects.get(uuid=uuid)

    return render(request, 
                'contacts/contact_detail.html', 
                {'contact': contact}
    )

@login_required()
def contact_cru(request, uuid=None, account=None):

    if uuid:
        contact = get_object_or_404(Contact, uuid=uuid)
        if contact.owner != request.user:
            return HttpResponseForbidden()
    else:
        contact = Contact(owner=request.user)

    if request.POST:
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            # make sure the user owns the account
            account = form.cleaned_data['account']
            if account.owner != request.user:
                return HttpResponseForbidden()
            # save the data
            form.save()
            # return the user to the account detail view
            reverse_url = reverse(
                'crmapp.accounts.views.account_detail',
                args=(account.uuid,)
            )
            return HttpResponseRedirect(reverse_url)
    else:
        form = ContactForm(instance=contact)

    # this is used to render the account in the template
    if request.GET.get('account', ''):
        account = Account.objects.get(id=request.GET.get('account', ''))

    variables = {
        'form': form,
        'contact': contact,
        'account': account
    }

    template = 'contacts/contact_cru.html'

    return render(request, template, variables)
