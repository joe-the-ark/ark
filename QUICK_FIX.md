# Quick Fix für Server-Probleme

## Problem: Django wird nicht gefunden

Wenn Sie diesen Fehler sehen:
```
ModuleNotFoundError: No module named 'django'
```

## Lösung 1: Virtuelle Umgebung manuell erstellen

```bash
cd /root/ark2020/ark

# Virtuelle Umgebung erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate

# Requirements installieren
pip install --upgrade pip
pip install -r requirements.txt

# Testen
python -c "import django; print(django.get_version())"
# Sollte "2.2.27" ausgeben
```

## Lösung 2: Build-Script ausführen

Das neue `build.sh` erstellt die virtuelle Umgebung automatisch, wenn sie nicht existiert:

```bash
cd /root/ark2020/ark
chmod +x build.sh
./build.sh
```

## Lösung 3: Supervisor-Konfiguration aktualisieren

Stellen Sie sicher, dass Supervisor die virtuelle Umgebung verwendet:

```bash
# Supervisor-Konfiguration kopieren
sudo cp /root/ark2020/ark/ark2020.conf /etc/supervisor/conf.d/ark2020.conf

# Supervisor neu laden
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart ark2020

# Status prüfen
sudo supervisorctl status ark2020
```

## Lösung 4: Wenn nichts funktioniert

```bash
cd /root/ark2020/ark

# 1. Virtuelle Umgebung sicherstellen
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Django manuell installieren
pip install Django==2.2.27 whitenoise==6.5.0

# 3. Testen
cd backend
python manage.py --version
# Sollte Django-Version zeigen

# 4. Build-Script ausführen
cd ..
./build.sh
```

## Debugging

### Prüfen Sie die virtuelle Umgebung:
```bash
cd /root/ark2020/ark
ls -la | grep venv
```

### Prüfen Sie, welche Python-Version verwendet wird:
```bash
source venv/bin/activate
which python
python --version
```

### Prüfen Sie, ob Django installiert ist:
```bash
source venv/bin/activate
pip list | grep Django
```

### Prüfen Sie Supervisor-Logs:
```bash
sudo tail -f /var/log/supervisor/supervisord.log
sudo tail -f /var/log/ark2020/error.log
```

