# Detaillierte Erklärung: Wie Safecircles berechnet werden

## Übersicht
Die Safecircle-Berechnung erfolgt in `backend/arkserver/circle.py` durch die Funktion `calc_circles(game)`. Diese Funktion analysiert die Abstimmungsdaten aus Übung 5 (ubung-5) und berechnet für verschiedene Toleranzfenster-Werte (1-100), welche Spieler in sicheren Kreisen verbunden sind.

## Datenstruktur: Was ist `get_u5(game)`?

Die Funktion `get_u5(game)` (in `backend/arkserver/management/commands/utils.py`) holt alle Abstimmungsdaten aus Übung 5:

```python
votes = {
    "Spieler1": {
        "Sicherheitsanker1~Triggerthema1": {
            "Spieler1": 75,  # Wie Spieler1 Spieler1 bei diesem Gegensatzpaar bewertet
            "Spieler2": 60,  # Wie Spieler2 Spieler1 bei diesem Gegensatzpaar bewertet
            "Spieler3": 80,  # ...
        },
        "Sicherheitsanker2~Triggerthema2": {
            "Spieler1": 50,
            "Spieler2": 70,
            ...
        },
        ...
    },
    "Spieler2": { ... },
    ...
}
```

**Struktur:**
- **Äußere Ebene**: `votes[player_name]` = Alle Abstimmungen, die sich auf diesen Spieler beziehen
- **Mittlere Ebene**: `votes[player_name][power_pair]` = Ein spezifisches Gegensatzpaar (Sicherheitsanker~Triggerthema)
- **Innere Ebene**: `votes[player_name][power_pair][voter_name]` = Die Bewertung (0-100), die ein bestimmter Spieler für dieses Gegensatzpaar abgegeben hat

## Schritt-für-Schritt Berechnung

### Schritt 1: Berechnung der Safe-Zone Baseline (`safezone`)

Für jedes Gegensatzpaar (z.B. "Vertrauen~Misstrauen") wird ein Team-Durchschnitt berechnet:

```python
safezone[power] = Summe aller Bewertungen für dieses Gegensatzpaar / (n * n)
```

**Beispiel für TestLucerne25:**
- Angenommen, es gibt 10 Spieler (n=10)
- Für das Gegensatzpaar "Vertrauen~Misstrauen" wurden insgesamt 100 Bewertungen abgegeben
- `safezone["Vertrauen~Misstrauen"] = 100 / (10 * 10) = 1.0`

Dieser Wert stellt die **Team-Baseline** dar - den erwarteten Durchschnittswert für dieses Gegensatzpaar.

### Schritt 2: Berechnung der normalisierten Distanz zwischen Spielern

Für jedes Spielerpaar (P1, P2) wird eine **normalisierte Distanz** berechnet:

```python
result[P1][P2] = Summe über alle Gegensatzpaare von:
    abs(score - baseline) / safebar / n
```

**Formel im Detail:**
- Für jedes Gegensatzpaar `p`:
  - `score` = Die Bewertung, die P1 für P2 bei diesem Gegensatzpaar abgegeben hat
  - `baseline` = Der Safe-Zone Durchschnitt für dieses Gegensatzpaar
  - `delta = abs(score - baseline) / safebar`
  - `s += delta / n`
- `result[P1][P2] = s` (kumulierte normalisierte Distanz)

**Beispiel:**
- P1 bewertet P2 bei 3 Gegensatzpaaren: [70, 60, 80]
- Baselines für diese Paare: [65, 55, 75]
- `safebar = 16` (Toleranzfenster)
- `n = 10`

```
delta1 = |70-65| / 16 = 5/16 = 0.3125
delta2 = |60-55| / 16 = 5/16 = 0.3125
delta3 = |80-75| / 16 = 5/16 = 0.3125
s = (0.3125 + 0.3125 + 0.3125) / 10 = 0.09375
result[P1][P2] = 0.09375
```

