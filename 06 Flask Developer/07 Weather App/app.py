from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        city_dict = dict()
        city = request.form['city_name']
        city_json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=6e52c2b3e1a361f99484e92425c61b3f").json()
        city_dict['city_name'] = city_json['name'].upper()
        city_dict['current_temp'] = int(city_json['main']['temp'])
        city_dict['weather_state'] = city_json['weather'][0]['main']
        return render_template('index.html', weather=city_dict)
    else:
        return render_template('index.html')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
