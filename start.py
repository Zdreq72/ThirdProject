import os

print("📌 Running migrations...")
os.system("python SaudiEstate/manage.py migrate")

print("📌 Collecting static files...")
os.system("python SaudiEstate/manage.py collectstatic --noinput")

print("🚀 Starting Gunicorn...")
os.system("gunicorn SaudiEstate.wsgi:application --bind 0.0.0.0:8000")
