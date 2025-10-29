from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
        if 'create_group' in request.POST:
            group_form = NotesGroupForm(request.POST)
            if group_form.is_valid():
                group = group_form.save(commit=False)
                group.user = request.user
                group.save()
                messages.success(request, f"Group '{group.name}' created successfully!")
                return redirect('notes')
        else:
            form = NotesForm(request.POST, request.FILES)
            if form.is_valid():
                notes = form.save(commit=False)
                notes.user = request.user
                notes.save()
                messages.success(request, f"Note '{notes.title}' added successfully!")
                return redirect('notes')
    
    notes = Notes.objects.filter(user=request.user).order_by('-created_at')
    groups = NotesGroup.objects.filter(user=request.user)
    form = NotesForm()
    group_form = NotesGroupForm()
    
    # Filter by group if specified
    group_id = request.GET.get('group')
    if group_id:
        notes = notes.filter(group_id=group_id)
        active_group = get_object_or_404(NotesGroup, id=group_id, user=request.user)
    else:
        active_group = None
    
    context = {
        'notes': notes,
        'form': form,
        'groups': groups,
        'group_form': group_form,
        'active_group': active_group
    }
    return render(request, 'dashboard/notes.html', context)


@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk, user=request.user).delete()
    messages.success(request, "Note deleted successfully!")
    return redirect("notes")

@login_required
def delete_notes_group(request, pk=None):
    group = get_object_or_404(NotesGroup, id=pk, user=request.user)
    group_name = group.name
    group.delete()
    messages.success(request, f"Group '{group_name}' deleted successfully!")
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    context_object_name = 'note'

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

import requests
from django.shortcuts import render
from django.conf import settings
from decimal import Decimal, InvalidOperation
from .forms import DashboardForm

def books(request):
    results = []
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            r = requests.get(url)
            answer = r.json()

            #  Check if 'items' exists in response
            if 'items' in answer:
                for item in answer['items'][:10]:  # Limit to 10
                    volume_info = item.get('volumeInfo', {})
                    result_dict = {
                        'title': volume_info.get('title', 'No title available'),
                        'subtitle': volume_info.get('subtitle', ''),
                        'description': volume_info.get('description', ''),
                        'count': volume_info.get('pageCount', 'Unknown'),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 'No rating'),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
                        'preview': volume_info.get('previewLink', '#'),
                    }
                    results.append(result_dict)
            else:
                # If no results were found
                results = []
                message = "No books found for your search query."
                return render(request, 'dashboard/books.html', {'form': form, 'message': message})
    else:
        form = DashboardForm()

    return render(request, 'dashboard/books.html', {'form': form, 'results': results})


def dictionary(request):
    try:
        if request.method == "POST":
            form = DashboardForm(request.POST)
            text = request.POST.get('text', '').strip()

            if not text:
                messages.error(request, "Please enter a word to search.")
                return redirect('dictionary')

            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"

            try:
                r = requests.get(url, timeout=6)
                r.raise_for_status()
                answer = r.json()

                # When API returns a valid result
                if isinstance(answer, list) and len(answer) > 0:
                    phonetics = answer[0].get('phonetics', [{}])[0].get('text', '')
                    audio = answer[0].get('phonetics', [{}])[0].get('audio', '')
                    definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'No definition available.')
                    example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'No example available.')
                    synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

                    context = {
                        'form': form,
                        'input': text,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms,
                    }
                else:
                    messages.error(request, f"No results found for '{text}'.")
                    return redirect('dictionary')

            except requests.exceptions.HTTPError:
                messages.error(request, f"No results found for '{text}'.")
                return redirect('dictionary')
            except requests.exceptions.RequestException:
                messages.error(request, "Failed to fetch data from the dictionary API. Please try again later.")
                return redirect('dictionary')

            return render(request, 'dashboard/dictionary.html', context)

        else:
            form = DashboardForm()
            context = {'form': form}
            return render(request, 'dashboard/dictionary.html', context)

    except requests.exceptions.ConnectionError:
        messages.error(request, "No internet connection. Please check your connection and try again.")
        return redirect('dictionary')


def wiki(request):
    if request.method == "POST":
        text = request.POST.get('text', '').strip()
        form = DashboardForm(request.POST)

        if not text:
            context = {
                'form': form,
                'title': "Please enter a valid search term."
            }
            return render(request, 'dashboard/wiki.html', context)

        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary,
                'is_disambiguation': False
            }
            return render(request, 'dashboard/wiki.html', context)

        except wikipedia.exceptions.DisambiguationError as e:
            context = {
                'form': form,
                'title': "The term is ambiguous, please be more specific",
                'details': e.options,
                'is_disambiguation': True
            }
            return render(request, 'dashboard/wiki.html', context)

        except wikipedia.exceptions.PageError:
            context = {
                'form': form,
                'title': "The page does not exist, please try again"
            }
            return render(request, 'dashboard/wiki.html', context)

        except (requests.exceptions.ConnectionError, wikipedia.exceptions.HTTPTimeoutError):
            context = {
                'form': form,
                'title': "Connection error: please check your internet connection and try again."
            }
            return render(request, 'dashboard/wiki.html', context)

        except Exception as e:
            context = {
                'form': form,
                'title': "Something went wrong, please try again."
            }
            return render(request, 'dashboard/wiki.html', context)

    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/wiki.html', context)

