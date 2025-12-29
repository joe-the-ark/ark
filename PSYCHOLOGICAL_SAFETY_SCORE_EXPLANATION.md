# Psychological Safety Score Calculation - Explanation

## Overview
The psychological safety score is calculated based on votes from Ubung-4 (Safety Score exercise), where team members assign each other to different statement boxes.

## Statement Boxes and Their Weights

The six statement boxes have different weights based on their contribution to psychological safety:

| Row | Statement | Color | Weight | Meaning |
|-----|-----------|-------|--------|---------|
| **row0** | "Schwierige Themen können wir meist gut zusammen anschauen." | Green (#9FE2BF) | **4** | Positive - indicates good collaboration |
| **row1** | "Ich beobachte wie du gelegentlich Menschen im Team ausschliesst." | Red (#fa5252) | **1** | Negative - indicates exclusion behavior |
| **row2** | "Für mich bist du im Team nicht immer sichtbar." | Orange (#E29635) | **3** | Neutral/Challenging - visibility issues |
| **row3** | "Ich fühle wie meine Talente von dir gesehen und einbezogen werden." | Green (#9FE2BF) | **5** | Very Positive - highest weight, indicates talent recognition |
| **row4** | "Ich habe das Gefühl du reagierst auf Fehler mit Schuldzuweisungen an Einzelne im Team." | Red (#fa5252) | **0** | Very Negative - blame culture (no positive contribution) |
| **row5** | "Mir fällt es mitunter schwer dich um Hilfe zu bitten." | Orange (#E29635) | **2** | Neutral/Challenging - difficulty asking for help |

## Score Calculation Formula

```
score = (row_0 × 4 + row_1 × 1 + row_2 × 3 + row_3 × 5 + row_4 × 0 + row_5 × 2) × 20
final_score = score / (number_of_active_players)²
```

### Step-by-Step:

1. **Count all votes** in each row across all team members' Ubung4 submissions
2. **Apply weights** to each row count
3. **Sum weighted values** and multiply by 20
4. **Normalize** by dividing by the square of the number of active players
5. **Round** to nearest integer

### Example Calculation:

For a team with 4 active players:
- row0: 8 votes → 8 × 4 = 32
- row1: 2 votes → 2 × 1 = 2
- row2: 4 votes → 4 × 3 = 12
- row3: 10 votes → 10 × 5 = 50
- row4: 1 vote → 1 × 0 = 0
- row5: 3 votes → 3 × 2 = 6

Weighted sum: 32 + 2 + 12 + 50 + 0 + 6 = 102
Multiplied by 20: 102 × 20 = 2040
Normalized: 2040 / (4²) = 2040 / 16 = 127.5
Final score: **128** (rounded)

## Score Range

- **Scale**: 0 to 99 (as displayed in the UI)
- **Interpretation** (from tooltip):
  - **> 85**: Safe (aussergewöhnlich sicher)
  - **75-85**: Rather safe (eher sicher)
  - **65-75**: Gray area - caution needed (Graubereich - Vorsicht geboten)
  - **< 65**: Rather unsafe - external support should be considered (eher unsicher)
  - **< 60**: Very unsafe (sehr unsicher)

## ⚠️ BUG IDENTIFIED

**Issue**: In `psychologischer` view (line 1618), the score is calculated using only the **current user's** appearances in each box, not all team votes.

**Current (BUGGY) code**:
```python
row_0 = len(row0_current_user)  # Only counts current user!
# ... same for other rows
score = (row_0 * 4 + row_1 * 1 + ...) * 20 / num
```

**Correct approach** (as used in `assessment` view):
```python
# Count ALL votes across all players
for game_ in game_place:
    row_0 += game_.row0.all().count()  # Counts all players
    # ... same for other rows
```

**Impact**: Each user sees a different score, which is incorrect for a team metric. The score should be the same for all team members.

## Fix Required

The `psychologischer` view should count ALL votes (like `assessment` view does), not just the current user's votes.

