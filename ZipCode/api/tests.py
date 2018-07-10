from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import UserEntry, ZipCodeCounter
from .serializers import UserEntry, UserEntrySerializer, ZipCodeCounterSerializer
from django.urls import reverse
from django.db.utils import IntegrityError
from django.db import transaction
from functools import reduce

factory = APIClient()

class ModelTest(object):
    rev_name = None
    model = None
    data = None
    expected_str = None

    '''test GET request'''
    def test_get(self):
        url = reverse(self.rev_name)
        response = factory.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) #test GET
    
    '''check if objects are instances of models'''
    def test_model(self):   
        _model = self.model.objects.create(**self.data)
        _model.save()
        self.assertIsInstance(_model, self.model)
    
    '''test __str__'''
    def test_str(self):
        _model = self.model(**self.data)
        self.assertEqual(str(_model), self.expected_str)


class SerializerTest(object):
    #don't test because we have None objects
    serializer = None
    model = None
    keys = None
    data = None
    
    '''test if serializer inherits fields properly'''
    def test_fields(self):
        _model = self.model.objects.create(**self.data)
        _serializer = self.serializer(instance=_model)
        data = _serializer.data
        self.assertCountEqual(data.keys(), self.keys)

    '''test is_valid() on serializers'''
    def test_validity(self):
        _serializer = self.serializer(data=self.data)
        self.assertTrue(_serializer.is_valid())


class UserEntryTest(APITestCase, ModelTest):
    rev_name = 'user_entries'
    model = UserEntry
    data = { 'zip': '22-222', 'email': 'test@test.com', 'name': 'John Smith' }
    expected_str = '22-222'

    def test_post(self):
        '''test POST Request'''
        url = reverse('user_entry_create')
        response = factory.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

        count = UserEntry.objects.count() #test if db updates properly
        self.assertEqual(count, 1)
 
        '''check if data hasn't changed during POST''' 
        created = UserEntry.objects.all()[0]
        self.assertEqual(created.zip, self.data['zip'])
        self.assertEqual(created.name, self.data['name'])
        self.assertEqual(created.email, self.data['email'])

        '''submit incorrect data format'''
        response = factory.post(url, { 'zip': '22-23f', 'name': 'John Smith', 'email': 'test2@test2.com' })
        bad_zip = self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        response = factory.post(url, { 'zip': '313-235', 'name': 'John Smith', 'email': 'test2@test2.com' })
        bad_zip = self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

        response = factory.post(url, { 'zip': '53-713', 'name': 'Three Piece Name', 'email': 'test@test@com' })
        bad_email = self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        response = factory.post(url, { 'zip': '62-912', 'name': 'Tomek123', 'email': 'test3@test3.com' })
        bad_name = self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    '''check if data has proper formats'''
    def test_data_formats(self):
        entry = self.model.objects.create(**self.data)
        self.assertEqual(len(entry.zip), 6)
        #only letters and spaces
        self.assertTrue(reduce(lambda x, y: x and y, [ ch.isalpha() or ch.isspace() for ch in entry.name]))

    '''test whether an exception is raised when one email address is submitted twice'''
    def test_email_uniqueness(self):
        dupl = self.model.objects.create(**self.data)
        self.assertRaises(IntegrityError)

class ZipCodeCounterTest(APITestCase, ModelTest):
    rev_name = 'zip_code_counter'
    model = ZipCodeCounter
    data = { 'zip_code': '22-222', 'counter': 5}
    expected_str = '22-222: 5'
    
    '''check if the counter increments properly upon adding a unique zip code'''
    def test_increment(self):
        UserEntry.objects.create(zip='22-222', email='test2@test2.com', name='John Smith')
        counter = ZipCodeCounter.objects.all()[0].counter
        self.assertEqual(counter, 1)

        #add another instance with the same zip, expect counter to be 2
        UserEntry.objects.create(zip='22-222', email='test5@test5.com', name='Tomek')
        counter = ZipCodeCounter.objects.all()[0].counter
        self.assertEqual(counter, 2)
    
class TestUserEntrySerializer(APITestCase, SerializerTest): 
    serializer = UserEntrySerializer
    model = UserEntry
    keys = ['id', 'zip', 'name', 'date', 'email']
    data = { 'zip': '22-222', 'email': 'test2@test2.com', 'name': 'Maciek' }
 

class TestZipCodeCounterSerializer(APITestCase, SerializerTest): 
    serializer = ZipCodeCounterSerializer
    model = ZipCodeCounter
    keys = ['id', 'zip_code', 'counter']
    data = { 'zip_code': '22-222', 'counter': 4 }


class TestURLS(APITestCase):
    def test_urls(self):
        '''test if reversed urls equal expected urls'''
        user_entry_create = reverse('user_entry_create')
        self.assertEqual(user_entry_create, '/api/entries/create/')
        
        zip_code_counter = reverse('zip_code_counter')
        self.assertEqual(zip_code_counter, '/api/zipcodecounter/')

        user_entries = reverse('user_entries')
        self.assertEqual(user_entries, '/api/entries/')
