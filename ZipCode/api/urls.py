from django.urls import path, re_path
from .views import UserEntryPost, UserEntries, ZipCodeCounters, UserEntry, ZipCodeCounter


urlpatterns = [
    path('entries/create/', UserEntryPost.as_view(), name='user_entry_create'),
    path('entries/', UserEntries.as_view(), name='user_entries'),
    path('counters/', ZipCodeCounters.as_view(), name='zip_code_counters'),
    re_path(r'counter/(?P<pk>[0-9]+)/$', ZipCodeCounter.as_view(), name='zip_code_counter'),
    re_path(r'^entry/(?P<pk>[0-9]+)/$', UserEntry.as_view(), name='user_entry'), 
    
]