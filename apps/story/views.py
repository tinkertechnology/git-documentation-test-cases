import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import StoryForm, CommentForm
from .models import Story, Vote, Comment, Project

from django.http import HttpResponse
from django.core.paginator import Paginator
import pdfkit
from django.template.loader import get_template

@login_required
def frontpage(request):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    projects = Project.objects.all()
    stories = Story.objects.filter(created_at__gte=date_from).order_by('-number_of_votes')[0:30]

    return render(request, 'story/frontpage.html', {'stories': stories, 'projects' : projects })

@login_required
def listing(request, project_id):
    storiesi = Story.objects.filter(fk_project_id=project_id)
    p = Paginator(storiesi, 10)
    page_number = request.GET.get('page')
    try:
        stories = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        stories = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        stories = p.page(p.num_pages)
    projects = Project.objects.all()
    return render(request, 'story/listing.html', {'stories': stories, 'projects' : projects, 'project_ver': project_id})

@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        stories = Story.objects.filter(title__icontains=query)
    else:
        stories = []
    
    return render(request, 'story/search.html', {'stories': stories, 'query': query})

def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    stories = Story.objects.all().order_by('-title')[:5]
 
    return render(request, 'story/detail.html', {'story': story, 'stories': stories})

def newest(request):
    stories = Story.objects.all()[0:200]

    return render(request, 'story/newest.html', {'stories': stories})

@login_required
def vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    next_page = request.GET.get('next_page', '')

    if story.created_by != request.user and not Vote.objects.filter(created_by=request.user, story=story):
        vote = Vote.objects.create(story=story, created_by=request.user)
    
    if next_page == 'story':
        return redirect('story', story_id=story_id)
    else:
        return redirect('frontpage')

@login_required
def submit(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()

            return redirect('frontpage')
    else:
        form = StoryForm()

    return render(request, 'story/submit.html', {'form': form})





def viewPDFInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Settings.objects.all().first()

    #Calculate the Invoice Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    return render(request, 'invoice/invoice-template.html', context)

from django_sql_query_to_excel import SqlQueryToExcel
def test_sql(request):
    return SqlQueryToExcel.query_to_excel("select 1")
    pass

def printAllVersions(request, projectID):
    #fetch that invoice
    try:
        versions = Story.objects.filter(fk_project_id=projectID).order_by('title')
        pass
    except:
        pass
        # messages.error(request, 'Something went wrong')
        # return redirect('invoices')

    #fetch all the products - related to this invoice
    # products = Product.objects.filter(invoice=invoice)

    # #Get Client Settings
    # p_settings = Settings.objects.all().first()

    # #Calculate the Invoice Total
    # invoiceTotal = 0.0
    # if len(products) > 0:
    #     for x in products:
    #         y = float(x.quantity) * float(x.price)
    #         invoiceTotal += y



    context = {}
    context['versions'] = versions
    # context['products'] = products
    # context['p_settings'] = p_settings
    # context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(versions.first().fk_project.title)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('story/pdf_template_all.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    #IF you have CSS to add to template
    # css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response



def viewPDFInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Settings.objects.all().first()

    #Calculate the Invoice Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    return render(request, 'invoice/invoice-template.html', context)



def viewDocumentInvoice(request, versionID):
    #fetch that invoice
    try:
        version = Story.objects.get(pk=versionID)
        pass
    except:
        pass
        # messages.error(request, 'Something went wrong')
        # return redirect('invoices')

    #fetch all the products - related to this invoice
    # products = Product.objects.filter(invoice=invoice)

    # #Get Client Settings
    # p_settings = Settings.objects.all().first()

    # #Calculate the Invoice Total
    # invoiceTotal = 0.0
    # if len(products) > 0:
    #     for x in products:
    #         y = float(x.quantity) * float(x.price)
    #         invoiceTotal += y



    context = {}
    context['version'] = version
    # context['products'] = products
    # context['p_settings'] = p_settings
    # context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(version.title)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('story/pdf_template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    #IF you have CSS to add to template
    # css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response