**Interpretation:** 
- `result[P1][P2] <= 1` bedeutet: P1's Wahrnehmung von P2 liegt innerhalb des Toleranzfensters
- `result[P1][P2] > 1` bedeutet: P1's Wahrnehmung von P2 liegt außerhalb des Toleranzfensters

### Schritt 3: Identifikation von "Edges" (sichere Verbindungen)

Ein **Edge** (Verbindung) zwischen zwei Spielern existiert, wenn:
- `result[P1][P2] <= 1` UND
- `result[P2][P1] <= 1`

Das bedeutet: **Beide Spieler nehmen sich gegenseitig als sicher wahr** (bidirektionale Sicherheit).

### Schritt 4: Berechnung der Safecircles

Die Safecircles werden durch **kombinatorische Suche** gefunden:

```python
for size in range(n, 1, -1):  # Von größten zu kleinsten Gruppen
    for combination in combinations(range(n), size):
        # Prüfe, ob alle Spielerpaare in dieser Kombination sicher verbunden sind
        if all(result[players[x]][players[y]] <= 1 for x, y in pairs):
            # Dies ist ein Safecircle!
```

**Algorithmus:**
1. Beginne mit der größten möglichen Gruppe (alle n Spieler)
2. Prüfe alle Kombinationen dieser Größe
3. Ein Safecircle existiert, wenn **alle Spielerpaare** innerhalb des Kreises eine Distanz <= 1 haben
4. Wenn ein Safecircle gefunden wird, werden kleinere Subsets ignoriert (um Redundanz zu vermeiden)
5. Wiederhole für kleinere Gruppen (n-1, n-2, ..., 2)

**Beispiel für einen Safecircle:**
- Spieler [0, 1, 2, 3] bilden einen Safecircle, wenn:
  - `result[0][1] <= 1` und `result[1][0] <= 1` ✓
  - `result[0][2] <= 1` und `result[2][0] <= 1` ✓
  - `result[0][3] <= 1` und `result[3][0] <= 1` ✓
  - `result[1][2] <= 1` und `result[2][1] <= 1` ✓
  - `result[1][3] <= 1` und `result[3][1] <= 1` ✓
  - `result[2][3] <= 1` und `result[3][2] <= 1` ✓

### Schritt 5: Berechnung der Dyads (Zweier-Verbindungen)

**Dyads** sind Paare von Spielern, die:
- Eine sichere Verbindung haben (Edge existiert)
- **NICHT** bereits Teil eines größeren Safecircles sind

### Schritt 6: Iteration über Toleranzfenster-Werte

Die gesamte Berechnung wird für **jeden Toleranzfenster-Wert von 1 bis 100** durchgeführt:

```python
for bar in range(1, 100):
    data = calc_single(players, votes, n, safezone, bar)
    result[bar] = data
```

**Stoppbedingung:**
- Wenn alle Spieler in einem einzigen Safecircle sind (`len(circle_count) == n` und `len(circles) == 1`)
- UND jeder Spieler ist nur in diesem einen Kreis (`mono_circle = True`)
- Dann wird die Iteration gestoppt (weiter größere Werte ergeben keine neuen Informationen)

## Beispiel: TestLucerne25

### Annahmen:
- **10 Spieler**: Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Henry, Iris, Jack
- **3 Gegensatzpaare**: 
  - "Vertrauen~Misstrauen"
  - "Offenheit~Zurückhaltung"
  - "Mut~Angst"

### Schritt 1: Safe-Zone Baseline
```
safezone["Vertrauen~Misstrauen"] = 65.0
safezone["Offenheit~Zurückhaltung"] = 55.0
safezone["Mut~Angst"] = 70.0
```

### Schritt 2: Normalisierte Distanzen (für safebar=16)

**Beispiel: Alice → Bob**
- Alice bewertet Bob bei "Vertrauen~Misstrauen": 70
- Alice bewertet Bob bei "Offenheit~Zurückhaltung": 60
- Alice bewertet Bob bei "Mut~Angst": 75

