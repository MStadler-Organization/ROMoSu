# Backend

## How to add new API endpoint

1. Create Model (=DB entity) in ```models.py```
2. (Register new model in ```admin.py```)
3. Migrate new model (see useful commands)
4. Create Serializer (transforms Models to JSON) in ```serializers.py```
5. Create View for actual logic of API call in ```views.py```
6. Add API endpoint to URLs in ``urls.py`` (depending on implementation in ```views.py```, respectively call function or
   with the router)
7. Run server and navigate to respective API endpoint

## Useful commands

### Run Server

```python manage.py runserver```

When using the above comamnd, Django starts two processes, one for the actual development server and other to reload
your application when the code changes. To run only single instance with no reload (necessary to not start multiple ROS
connectors):

```python manage.py runserver --noreload```

### Migrate after adding a new model

```python manage.py makemigrations quickstart```

```python manage.py migrate quickstart```

### Create dummy data for API testing

run ```python manage.py shell```

insert data:

```
from dj_server.quickstart.models import Hero

hero_1 = Hero(name="Superman", alias="SM")
hero_2 = Hero(name="Batman", alias="BM")


hero_1.save()
hero_2.save()
```

## Useful Links

https://www.django-rest-framework.org/tutorial/quickstart/

https://www.django-rest-framework.org/tutorial/1-serialization/

https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
