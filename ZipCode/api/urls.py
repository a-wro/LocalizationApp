from django.urls import path
from .views import UserEntryPost, UserEntries, ZipCodeCounters


urlpatterns = [
    path('entries/create/', UserEntryPost.as_view(), name='user_entry_create'),
    path('entries/', UserEntries.as_view(), name='user_entries'),
    path('zipcodecounter/', ZipCodeCounters.as_view(), name='zip_code_counter'),
]