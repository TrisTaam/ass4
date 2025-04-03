@echo off
echo ===== Django E-Commerce Microservices Deployment =====
echo.

:: Create requirements.txt if it doesn't exist
if not exist requirements.txt (
    echo Creating requirements.txt...
    echo Django==4.2.7 > requirements.txt
    echo djangorestframework==3.14.0 >> requirements.txt
    echo requests==2.31.0 >> requirements.txt
    echo python-dotenv==1.0.0 >> requirements.txt
    echo Pillow==10.1.0 >> requirements.txt
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt
pip install djangorestframework

:: Verify installations
echo Verifying installations...
pip list

:: Set environment variables
echo Setting environment variables...
set DJANGO_SETTINGS_MODULE=ecommerce.settings
set PYTHONPATH=%cd%

:: Verify Django installation
echo Verifying Django installation...
python -m pip install django

:: Create database tables for each service
echo Creating database tables...

:: Main service
echo Setting up main service...
python manage.py makemigrations
python manage.py migrate

:: Customer service
echo Setting up customer service...
cd customer_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Cart service
echo Setting up cart service...
cd cart_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Order service
echo Setting up order service...
cd order_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Paying service
echo Setting up paying service...
cd paying_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Shipping service
echo Setting up shipping service...
cd shipping_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Items service
echo Setting up items service...
cd items_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Book service
echo Setting up book service...
cd book_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Mobile service
echo Setting up mobile service...
cd mobile_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Laptop service
echo Setting up laptop service...
cd laptop_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Clothes service
echo Setting up clothes service...
cd clothes_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Gateway service
echo Setting up gateway service...
cd gateway_service
python manage.py makemigrations
python manage.py migrate
cd ..

:: Load initial data
echo Loading initial data...
python load_initial_data_local.py

:: Start services without separate windows
echo Starting services...
echo WARNING: Services will run sequentially. Press Ctrl+C to stop.
echo.

:: Start main service
echo Starting main service on port 8000...
call .venv\Scripts\activate.bat && python manage.py runserver 8000

:: The following services won't run unless the above service is stopped
:: If you want to run a specific service, comment out the others and uncomment the one you need

:: Start customer service
:: echo Starting customer service on port 8001...
:: call .venv\Scripts\activate.bat && cd customer_service && python manage.py runserver 8001

:: Start cart service
:: echo Starting cart service on port 8002...
:: call .venv\Scripts\activate.bat && cd cart_service && python manage.py runserver 8002

:: Start order service
start cmd /k "call venv\Scripts\activate.bat && cd order_service && python manage.py runserver 8003"

:: Start paying service
start cmd /k "call venv\Scripts\activate.bat && cd paying_service && python manage.py runserver 8004"

:: Start items service
start cmd /k "call venv\Scripts\activate.bat && cd items_service && python manage.py runserver 8005"

:: Start shipping service
start cmd /k "call venv\Scripts\activate.bat && cd shipping_service && python manage.py runserver 8006"

:: Start book service
start cmd /k "call venv\Scripts\activate.bat && cd book_service && python manage.py runserver 8010"

:: Start laptop service
start cmd /k "call venv\Scripts\activate.bat && cd laptop_service && python manage.py runserver 8011"

:: Start mobile service
start cmd /k "call venv\Scripts\activate.bat && cd mobile_service && python manage.py runserver 8012"

:: Start clothes service
start cmd /k "call venv\Scripts\activate.bat && cd clothes_service && python manage.py runserver 8013"

:: Start gateway service (last, since it depends on other services)
start cmd /k "call venv\Scripts\activate.bat && cd gateway_service && python manage.py runserver 8007"

echo.
echo All services started! Access the main application at http://localhost:8000
echo Gateway service is running at http://localhost:8007
echo.
echo Press any key to stop all services...
pause > nul

:: Kill all python processes (be careful with this in a real environment)
taskkill /f /im python.exe

echo All services stopped.