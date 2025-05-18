import sys
import os
##import serial
import requests
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QComboBox, QTextEdit, QCalendarWidget, QMessageBox, QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# API anahtarı
OPENWEATHER_API_KEY = "d3ffd8c3bde1861e2cd020cfde8419ad"

def get_temperature(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data["main"]["temp"]
    except:
        return None
##def get_sensor_values(port='COM3', baudrate=9600, timeout=2):
    try:
      ##  with serial.Serial(port, baudrate, timeout=timeout) as ser:
          ##  line = ser.readline().decode().strip()
            # Örnek format: "SICAKLIK:25.6|TOPRAK_NEM:420"
            data_parts = line.split('|')
            temp = None
            soil = None
            for part in data_parts:
                if "SICAKLIK" in part:
                    temp = part.split(':')[1]
                elif "TOPRAK_NEM" in part:
                    soil = part.split(':')[1]
            return temp, soil
    except Exception as e:
        print("Hata:", e)
        return None, None


def generate_monthly_watering_schedule(sowing_date_str, crop_name):
    sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d")
    schedule = []
    current_date = sowing_date
    sowing_month = sowing_date.month

    while current_date.month == sowing_month:
        label = f"{current_date.strftime('%Y-%m-%d')} - {crop_name} sulama zamanı"
        schedule.append(label)
        current_date += timedelta(days=3)

    return schedule

HELP_DOCS = {
"Buğday": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Arpa": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Mısır": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Yulaf": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Çavdar": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Pirinç": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Nohut": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Mercimek": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Fasulye": "Aşılama: Gerekli değildir.\nBudama: Gerektiğinde yapılabilir.",
    "Bezelye": "Aşılama: Gerekli değildir.\nBudama: Gerektiğinde yapılabilir.",
    "Bakla": "Aşılama: Gerekli değildir.\nBudama: Gerektiğinde yapılabilir.",
    "Domates": "Aşılama: Fideler 30 günlük olduğunda aşılama yapılabilir.\nBudama: Yan sürgünler düzenli olarak alınmalıdır.",
    "Biber": "Aşılama: Fideler 25-30 günlükken yapılabilir.\nBudama: İlk meyvelerden sonra dip sürgünler temizlenmelidir.",
    "Patlıcan": "Aşılama: 30 gün sonra.\nBudama: Gerektiğinde yapılabilir.",
    "Salatalık": "Aşılama: Gerekli değildir.\nBudama: Ana gövde dışındaki yan sürgünler budanabilir.",
    "Kabak": "Aşılama: Gerekli değildir.\nBudama: Ana gövde dışındaki sürgünler alınabilir.",
    "Havuç": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Ispanak": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Lahana": "Aşılama: Gerekli değildir.\nBudama: Sararan yapraklar alınmalıdır.",
    "Pırasa": "Aşılama: Gerekli değildir.\nBudama: Gerektiğinde sarı yapraklar alınabilir.",
    "Marul": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Soğan": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Sarımsak": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Patates": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Turp": "Aşılama: Gerekli değildir.\nBudama: Uygulanmaz.",
    "Karnabahar": "Aşılama: Gerekli değildir.\nBudama: Sararan yapraklar alınmalıdır.",
    "Brokoli": "Aşılama: Gerekli değildir.\nBudama: Hasattan sonra yan sürgünler alınabilir.",
    "Roka": "Aşılama: Gerekli değildir.\nBudama: Sık çıkarsa seyreltme yapılabilir.",
    "Maydanoz": "Aşılama: Gerekli değildir.\nBudama: Hasattan sonra düzenli biçilmelidir."
}

def get_help_doc(crop_name):
    return HELP_DOCS.get(crop_name, "Bu ekin için henüz bilgi yok.")

class EkinTakipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ekin Takip Uygulaması")
        self.setGeometry(100, 100, 800, 700)
        self.initUI()

    def initUI(self):
        title = QLabel("🌱 Ekin Takip Uygulaması")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        self.sensor_temp_label = QLabel("ETU devresi ile elde edilen sıcaklık değeri: -")
        self.sensor_soil_label = QLabel("ETU devresi ile elde edilen toprak nem değeri: -")
        self.sensor_temp_label.setFont(QFont("Arial", 10))
        self.sensor_soil_label.setFont(QFont("Arial", 10))


        self.city_input = QComboBox()
        self.city_input.addItems([  "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya",
            "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
            "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne",
            "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
            "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu",
            "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya",
            "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
            "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
            "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray",
            "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır",
            "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"])

        self.crop_input = QComboBox()
        self.crop_list = ["Buğday", "Arpa", "Mısır", "Yulaf", "Çavdar", "Pirinç", "Nohut", "Mercimek",
            "Fasulye", "Bezelye", "Bakla", "Domates", "Biber", "Patlıcan", "Salatalık",
            "Kabak", "Havuç", "Ispanak", "Lahana", "Pırasa", "Marul", "Soğan", "Sarımsak",
            "Patates", "Turp", "Karnabahar", "Brokoli", "Roka", "Maydanoz", "Elma", "Armut",
            "Şeftali", "Erik", "Kayısı", "Kiraz", "Vişne", "Üzüm", "Nar", "Ayva", "İncir",
            "Muz", "Kivi", "Portakal", "Mandalina", "Limon", "Greyfurt", "Ceviz", "Fındık",
            "Badem", "Zeytin", "Ayçiçeği", "Kanola", "Soya", "Yer fıstığı", "Pamuk",
            "Şeker pancarı", "Tütün", "Kenevir", "Çay", "Nane", "Kekik", "Adaçayı", "Rezene",
            "Lavanta", "Melisa", "Çemen otu", "Serada Domates", "Serada Salatalık",
            "Serada Biber", "Serada Marul", "Serada Çilek", "Serada Fasulye"]
        self.crop_input.addItems(self.crop_list)

        self.calendar = QCalendarWidget()
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        self.notification_label = QLabel("")
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setFont(QFont("Arial", 10))
        self.notification_label.setStyleSheet("color: green")

        self.generate_button = QPushButton("📅 Takvimimi Oluştur")
        self.generate_button.clicked.connect(self.create_schedule)

        self.weather_button = QPushButton("🌤️ Hava Durumu Kontrol Et")
        self.weather_button.clicked.connect(self.check_weather)

        self.view_button = QPushButton("📂 Takvimimi Görüntüle")
        self.view_button.clicked.connect(self.view_schedule)

        self.reset_button = QPushButton("🗑️ Takvimimi Sıfırla")
        self.reset_button.clicked.connect(self.reset_schedule)
        self.sensor_button = QPushButton("🔎 Sensör Verilerini Oku")
        self.sensor_button.clicked.connect(self.read_sensor_data)


        help_title = QLabel("📖 Yardımcı Dökümanlar")
        help_title.setFont(QFont("Arial", 14))
        help_title.setAlignment(Qt.AlignCenter)

        self.help_search_input = QLineEdit()
        self.help_search_input.setPlaceholderText("Ekin adı ile ara (örn: Domates)")
        self.help_search_input.returnPressed.connect(self.show_help_doc)

        self.help_search_button = QPushButton("🔍 Ara")
        self.help_search_button.clicked.connect(self.show_help_doc)

        self.help_result_area = QTextEdit()
        self.help_result_area.setReadOnly(True)

        help_search_layout = QHBoxLayout()
        help_search_layout.addWidget(self.help_search_input)
        help_search_layout.addWidget(self.help_search_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(QLabel("📍 Şehir Seçiniz:"))
        layout.addWidget(self.city_input)
        layout.addWidget(QLabel("🌾 Ekin Seçiniz:"))
        layout.addWidget(self.crop_input)
        layout.addWidget(QLabel("📅 Ekim Tarihini Seçiniz:"))
        layout.addWidget(self.calendar)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.weather_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.sensor_button)
        layout.addWidget(self.sensor_temp_label)
        layout.addWidget(self.sensor_soil_label)
        layout.addWidget(QLabel("📌 Bilgilendirme:"))
        layout.addWidget(self.notification_label)
        layout.addWidget(QLabel("📋 Takvimim:"))
        layout.addWidget(self.result_area)
        layout.addSpacing(20)
        layout.addWidget(help_title)
        layout.addLayout(help_search_layout)
        layout.addWidget(self.help_result_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_schedule(self):
        crop = self.crop_input.currentText()
        city = self.city_input.currentText()
        sowing_date = self.calendar.selectedDate().toString("yyyy-MM-dd")

        watering_schedule = generate_monthly_watering_schedule(sowing_date, crop)

        output = (
            f"🌾 Ekin: {crop}\n"
            f"📍 Şehir: {city}\n"
            f"📅 Ekim Tarihi: {sowing_date}\n\n"
            f"💧 Sulama Takvimi:\n- " + "\n- ".join(watering_schedule)
        )

        try:
            with open("takvimim.txt", "w", encoding="utf-8") as file:
                file.write(output)
            self.result_area.setText(output)
            self.notification_label.setText("✅ Takviminiz başarıyla oluşturuldu!")
        except Exception as e:
            self.notification_label.setText(f"Hata: {str(e)}")
            
    def read_sensor_data(self):
             self.sensor_temp_label.setText(f"ETU devresi ile elde edilen sıcaklık değeri:- °C")
             self.sensor_soil_label.setText(f"ETU devresi ile elde edilen toprak nem değeri: -")
         

    def view_schedule(self):
        try:
            if os.path.exists("takvimim.txt"):
                with open("takvimim.txt", "r", encoding="utf-8") as file:
                    content = file.read()
                    self.result_area.setText(content)
                    self.notification_label.setText("📄 Takviminiz yüklendi.")
            else:
                self.result_area.setText("Henüz bir takvim oluşturmadınız.")
                self.notification_label.setText("ℹ️ Görüntülenecek takvim bulunamadı.")
        except Exception as e:
            self.notification_label.setText(f"Hata: {str(e)}")

    def reset_schedule(self):
        try:
            if os.path.exists("takvimim.txt"):
                os.remove("takvimim.txt")
                self.result_area.clear()
                self.notification_label.setText("🗑️ Takviminiz sıfırlandı.")
            else:
                self.notification_label.setText("🚫 Sıfırlanacak takvim bulunamadı.")
        except Exception as e:
            self.notification_label.setText(f"Hata: {str(e)}")

    def check_weather(self):
        city = self.city_input.currentText()
        temperature = get_temperature(city)
        if temperature is None:
            self.notification_label.setText("🌥️ Hava durumu alınamadı.")
        elif temperature > 30:
            self.notification_label.setText(f"🌡️ {city} için sıcaklık {temperature}°C. Daha fazla sulama önerilir.")
        else:
            self.notification_label.setText(f"🌤️ {city} için sıcaklık {temperature}°C. Şu an için ideal.")

    def show_help_doc(self):
        search_text = self.help_search_input.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir ekin adı girin.")
            return

        matched = None
        for ekin in self.crop_list:
            if ekin.lower() == search_text.lower():
                matched = ekin
                break

        if matched:
            info = get_help_doc(matched)
            self.help_result_area.setText(f"📖 {matched} hakkında bilgi:\n\n{info}")
        else:
            self.help_result_area.setText("❌ Aradığınız ekin bulunamadı.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EkinTakipApp()
    window.show()
    sys.exit(app.exec_())
