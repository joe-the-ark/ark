#!/bin/bash
set -e  # Exit on error

echo "Starting build process..."

# 1. Git pull
echo "Pulling latest changes from repository..."
git pull

# 2. Activate virtual environment (check common locations)
VENV_ACTIVATED=false
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated: venv/"
    VENV_ACTIVATED=true
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated: .venv/"
    VENV_ACTIVATED=true
elif [ -f "env/bin/activate" ]; then
    source env/bin/activate
    echo "Virtual environment activated: env/"
    VENV_ACTIVATED=true
else
    echo "WARNING: No virtual environment found. Using system Python."
    echo "This may cause issues if Django is not installed system-wide."
fi

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# 4. Install/update requirements
echo "Installing/updating requirements..."
pip install -r requirements.txt --quiet

# 5. Compile translations
echo "Compiling translations..."
# Use python manage.py instead of django-admin to ensure we use the correct Python
cd backend
python manage.py compilemessages --settings=backend.settings_prod
cd ..

# 6. Run Django migrations
echo "Running database migrations..."
cd backend
python manage.py migrate --settings=backend.settings_prod

# 7. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --settings=backend.settings_prod

# 8. Return to root directory
cd ..

# 9. Restart services
echo "Restarting services..."
supervisorctl restart ark2020
service nginx restart

echo "Build completed successfully!"