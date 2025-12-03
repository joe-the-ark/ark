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

# Store the Python path for later use
PYTHON_BIN="$(which python)"
PYTHON_PATH="$PYTHON_BIN"

echo "Using Python: $PYTHON_BIN"
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"

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

# 4.5. Install meta library (required for the application)
echo "Installing meta library..."
# Always reinstall meta library to ensure it's available in venv
if [ -d "meta/backend/src" ]; then
    echo "Found meta/backend/src, installing meta library in virtual environment..."
    cd meta/backend/src
    
    # First, try to uninstall any existing meta installation
    pip uninstall -y meta 2>/dev/null || true
    
    # Install dependencies first (Crypto, pycrypto)
    echo "Installing meta library dependencies..."
    "$PYTHON_BIN" -m pip install pycrypto --quiet 2>/dev/null || true
    
    # Install using pip with editable mode to ensure it's in venv
    echo "Installing meta library with pip (editable mode)..."
    "$PYTHON_BIN" -m pip install -e . --quiet
    INSTALL_META_EXIT=$?
    
    if [ $INSTALL_META_EXIT -ne 0 ]; then
        echo "Pip editable install failed, trying regular install..."
        "$PYTHON_BIN" -m pip install . --quiet
        INSTALL_META_EXIT=$?
    fi
    
    if [ $INSTALL_META_EXIT -ne 0 ]; then
        echo "Pip install failed, trying setup.py install..."
        "$PYTHON_BIN" setup.py install
        INSTALL_META_EXIT=$?
    fi
    
    cd ../../..
    
    if [ $INSTALL_META_EXIT -ne 0 ]; then
        echo "✗ ERROR: Failed to install meta library!"
        echo "Please install it manually:"
        echo "  source $VENV_PATH/bin/activate"
        echo "  cd meta/backend/src"
        echo "  pip install -e ."
        exit 1
    fi
    
    echo "✓ Meta library installation completed"
    
    # CRITICAL: Verify installation - must be importable with the venv Python
    echo "Verifying meta library installation with venv Python..."
    VERIFY_OUTPUT=$("$PYTHON_BIN" -c "import meta; print('SUCCESS')" 2>&1)
    if [ $? -ne 0 ] || [ "$VERIFY_OUTPUT" != "SUCCESS" ]; then
        echo "✗ ERROR: Meta library installed but NOT importable with venv Python!"
        echo "Verification output: $VERIFY_OUTPUT"
        echo "Python binary: $PYTHON_BIN"
        echo "Virtual env: $VIRTUAL_ENV"
        echo ""
        echo "Checking Python paths:"
        "$PYTHON_BIN" -c "import sys; [print(p) for p in sys.path]"
        echo ""
        echo "Checking if meta is installed:"
        "$PYTHON_BIN" -m pip list | grep meta || echo "meta not found in pip list"
        echo ""
        echo "Trying to find meta installation:"
        find "$VIRTUAL_ENV" -name "meta" -type d 2>/dev/null | head -5
        exit 1
    fi
    echo "✓ Meta library verified and ready"
else
    echo "✗ ERROR: meta/backend/src directory not found!"
    echo "Current directory: $(pwd)"
    echo "Please ensure the meta library source code is available."
    exit 1
fi

# 5. Compile translations
echo "Compiling translations..."
cd backend
# Use the Python from virtual environment
"$PYTHON_BIN" manage.py compilemessages --settings=backend.settings_prod
COMPILE_EXIT=$?
cd ..
if [ $COMPILE_EXIT -ne 0 ]; then
    echo "⚠ WARNING: Translation compilation failed, continuing anyway..."
fi

# 6. Run Django migrations
echo "Running database migrations..."
cd backend
# Use the Python from virtual environment
"$PYTHON_BIN" manage.py migrate --settings=backend.settings_prod
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
# Use the Python from virtual environment
"$PYTHON_BIN" manage.py collectstatic --no-input --settings=backend.settings_prod
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