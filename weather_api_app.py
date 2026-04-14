import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,QGraphicsOpacityEffect
from PyQt5.QtCore import Qt,QPropertyAnimation, QEasingCurve




class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Wprowadź nazwę miasta",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Sprawdź pogodę",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.desc_label=QLabel(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Pogodna aplikacja")

        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")
        self.apply_theme(True)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="" #tu wpisz swój api key
        city= self.city_input.text()
        url_weather=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response=requests.get(url_weather)
            response.raise_for_status()
            data= response.json()

            if data["cod"]==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nSpróbuj wpisać coś innego")
                case 401:
                    self.display_error("Unauthorized:\nZły klucz API")
                case 403:
                    self.display_error("Forbidden:\nBrak dostępu")
                case 404:
                    self.display_error("Not found:\nMiasto nie znalezione")
                case 500:
                    self.display_error("Internal Server Error:\nSpróbuj później")
                case 502:
                    self.display_error("Bad gateway:\nZła odpowiedź ze strony serwera")
                case 503:
                    self.display_error("Service unavailable:\nSerwer jest wyłączony")
                case 504:
                    self.display_error("Gateway timeout:\nBrak odpowiedzi ze stony serwera")
                case _:
                    self.display_error(f"HTTPError occured:\n{http_error}")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nSprawdź swoje połączenie")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nPolączenie zostało zerwane")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nsprawdź url")


    def translate_description(self, desc):
        translations = {
            "clear sky": "bezchmurnie",
            "few clouds": "lekkie zachmurzenie",
            "scattered clouds": "rozproszone chmury",
            "broken clouds": "pochmurno",
            "overcast clouds": "całkowite zachmurzenie",
            "light rain": "lekki deszcz",
            "moderate rain": "umiarkowany deszcz",
            "heavy intensity rain": "ulewa",
            "thunderstorm": "burza",
            "snow": "śnieg",
            "mist": "mgła"
        }
        return translations.get(desc.lower(), desc)
            
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.desc_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature_K=data["main"]["temp"]
        temperature_C=temperature_K-273.15
        self.temperature_label.setText(f"{temperature_C:.1f}°C")
        weather_description=self.translate_description(data["weather"][0]["description"])
        self.desc_label.setText(weather_description)
        weather_id=data["weather"][0]["id"]
        day = self.is_day(data)
        self.apply_theme(day)
        self.emoji_label.setText(self.get_weather_emoji(weather_id,day))
        

    def is_day(self,data):
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        current = data['dt']
       
        return sunrise <= current < sunset
        
    def apply_theme(self,is_day):
        if is_day:
            self.setStyleSheet("""
            QWidget{
                background-color: #F0F2F5;
                           }
            QLabel,QPushButton{
                font-family: calibri;
                color: #333333;
                background-color: #F0F2F5;
                           }
            QLabel#city_label{
                font-size:40px;
                font-style:italic;
                font-weight:bold;
                color: #000000;
                           }
            QLineEdit#city_input{
                font-size:40px;
                background-color: #F0F2F5;
                color: #000000;
                           }
            QPushButton#get_weather_button{
                font-size:30px;
                font-weight:bold;
                
                           }
            QLabel#temperature_label{
                font-size:75px;
                color: #000000;
                           }
            QLabel#emoji_label{
                font-size:80px;
                font-family:Segoe UI emoji;
                           }
            QLabel#desc_label{
                font-size:50px;
                color: #000000;
                           }
        """)
        else:
            self.setStyleSheet("""
            QWidget{
                background-color: #2C3E50;
                           }
            QLabel,QPushButton{
                font-family: calibri;
                color: #ECF0F1;
                background-color: #2C3E50;
                           }
            QLabel#city_label{
                font-size:40px;
                font-style:italic;
                font-weight:bold;
                           }
            QLineEdit#city_input{
                font-size:40px;
                background-color: #2C3E50;
                color: #ECF0F1;
                           }
            QPushButton#get_weather_button{
                font-size:30px;
                font-weight:bold;
                           }
            QLabel#temperature_label{
                font-size:75px;
                           }
            QLabel#emoji_label{
                font-size:80px;
                font-family:Segoe UI emoji;
                
                           }
            QLabel#desc_label{
                font-size:50px;
                           }
        """)


        

    def get_weather_emoji(self,weather_id,is_day):
        if 200<=weather_id<=232:
            return "🌩️"
        elif 300<=weather_id<=321 and is_day==True:
            return "🌥️"
        elif 300<=weather_id<=321 and is_day==False:
            return "☁️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "🌨️"
        elif 701<=weather_id<=741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800 and is_day==True:
            return "☀️" 
        elif weather_id == 800 and is_day==False:
            return "🌙"
        elif 801<=weather_id<=804:
            return "☁️"
        else:
            return " "

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())