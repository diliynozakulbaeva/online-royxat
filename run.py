import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Render PORT muhit o'zgaruvchisidan foydalanadi, u yo'q bo'lsa 5000 ni oladi
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' saytni tashqaridan kirishga ochib beradi
    app.run(host='0.0.0.0', port=port)