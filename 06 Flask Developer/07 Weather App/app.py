from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, render_template, request, redirect, flash
from os.path import exists
import sys
import requests


app = Flask(__name__)
app.secret_key = "my very secret key"
Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class DatabaseProcessor:
    def __init__(self):
        self.DATABASE_NAME = 'weather.db'
        engine = create_engine("sqlite:///" + self.DATABASE_NAME, echo=False)
        self.session = sessionmaker(bind=engine)()
        if not exists(self.DATABASE_NAME):
            Base.metadata.create_all(engine)

    def get_cities(self):
        query = self.session.query(City)
        return [x for x in query]

    def add_city(self, city_id, city_name):
        city_ids = [x.id for x in self.get_cities()]
        if city_id in city_ids:
            return False
        self.session.add(City(id=city_id, name=city_name))
        self.session.commit()
        return True

    def delete_city(self, city_id):
        query = self.session.query(City)
        query.filter(City.id == city_id).delete()
        self.session.commit()


@app.route('/')
def index():
    cities = []
    for city in db.get_cities():
        city_dict = dict()
        city_json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid=6e52c2b3e1a361f99484e92425c61b3f").json()
        city_dict['id'] = city_json['id']
        city_dict['city_name'] = city_json['name'].upper()
        city_dict['current_temp'] = int(city_json['main']['temp'])
        city_dict['weather_state'] = city_json['weather'][0]['main']
        cities.append(city_dict)
    return render_template('index.html', weathers=cities)


@app.route('/add', methods=['POST'])
def add_city():
    city_name = request.form['city_name']
    r_json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid=6e52c2b3e1a361f99484e92425c61b3f").json()
    if r_json['cod'] != 200:
        flash("The city doesn't exist!")
    elif not db.add_city(r_json['id'], city_name.upper()):
        flash("The city has already been added to the list!")
    return redirect('/')


@app.route('/delete/<city_id>', methods=['POST'])
def delete_city(city_id):
    db.delete_city(city_id)
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    db = DatabaseProcessor()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
