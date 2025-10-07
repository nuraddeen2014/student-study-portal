from django.shortcuts import render, redirect
import requests
import wikipedia
from . forms import *
from django.contrib import messages
from django.views import generic
import yt_dlp
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f'Notes Added from {request.user.username} Successfully!')
        return redirect("notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username}!!')
            return redirect('homework')
    else:
        form = HomeworkForm()
    
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
                'homeworks':homework, 
               'homework_done':homework_done, 
               'form':form,
               }
    return render(request, 'dashboard/homework.html',context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
        results = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_url = f"ytsearch10:{text}"
            info = ydl.extract_info(search_url, download=False)
            for entry in info.get('entries', []):
                results.append({
                    'title': entry.get('title'),
                    'channel': entry.get('uploader'),
                    'link': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'thumbnail': entry.get('thumbnails', [{}])[0].get('url', ''),
                    'description': entry.get('description', ''),
                    'duration': entry.get('duration'),
                    'views': entry.get('view_count'),
                    'published': entry.get('upload_date'),
                })
        context = {'form': form, 'results': results}
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f'Todo added from {request.user.username}!!')
            return redirect('todo')
    else:
        form = TodoForm()
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todos': todos,
        'todos_done': todos_done
        
        }
    return render(request, 'dashboard/todo.html', context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    messages.success(request,f'Todo deleted from {request.user.username}!!')
    return redirect("todo")

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        r = requests.get(url)
        answer = r.json()
        results = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo'].get('title'),
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            results.append(result_dict)
            context = {'form': form, 'results': results}
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except:
            context = {'form': form, 'input': ""}
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)

def wiki(request):
    if request.method == "POST":
        try:
            text = request.POST['text']
            form = DashboardForm(request.POST)
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
            return render(request, 'dashboard/wiki.html', context)
        except wikipedia.exceptions.DisambiguationError as e:
            form = DashboardForm()
            context = {
                'form': form,
                'title': "The term is ambiguous, please be more specific",
                'details': e.options
            }
            return render(request, 'dashboard/wiki.html', context)
        
        except wikipedia.exceptions.PageError:
            form = DashboardForm()
            context = {
                'form': form,
                'title': "The page does not exist, please be more specific"
            }
            return render(request, 'dashboard/wiki.html', context)
        except Exception as e:
            form = DashboardForm()
            context = {
                'form': form,
                'title': "Something went wrong, please try again"
            }
            return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/wiki.html', context)

def conversion(request):
    answer = ''
    if request.method == "POST":
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')
        
        if measurement_type == 'length':
            m_form = ConversionLengthForm(request.POST)
            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'yard' and second == 'foot':
                    answer = f"{input_value} yard = {input_value*3} foot"
                if first == 'foot' and second == 'yard':
                    answer = f"{input_value} foot = {input_value/3} yard"

        elif measurement_type == 'mass':
            m_form = ConversionMassForm(request.POST)
            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'pound' and second == 'kilogram':
                    answer = f"{input_value} pound = {input_value*0.453592} kilogram"
                if first == 'kilogram' and second == 'pound':
                    answer = f"{input_value} kilogram = {input_value*2.20462} pound"

        elif measurement_type == 'volume':
            m_form = ConversionVolumeForm(request.POST)
            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'liter' and second == 'gallon':
                    answer = f"{input_value} liter = {input_value*0.264172} gallon"
                if first == 'gallon' and second == 'liter':
                    answer = f"{input_value} gallon = {input_value*3.78541} liter"

        elif measurement_type == 'currency':
            m_form = ConversionCurrencyForm(request.POST)
            if 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                # Example rates, adjust as needed
                if first == 'naira' and second == 'dollar':
                    answer = f"₦{input_value} = ${input_value/750:.2f}"
                if first == 'naira' and second == 'pound':
                    answer = f"₦{input_value} = £{input_value/930:.2f}"
                if first == 'dollar' and second == 'naira':
                    answer = f"${input_value} = ₦{input_value*750:.2f}"
                if first == 'pound' and second == 'naira':
                    answer = f"£{input_value} = ₦{input_value*930:.2f}"

        context = {
            'form': form,
            'm_form': m_form,
            'input': True,
            'answer': answer
        }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, 'dashboard/conversion.html', context)



"""@login_required
def profile(request):
    # Handle user update form (username, first/last name, email)
    from .forms import UserUpdateForm

    if request.method == 'POST' and 'update_profile' in request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    username = request.user.username
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'username': username,
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done,
        'user_form': user_form,
    }
    return render(request, 'dashboard/profile.html', context)"""


def logout_view(request):
    # Show confirmation on GET; perform logout on POST
    if request.method == 'POST':
        try:
            user_repr = f"{request.user.username} (id={request.user.id})"
        except Exception:
            user_repr = str(request.user)
        print(f"[logout_view] POST received. user before logout: {user_repr}")

        # Perform logout and clear session
        logout(request)
        try:
            request.session.flush()
        except Exception:
            pass

        messages.success(request, 'You have been logged out.')
        print(f"[logout_view] user after logout: {request.user}")
        return redirect('home')

    return render(request, 'dashboard/logout.html')


# -------------------- PROFILE DASHBOARD --------------------
@login_required
def profile_dashboard(request):
    user = request.user
    # Ensure UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    user_form = UserUpdateForm(instance=user)
    profile_form = UserProfileForm(instance=profile)

    # User todos & homeworks
    todos = Todo.objects.filter(user=user, is_finished=False)
    homeworks = Homework.objects.filter(user=user, is_finished=False)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "todos": todos,
        "homeworks": homeworks,
        "todos_done": not todos.exists(),
        "homework_done": not homeworks.exists(),
    }
    return render(request, "dashboard/profile.html", context)





# --- View ---
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure UserProfile is created
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, "Your account has been created successfully!")
            # Optionally auto-login user

            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'dashboard/register.html', {'form': form})
