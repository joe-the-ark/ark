# Team Average Gradient - Where to Change Colors

## Files to Update

The `team-average__wrapper` gradient appears in these CSS files:

### 1. `/frontend/public/css/boxings.css`
**Line 26-34** (used by `psychologischer.html`)
```css
.team-average__wrapper:before {
  content: ' ';
  position: absolute;
  top: 0;
  left: 0;
  height: 8px;
  width: 100%;
  background: linear-gradient(89.69deg, #3dff39 30%, #e1f131 50%, #f53131 80%);
}
```

### 2. `/frontend/public/css/assessment.css`
**Line 320-328**
```css
.team-average__wrapper:before {
  content: ' ';
  position: absolute;
  top: 0;
  left: 0;
  height: 8px;
  width: 100%;
  background: linear-gradient(89.69deg, #3dff39 30%, #e1f131 50%, #f53131 80%);
}
```

### 3. `/frontend/public/css/psychologischer2.css`
**Line 26-34**
```css
.team-average__wrapper:before {
  content: ' ';
  position: absolute;
  top: 0;
  left: 0;
  height: 8px;
  width: 100%;
  background: linear-gradient(89.69deg, #3dff39 50%, #e1f131 50%, #f53131 80%);
}
```

## Current Colors
- `#3dff39` = Green (currently used for high values)
- `#e1f131` = Yellow (currently used for middle values)
- `#f53131` = Red (currently used for low values)

## Project Colors to Use
- `#fa5252` = Red (for low values)
- `#E29635` = Orange (for middle values)
- `#9FE2BF` = Green (for high values)

## How to Change

Replace the `background` property in each file with:

```css
background: linear-gradient(89.69deg, #fa5252 0%, #fa5252 33%, #E29635 33%, #E29635 66%, #9FE2BF 66%, #9FE2BF 100%);
```

This creates:
- **Red (#fa5252)** from 0% to 33% (low values)
- **Orange (#E29635)** from 33% to 66% (middle values)
- **Green (#9FE2BF)** from 66% to 100% (high values)

## Score Range Mapping
- **1-33**: Red (unsafe)
- **34-66**: Orange (caution)
- **67-99**: Green (safe)

