Compilation and running (UNIX, Python 3):

Create a virtual environment:
``` 
python3 -m venv my_venv
cd my_venv
source bin/activate  
``` 
Then:
``` 
git clone https://github.com/a-wro/LocalizationApp.git  
cd LocalizationApp/ZipCode  
pip install -r requirements.txt  
python3 manage.py runserver  
``` 

If port is taken run with:
``` python3 manage.py runserver localhost:8888 ``` 
(or any other free port)

the endpoints are:
```
/api/entries/
/api/entry/create/
/api/counters/
/api/counter/{zipcode}/
```
