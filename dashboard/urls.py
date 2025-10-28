from django.urls import path
from . import views
from .views import NotesDetailView

urlpatterns = [
    path('', views.home, name='home'),

    path('notes/', views.notes, name='notes'),
    path('notes/<int:pk>/', NotesDetailView.as_view(), name='notes-detail'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete-note'),
    path('notes/group/delete/<int:pk>/', views.delete_notes_group, name='delete-notes-group'),

    path('homework/', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),

    path('youtube/', views.youtube, name='youtube'),

    path('todo/', views.todo, name='todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),

    path('books/', views.books, name='books'),

    path('dictionary/', views.dictionary, name='dictionary'),

    path('wiki/', views.wiki, name='wiki'),
    
    path('conversion/', views.conversion, name='conversion'),
    path('profile/', views.profile_dashboard, name='profile'),
    
    

]
 