# Virtual Environment Setup Guide

## Problem
Wenn Django nicht gefunden wird, liegt das meist daran, dass keine virtuelle Umgebung aktiviert ist oder die Requirements nicht installiert sind.

## Lösung: Virtuelle Umgebung einrichten

### Schritt 1: Virtuelle Umgebung erstellen

```bash
cd /root/ark2020/ark
python3 -m venv venv
```

### Schritt 2: Virtuelle Umgebung aktivieren

```bash
source venv/bin/activate
```

### Schritt 3: Requirements installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Schritt 4: Meta-Library installieren (falls benötigt)

```bash
cd meta/backend/src
python setup.py install
cd ../../..
```

### Schritt 5: Testen

```bash
# Django-Version prüfen
python -c "import django; print(django.get_version())"

# Sollte Django 2.2.27 ausgeben
```

### Schritt 6: Supervisor-Konfiguration aktualisieren

Die `ark2020.conf` Datei sollte den vollständigen Pfad zur virtuellen Umgebung verwenden:

```ini
[program:ark2020]
command = /root/ark2020/ark/venv/bin/gunicorn backend.wsgi_prod -b 127.0.0.1:8888 -w 12
directory = /root/ark2020/ark/backend/
environment=PATH="/root/ark2020/ark/venv/bin:%(ENV_PATH)s"
```

### Schritt 7: Supervisor neu laden

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart ark2020
```

## Alternative: Wenn venv an anderem Ort

Falls die virtuelle Umgebung an einem anderen Ort liegt, passen Sie die Pfade in `build.sh` und `ark2020.conf` entsprechend an:

- `.venv/` statt `venv/`
- `env/` statt `venv/`
- Oder vollständiger Pfad wie `/root/ark2020/ark/.venv/`

## Troubleshooting

### Django wird immer noch nicht gefunden

1. Prüfen Sie, ob die virtuelle Umgebung existiert:
   ```bash
   ls -la /root/ark2020/ark/ | grep venv
   ```

2. Prüfen Sie, ob Django installiert ist:
   ```bash
   source venv/bin/activate
   pip list | grep Django
   ```

3. Falls nicht, installieren Sie es manuell:
   ```bash
   source venv/bin/activate
   pip install Django==2.2.27
   pip install -r requirements.txt
   ```

### Supervisor verwendet falsche Python-Version

Stellen Sie sicher, dass Supervisor die virtuelle Umgebung verwendet:

```bash
# Supervisor-Konfiguration prüfen
sudo cat /etc/supervisor/conf.d/ark2020.conf

# Falls nötig, aktualisieren:
sudo nano /etc/supervisor/conf.d/ark2020.conf
# Dann:
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart ark2020
```

### Logs prüfen

```bash
# Supervisor-Logs
sudo tail -f /var/log/supervisor/supervisord.log

# Application-Logs (falls konfiguriert)
sudo tail -f /var/log/ark2020/error.log
```