```
delta1 = |70-65| / 16 = 0.3125
delta2 = |60-55| / 16 = 0.3125
delta3 = |75-70| / 16 = 0.3125
result[Alice][Bob] = (0.3125 + 0.3125 + 0.3125) / 10 = 0.09375 ✓ (<= 1)
```

**Beispiel: Alice → Charlie** (wenn Alice Charlie sehr kritisch sieht)
- Alice bewertet Charlie bei "Vertrauen~Misstrauen": 30
- Alice bewertet Charlie bei "Offenheit~Zurückhaltung": 25
- Alice bewertet Charlie bei "Mut~Angst": 20

```
delta1 = |30-65| / 16 = 2.1875
delta2 = |25-55| / 16 = 1.875
delta3 = |20-70| / 16 = 3.125
result[Alice][Charlie] = (2.1875 + 1.875 + 3.125) / 10 = 0.71875 ✓ (<= 1, aber nah an der Grenze)
```

### Schritt 3: Edges identifizieren

**Edge Alice ↔ Bob existiert, wenn:**
- `result[Alice][Bob] <= 1` ✓
- `result[Bob][Alice] <= 1` ✓

### Schritt 4: Safecircles finden

**Für safebar=16:**
- Safecircle 1: [Alice, Bob, Diana, Eve] - alle haben bidirektionale Distanzen <= 1
- Safecircle 2: [Frank, Grace, Henry] - alle haben bidirektionale Distanzen <= 1
- Safecircle 3: [Iris, Jack] - Dyad

**Für safebar=20 (größeres Toleranzfenster):**
- Safecircle 1: [Alice, Bob, Charlie, Diana, Eve] - jetzt ist auch Charlie dabei!
- Safecircle 2: [Frank, Grace, Henry, Iris] - jetzt ist Iris dabei!
- Safecircle 3: [Jack] - Solo (kein Safecircle)

**Für safebar=35 (sehr großes Toleranzfenster):**
- Safecircle 1: [Alice, Bob, Charlie, Diana, Eve, Frank, Grace, Henry, Iris, Jack] - alle in einem Kreis!

## Wichtige Konzepte

### 1. Toleranzfenster (`safebar`)
- **Kleiner Wert (z.B. 10)**: Sehr enge Toleranz → Wenige, kleine Safecircles
- **Mittlerer Wert (z.B. 16)**: Standard → Mehrere, mittlere Safecircles
- **Großer Wert (z.B. 35)**: Sehr weite Toleranz → Ein großer Safecircle mit allen

### 2. Bidirektionale Sicherheit
Ein Safecircle erfordert, dass **alle Paare** bidirektional sicher sind:
- Nicht nur: "Alice findet Bob sicher"
- Sondern auch: "Bob findet Alice sicher"

### 3. Maximale Safecircles
Der Algorithmus findet **maximale** Safecircles:
- Wenn [A, B, C, D] ein Safecircle ist, dann ist [A, B] kein separater Safecircle
- Es werden nur die größten möglichen Gruppen gefunden

### 4. Circle Count
Für jeden Spieler wird gezählt, in wie vielen Safecircles er ist:
- `circle_count[Alice] = 2` bedeutet: Alice ist in 2 Safecircles
- Spieler mit hohem `circle_count` sind **Integratoren** (verbinden verschiedene Gruppen)

## Visualisierung in team-potential.html

Die berechneten Safecircles werden dann in `team-potential.html` visualisiert:
- **Canvas**: Zeigt die Safecircles als farbige Kreise
- **Safe Circles Overview**: Listet alle Safecircles für den aktuellen Toleranzfenster-Wert
- **Integratoren**: Spieler mit hohem `circle_count` werden als grüne Punkte markiert

## Zusammenfassung

