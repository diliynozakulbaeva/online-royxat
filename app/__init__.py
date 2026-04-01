from flask import Flask
from .database import db
import os

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(__name__,
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_queue.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'bank-queue-secret'

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _seed_data()  # ← bu yerda chaqiriladi

    return app

def _seed_data():  # ← create_app() DAN TASHQARIDA, lekin bir xil faylda
    from .models import Branch, Service
    if not Branch.query.first():
        branches = [
            Branch(name="Asakabank - Nukus filial", code="A"),
            Branch(name="SQB Bank - Nukus filial", code="B"),
            Branch(name="Aloqabank - Nukus filial", code="C"),
            Branch(name="Xalq Banki - Nukus filial", code="D"),
        ]
        db.session.add_all(branches)
        db.session.commit()

    if not Service.query.first():
        services = [
            # 1. Kassa amallari
            Service(name="Naqd pul qabul qilish (kiritish)", duration=5),
            Service(name="Naqd pul berish (olish)", duration=5),
            Service(name="Valyuta ayirboshlash", duration=10),
            Service(name="To'lovlar (kommunal, soliq va b.)", duration=5),

            # 2. Kartaga xizmat ko'rsatish
            Service(name="Kartani qayta tiklash / almashtirish", duration=15),
            Service(name="Kartani blokrovkadan ochish", duration=10),
            Service(name="PIN-kodni o'zgartirish", duration=10),

            # 3. Xalqaro va mahalliy pul o'tkazmalari
            Service(name="Bank ichki o'tkazmalari", duration=10),
            Service(name="Western Union / MoneyGram o'tkazmasi", duration=15),
            Service(name="Contact / Unistream o'tkazmasi", duration=15),
            Service(name="Zolotaya Korona / RIA o'tkazmasi", duration=15),

            # 4. Kredit mahsulotlari
            Service(name="Iste'mol krediti bo'yicha murojaat", duration=20),
            Service(name="Kredit to'lovi", duration=10),
            Service(name="Kredit olish (maslahat)", duration=20),

            # 5. Depozitlar
            Service(name="Depozit ochish / yopish", duration=15),
            Service(name="Foizlarni olish", duration=10),

            # 6. Hisob-kitob va ko'chirmalar
            Service(name="Hisobvaraqdan ko'chirma olish", duration=10),
            Service(name="Hisobvaraq ochish", duration=15),

            # 7. Boshqa xizmatlar
            Service(name="Ipoteka bo'yicha maslahat", duration=30),
            Service(name="Yuridik shaxslarga xizmat ko'rsatish", duration=30),
            Service(name="Umumiy maslahat / Yordamchi xodimga murojaat", duration=10),
        ]
        db.session.add_all(services)
        db.session.commit()