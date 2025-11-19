# Dynamic Progress Bar Implementation

## Overview
The hardcoded progress bars (showing fixed percentages like 65%, 20%, etc.) have been replaced with a dynamic system that calculates progress based on the current page in the game flow.

## Files Created
- `/frontend/public/js/game-progress.js` - Main JavaScript file that calculates and updates progress

## How It Works
1. The script defines the game flow sequence (preview → ubung-1 → ubung-2 → ... → assessment → arche)
2. It detects the current page from the URL
3. It calculates the progress percentage based on the page's position in the flow
4. It automatically updates the progress bar on page load

## Implementation Steps

### Step 1: Update Progress Bar HTML
Replace the hardcoded progress bar with a dynamic one:

**Before:**
```html
<div class="progress__bar">
    <div style="width: 65%; border-radius: 10px;">65%</div>
</div>
```

**After:**
```html
<div class="progress__bar">
    <div id="game-progress-bar" style="width: 0%; border-radius: 10px;">0%</div>
</div>
```

Or if you want to keep the existing structure, just ensure the inner div can be found by the script (it will look for `.progress__bar > div`).

### Step 2: Include the Script
Add the script tag before the closing `</body>` tag or in the `<head>` section:

```html
<script src="/static/js/game-progress.js"></script>
```

## Files That Need Updating

All HTML files in `/frontend/views/` that have a progress bar need to:
1. Replace hardcoded width/percentage in the progress bar div
2. Add the script tag: `<script src="/static/js/game-progress.js"></script>`

### Files with Progress Bars:
- ubung-1.html
- ubung-2.html
- ubung-3.html
- ubung-4.html ✅ (already updated)
- ubung-5.html
- wartezimmer.html
- assessment.html
- spannungsfelder.html
- team-potential.html
- waiting_room3.html
- mission-2-ubung-1.html
- mission-2-ubung-2.html
- preview.html
- preview-2.html
- ubung-1-pro.html
- ubung-3-pro.html
- psychologischer.html
- heatmap-pro.html
- arche.html

## Customization

### Adjusting Game Flow
Edit `/frontend/public/js/game-progress.js` and modify the `GAME_FLOW` array to match your actual game sequence:

```javascript
const GAME_FLOW = [
    'preview',
    'ubung-1',
    'ubung-2',
    // ... add/remove pages as needed
];
```

### Custom Progress Calculation
If you need more sophisticated progress calculation (e.g., based on completed steps within a page), modify the `calculateProgress()` function in `game-progress.js`.

## Testing
1. Navigate to different pages in the game flow
2. Check that the progress bar updates correctly
3. Verify the percentage matches the page's position in the flow

## Notes
- The script automatically initializes on page load
- Progress is calculated as: (current step / total steps) * 100 + 50% of step size
- The script is backward compatible - if a page isn't in the flow, it shows 0%
- You can access the progress calculator via `window.GameProgress` if needed

