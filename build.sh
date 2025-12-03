#!/bin/bash
# Don't use set -e here, we want to handle errors gracefully
set +e

echo "Starting build process..."

# 1. Git pull
echo "Pulling latest changes from repository..."
git pull

# 2. Activate virtual environment (check common locations)
VENV_ACTIVATED=false
VENV_PATH=""

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    VENV_PATH="venv"
    VENV_ACTIVATED=true
    echo "✓ Virtual environment activated: venv/"
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    VENV_PATH=".venv"
    VENV_ACTIVATED=true
    echo "✓ Virtual environment activated: .venv/"
elif [ -f "env/bin/activate" ]; then
    source env/bin/activate
    VENV_PATH="env"
    VENV_ACTIVATED=true
    echo "✓ Virtual environment activated: env/"
else
    echo "⚠ WARNING: No virtual environment found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        source venv/bin/activate
        VENV_PATH="venv"
        VENV_ACTIVATED=true
        echo "✓ Virtual environment created and activated: venv/"
    else
        echo "✗ ERROR: Failed to create virtual environment."
        echo "Please create it manually: python3 -m venv venv"
        exit 1
    fi
fi

# Verify virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "✗ ERROR: Virtual environment is not active!"
    exit 1
fi

echo "Using Python: $(which python)"
echo "Python version: $(python --version)"

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: pip upgrade failed, continuing anyway..."
fi

# 4. Install/update requirements
echo "Installing/updating requirements..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "✗ ERROR: Failed to install requirements!"
    echo "Please check requirements.txt and install manually:"
    echo "  source $VENV_PATH/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Verify Django is installed
python -c "import django; print('Django version:', django.get_version())" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "✗ ERROR: Django is not installed!"
    echo "Installing Django..."
    pip install Django==2.2.27
    if [ $? -ne 0 ]; then
        echo "✗ ERROR: Failed to install Django!"
        exit 1
    fi
fi

# 5. Compile translations
echo "Compiling translations..."
cd backend
python manage.py compilemessages --settings=backend.settings_prod
COMPILE_EXIT=$?
cd ..
if [ $COMPILE_EXIT -ne 0 ]; then
    echo "⚠ WARNING: Translation compilation failed, continuing anyway..."
fi

# 6. Run Django migrations
echo "Running database migrations..."
cd backend
python manage.py migrate --settings=backend.settings_prod
MIGRATE_EXIT=$?
if [ $MIGRATE_EXIT -ne 0 ]; then
    echo "✗ ERROR: Migration failed!"
    cd ..
    exit 1
fi
cd ..

# 7. Collect static files
echo "Collecting static files..."
cd backend
python manage.py collectstatic --no-input --settings=backend.settings_prod
COLLECT_EXIT=$?
cd ..
if [ $COLLECT_EXIT -ne 0 ]; then
    echo "✗ ERROR: Static file collection failed!"
    exit 1
fi

# 8. Restart services
echo "Restarting services..."
supervisorctl restart ark2020
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: supervisorctl restart failed, continuing..."
fi

service nginx restart
if [ $? -ne 0 ]; then
    echo "⚠ WARNING: nginx restart failed, continuing..."
fi

echo ""
echo "✓ Build completed successfully!"
echo "Virtual environment: $VENV_PATH"
echo "Python: $(which python)"