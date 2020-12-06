# watson

utility application to gather data from webpages and get basic analytics

## Getting Started

```
git clone https://github.com/Circles24/watson
```

### Prerequisites
* python3
* rabbitmq

### Installing

```
cd watson
pip install -r requirements.txt
sudo apt-get install rabbitmq-server
python manage.py migrate
python manage.py runserver
celery -A watson worker
```

## Built With

* [Django](https://www.djangoproject.com/) 
* [Celery](https://docs.celeryproject.org/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