Die Safecircle-Berechnung ist ein **iterativer Prozess**, der:
1. Abstimmungsdaten aus Übung 5 analysiert
2. Für jeden Toleranzfenster-Wert (1-100) berechnet:
   - Normalisierte Distanzen zwischen allen Spielerpaaren
   - Sichere Verbindungen (Edges)
   - Maximale Safecircles (Gruppen mit bidirektionaler Sicherheit)
   - Dyads (isolierte sichere Paare)
3. Die Ergebnisse für die Visualisierung aufbereitet

Der **Team-Sweetspot** ist jener Toleranzfenster-Wert, bei dem die **maximale Anzahl** von Safecircles entsteht - also die optimale Balance zwischen Sicherheit und Vielfalt.

## Praktische Analyse: TestLucerne25

Um die Safecircle-Berechnung für ein konkretes Spiel wie TestLucerne25 zu analysieren, kann das Django Management Command verwendet werden:

```bash
cd backend
python manage.py circle TestLucerne25
```

Oder mit einem spezifischen Toleranzfenster-Wert:

```bash
python manage.py circle TestLucerne25 -bar 16
```

**Ausgabe des Commands:**

1. **Matrix**: Zeigt die normalisierten Distanzen zwischen allen Spielerpaaren
   ```
   Matrix:
            Alice  Bob    Charlie Diana  Eve
   Alice    0.00   0.09   0.72   0.15   0.12
   Bob      0.08   0.00   0.65   0.11   0.10
   ...
   ```

2. **Edges**: Listet alle sicheren bidirektionalen Verbindungen
   ```
   Edges:
   Alice Bob 0.09
   Alice Diana 0.15
   Bob Diana 0.11
   ...
   ```

3. **Circles**: Zeigt alle gefundenen Safecircles mit ihrem Durchschnittswert
   ```
   Circles:
   Alice Bob Diana Eve 0.11
   Frank Grace Henry 0.08
   ...
   ```

4. **Circle count**: Zeigt für jeden Spieler, in wie vielen Safecircles er ist
   ```
   Circle count:
   Alice: 2
   Bob: 2
   Diana: 2
   ...
   ```

**Interpretation der Ausgabe:**

- **Matrix-Werte <= 1.0**: Sichere Verbindung in dieser Richtung
- **Matrix-Werte > 1.0**: Unsichere Verbindung (außerhalb des Toleranzfensters)
- **Edges**: Spielerpaare, die bidirektional sicher sind (beide Richtungen <= 1.0)
- **Circles**: Maximale Gruppen, in denen alle Spielerpaare sicher verbunden sind
- **Circle count**: Höhere Werte = Integratoren (Spieler, die mehrere Gruppen verbinden)

**Beispiel-Interpretation für TestLucerne25:**

Wenn die Ausgabe zeigt:
- Safecircle 1: [Alice, Bob, Diana, Eve] mit Wert 0.11
- Safecircle 2: [Frank, Grace, Henry] mit Wert 0.08
- Circle count: Alice=2, Bob=2, Diana=2, Eve=1, Frank=1, Grace=1, Henry=1

Dann bedeutet das:
- Alice, Bob, Diana und Eve bilden einen Safecircle (alle nehmen sich gegenseitig als sicher wahr)
- Frank, Grace und Henry bilden einen separaten Safecircle
- Alice, Bob und Diana sind Integratoren (in 2 Safecircles), was bedeutet, dass sie wahrscheinlich auch Verbindungen zu anderen Gruppen haben

## Code-Referenz

Die Hauptfunktionen befinden sich in:
- **`backend/arkserver/circle.py`**: `calc_circles()` und `calc_single()` - Hauptberechnungslogik
- **`backend/arkserver/management/commands/utils.py`**: `get_u5()` - Datenabruf aus der Datenbank
- **`backend/arkserver/views.py`**: `team_potential()` - View, die die Berechnung aufruft und an das Template übergibt