def conversion(request):
    answer = ''
    converted_amount = None
    if request.method == "POST":
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')
        action = request.POST.get('action', 'select')
        do_convert = (action == 'convert')
        
        if measurement_type == 'length':
            # Only bind the specific sub-form when performing the conversion to avoid showing
            # "This field is required" validation messages when user only selects the tool.
            if do_convert:
                m_form = ConversionLengthForm(request.POST)
            else:
                # preserve selections if present but do not bind
                initial = {}
                if 'measure1' in request.POST:
                    initial['measure1'] = request.POST.get('measure1')
                if 'measure2' in request.POST:
                    initial['measure2'] = request.POST.get('measure2')
                m_form = ConversionLengthForm(initial=initial)

            if do_convert and 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'yard' and second == 'foot':
                    answer = f"{input_value} yard = {input_value*3} foot"
                if first == 'foot' and second == 'yard':
                    answer = f"{input_value} foot = {input_value/3} yard"

        elif measurement_type == 'mass':
            if do_convert:
                m_form = ConversionMassForm(request.POST)
            else:
                initial = {}
                if 'measure1' in request.POST:
                    initial['measure1'] = request.POST.get('measure1')
                if 'measure2' in request.POST:
                    initial['measure2'] = request.POST.get('measure2')
                m_form = ConversionMassForm(initial=initial)

            if do_convert and 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'pound' and second == 'kilogram':
                    answer = f"{input_value} pound = {input_value*0.453592} kilogram"
                if first == 'kilogram' and second == 'pound':
                    answer = f"{input_value} kilogram = {input_value*2.20462} pound"

        elif measurement_type == 'volume':
            if do_convert:
                m_form = ConversionVolumeForm(request.POST)
            else:
                initial = {}
                if 'measure1' in request.POST:
                    initial['measure1'] = request.POST.get('measure1')
                if 'measure2' in request.POST:
                    initial['measure2'] = request.POST.get('measure2')
                m_form = ConversionVolumeForm(initial=initial)

            if do_convert and 'input' in request.POST and request.POST['input']:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = float(request.POST['input'])
                if first == 'liter' and second == 'gallon':
                    answer = f"{input_value} liter = {input_value*0.264172} gallon"
                if first == 'gallon' and second == 'liter':
                    answer = f"{input_value} gallon = {input_value*3.78541} liter"

        elif measurement_type == 'currency':
            # bind currency form only when converting to avoid premature validation errors
            if do_convert:
                m_form = ConversionCurrencyForm(request.POST)
            else:
                initial = {}
                if 'from_currency' in request.POST:
                    initial['from_currency'] = request.POST.get('from_currency')
                if 'to_currency' in request.POST:
                    initial['to_currency'] = request.POST.get('to_currency')
                if 'amount' in request.POST:
                    initial['amount'] = request.POST.get('amount')
                m_form = ConversionCurrencyForm(initial=initial)
            # Simple ExchangeRate-API implementation: compute converted_amount on Convert
            converted_amount = None
            from_curr = request.POST.get('from_currency') or request.POST.get('measure1')
            to_curr = request.POST.get('to_currency') or request.POST.get('measure2')
            try:
                amount_raw = request.POST.get('amount', '')
                if do_convert:
                    # Basic validation
                    if not amount_raw:
                        converted_amount = 'Please enter a valid amount.'
                    else:
                        try:
                            amt = float(amount_raw)
                        except (ValueError, TypeError):
                            converted_amount = 'Please enter a valid numeric amount.'
                        else:
                            api_key = getattr(settings, 'EXCHANGE_RATE_API_KEY', '')
                            if not api_key:
                                converted_amount = 'Exchange rate API key not configured.'
                            else:
                                base_url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/'
                                url = f"{base_url}{from_curr}"
                                try:
                                    r = requests.get(url, timeout=6)
                                    data = r.json()
                                except requests.exceptions.RequestException as e:
                                    converted_amount = f'API request failed: {e}'
                                else:
                                    if data.get('result') == 'success' and 'conversion_rates' in data:
                                        rates = data['conversion_rates']
                                        rate = rates.get(to_curr)
                                        if rate is None:
                                            converted_amount = f'No conversion rate from {from_curr} to {to_curr}.'
                                        else:
                                            value = round(amt * float(rate), 2)
                                            converted_amount = f"{value} {to_curr}"
                                    else:
                                        msg = data.get('error-type') or data.get('message') or str(data)
                                        converted_amount = f'Error fetching rates: {msg}'
                else:
                    converted_amount = None
            except Exception as e:
                converted_amount = f'An unexpected error occurred: {e}'

        context = {
            'form': form,
            'm_form': m_form,
            'input': True,
            'answer': answer,
            'converted_amount': converted_amount,
            'from_currency': request.POST.get('from_currency') or request.POST.get('measure1'),
            'to_currency': request.POST.get('to_currency') or request.POST.get('measure2'),
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
