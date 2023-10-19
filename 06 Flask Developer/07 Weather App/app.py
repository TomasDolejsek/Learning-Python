from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, render_template, request, redirect, url_for, flash
from os.path import exists
import sys
import requests


app = Flask(__name__)
app.secret_key = 'abc'
Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class DatabaseProcessor:
    def __init__(self):
        self.DATABASE_NAME = 'weather.db'
        engine = create_engine("sqlite:///" + self.DATABASE_NAME, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        if not exists(self.DATABASE_NAME):
            Base.metadata.create_all(engine)

    def get_city_names(self):
        query = self.session.query(City)
        return [x.name for x in query]

    def add_city(self, city_name):
        cities = self.get_city_names()
        if city_name in cities:
            return False
        self.session.add(City(id=len(cities) + 1, name=city_name))
        self.session.commit()
        return True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['city_name']
        check = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid=6e52c2b3e1a361f99484e92425c61b3f").json()
        if check['cod'] != 200:
            flash("City not found!")
            return redirect(url_for('index'))
        if not db.add_city(name):
            flash("City already exists!")
            return redirect(url_for('index'))
    cities = []
    for city in db.get_city_names():
        city_dict = dict()
        city_json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=6e52c2b3e1a361f99484e92425c61b3f").json()
        city_dict['city_name'] = city_json['name'].upper()
        city_dict['current_temp'] = int(city_json['main']['temp'])
        city_dict['weather_state'] = city_json['weather'][0]['main']
        cities.append(city_dict)
    return render_template('index.html', weathers=cities)


# don't change the following way to run flask:
if __name__ == '__main__':
    db = DatabaseProcessor()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
