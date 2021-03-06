"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Question, Choice, User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm, UserForm, SubjectFilterForm
from django.shortcuts import redirect
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

def index(request):

    latest_question_list = Question.objects.order_by('-pub_date')
    filtered_subject = None

    if request.method == "POST":
        form = SubjectFilterForm(request.POST)
        if form.is_valid:
            filtered_subject = request.POST.get('subjects', None)
            if filtered_subject:
                latest_question_list.filter(subject=filtered_subject)
    else:
        form = SubjectFilterForm()

    error_message = form.errors or None # Form not submitted or it has errors
    return render(request, 'polls/index.html', {
        'title': 'Lista de preguntas de la encuesta',
        'latest_question_list': latest_question_list,
        'form': form,
        'filtered_subject': filtered_subject,
        'error_message': error_message,
    })

def update_questions(request):

    latest_question_list = Question.objects.order_by('-pub_date')

    filtered_subject = request.GET.get('subjects', None)
    if filtered_subject:
        latest_question_list.filter(subject=filtered_subject)

    data = {
        'latest_question_list': latest_question_list,
        'filtered_subject': filtered_subject
    }
    return render(request, 'polls/index.html', data)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:', 'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:', 'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form.  Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))

def question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():

            question = form.save(commit=False)

            if question.correct_answer > question.number_responses:
                return render(request, 'polls/question_new.html', {'form': form, 'error_message': 'The correct answer number must be an existing one.'})
            
            question.pub_date = datetime.now()
            question.save()
            #return redirect('detail', pk=question_id)
            #return render(request, 'polls/index.html', {'title':'Respuestas
            #posibles','question': question})
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):

    question = Question.objects.get(id = question_id)
    is_correct_choice = question.correct_answer == question.choice_set.count() + 1

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit = False)
            choice.is_correct_answer = is_correct_choice
            choice.question = question
            choice.vote = 0
            choice.save()         
            #form.save()
            # Redirect to the same page, clearing the form in the process
            return HttpResponseRedirect('')
    else: 
        form = ChoiceForm()

    if question.choice_set.count() < question.number_responses:
        #return render_to_response ('choice_new.html', {'form': form,
        #'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text, 'form': form, 'is_correct_choice': is_correct_choice})
    else:
        return HttpResponseRedirect('index')

def chart(request, question_id):
    q = Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html',
                #{'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)