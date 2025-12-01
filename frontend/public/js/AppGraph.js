class AppGraph {
  constructor({
    container,
    data,
    safezoneData = [],
    graphNumber = 0,
    range,
    statistic,
    mobile,
    labelRange,
    auto = true,
    dependency = false,
    guess = [],
  }) {
    this.container = document.querySelector(container);
    this.data = data;
    this.safezoneData = safezoneData;
    this.graphNumber = graphNumber;
    this.range = range;
    this.labelRange = labelRange;
    this.statistic = statistic;
    this.mobile = mobile;
    this.auto = auto;
    this.guess = guess;
    this.dependency = dependency;
    this.effect = function () {};

    this.auto && this.buildGraph();
    this.safeLow = 0;
    this.safeHigh = 0;
  }

  safeArea() {
    let sum = () => {
      let itog = 0;
      for (let item of this.safezoneData) {
        itog += item;
      }
      return itog;
    };
    let median = Math.round(sum() / this.safezoneData.length);
    var low = median - 16;
    var high = median + 16;
    if (low < 0) {
      low = 0;
    }
    if (high > 100) {
      high = 100;
    }
    let slide = '.slide-' + this.graphNumber.toString();
    let spanung = document.querySelector(slide);
    this.container.children[0].setAttribute('low', low);
    this.container.children[0].setAttribute('high', high);
    this.safeLow = low;
    this.safeHigh = high;
    var blue_range = high - low;
    
    let qall = this.container.parentNode.querySelectorAll(
      '.custom-graph__safezone'
    );
    
    if (!qall || !qall[this.graphNumber]) {
      return; // Safezone element not found
    }

    // Check if this is a statistic graph - check multiple ways
    const isStatistic = this.statistic || 
                        (this.container && this.container.closest('.statistic')) || 
                        (this.container && this.container.querySelector('.statistic')) ||
                        (this.container && this.container.classList.contains('statistic')) ||
                        (this.container && this.container.parentElement && this.container.parentElement.classList.contains('statistic')) ||
                        (this.container && this.container.querySelector('.custom-graph.statistic'));
    
    if (window.innerWidth <= this.mobile) {
      if (isStatistic) {
        // For statistic in mobile: use full width of items container
        const itemsContainer = this.container.querySelector('.custom-graph__items');
        if (itemsContainer) {
          const containerWidth = itemsContainer.clientWidth;
          const containerHeight = itemsContainer.clientHeight;
          let mobRight = Math.round(containerWidth * ((100 - high) / 100));
          let mobWidth = Math.round(containerWidth * (blue_range / 100));
          
          // Ensure we use the full available width
          qall[this.graphNumber].style['right'] = mobRight.toString() + 'px';
          qall[this.graphNumber].style['width'] = mobWidth.toString() + 'px';
          qall[this.graphNumber].style['top'] = '0';
          qall[this.graphNumber].style['height'] = containerHeight + 'px';
          qall[this.graphNumber].style['left'] = 'auto';
          qall[this.graphNumber].style['position'] = 'absolute';
        }
      } else {
        // For non-statistic: use item width
        let halfAvatar =
          document.querySelector('div.custom-graph__item-avatar').clientHeight / 2;
        let height = document.querySelector('.custom-graph__item').clientHeight;
        let width = document.querySelector('.custom-graph__item').clientWidth;
        let mobRight = Math.round(width * ((100 - high) / 100));
        let mobWidth = Math.round(width * (blue_range / 100)) - 10;
        
        qall[this.graphNumber].style['right'] = mobRight.toString() + 'px';
        qall[this.graphNumber].style['width'] = mobWidth.toString() + 'px';
        qall[this.graphNumber].style['top'] = '0';
        qall[this.graphNumber].style['height'] = '100%';
        qall[this.graphNumber].style['left'] = 'auto';
      }
    } else {
      // Desktop view
      let height = document.querySelector('.custom-graph__item').clientHeight;
      let screenTop = Math.round(height * ((100 - high) / 100));
      let screenHeight = Math.round(height * (blue_range / 100)) - 10;
      
      qall[this.graphNumber].style['top'] = screenTop.toString() + 'px';
      qall[this.graphNumber].style['height'] = screenHeight.toString() + 'px';
      qall[this.graphNumber].style['right'] = '0';
      qall[this.graphNumber].style['width'] = '100%';
      qall[this.graphNumber].style['left'] = 'auto';
    }
  }

  isPermission({ dynamic, statics }) {
    // Is graph static or dynamic
    this.prePermission();
    if (!this.statistic) {
      return dynamic;
    } else {
      return statics;
    }
  }

  getMaxOfArray(numArray) {
    //Return the max number in the numbers array
    return Math.max.apply(null, numArray);
  }

  prePermission() {
    const wrappers = document.querySelectorAll('.custom-graph');
    wrappers.forEach((item, i) => {
      const status = item.querySelector('.custom-graph__status');
      if (window.innerWidth > this.mobile) {
        let statusChildren = status.children;
        // Get html collection with two elements <div class="custom-graph__status-down">  and same up
        let searchInnerWidth = [...statusChildren].map(
          (child) => child.clientWidth
        );
        // Get width of upper elements
        const offsetStatus = this.getMaxOfArray(searchInnerWidth);
        item.style.paddingLeft = `${offsetStatus + 20}px`;
        status.style.left = `${offsetStatus + 16}px`;
        // Add left padding to all graph and for status bar
      } else {
        item.style.paddingLeft = `inherit`;
        status.style.left = `inherit`;
        // Padding from parent
      }
    });
  }

buildGraph() {
  // Set all data points to 50
  this.data.forEach((item) => {
    item.status = 50;
  });

  this.render();
  this.safeArea();

    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        // Update safezone and redraw lines/polygons
        this.safeArea();
        this.update(); // Redraw lines and polygons
        this.updateDots();
        this.isAuto();
      }, 250); // Reduced timeout for faster response
    });

    this.auto
      ? window.addEventListener('load', () => this.isAuto())
      : this.isAuto();
  }

  isAuto() {
    this.isPermission({
      dynamic: () => {
        this.updateDots((input, head, index) =>
          this.handlersDots(input, head, index)
        );
        this.handlersItem();
      },
      statics: () => this.updateDots(),
    })();
  }

  handlersDots(input, head, index) {
    if (!this.templates) {
      this.templates = this.container.querySelectorAll('.custom-graph__item');
    }
    input.addEventListener('input', () =>
      this.showSliderValue(input, head, index)
    );
    input.addEventListener('change', () => {
      if (this.templates && this.templates[index]) {
        this.addDot(this.templates[index], index);
      }
    });
    
    // Add keyboard input support for typing numbers
    // Store buffer and timeout on the input element itself to persist across events
    if (!input._keyboardBuffer) {
      input._keyboardBuffer = '';
      input._keyboardTimeout = null;
    }
    
    input.addEventListener('keydown', (e) => {
      // Don't interfere with Tab and Arrow keys - let them work normally for navigation
      if (e.key === 'Tab' || e.key.startsWith('Arrow')) {
        return; // Allow default behavior
      }
      
      // Handle number input and related keys
      const isNumber = e.key >= '0' && e.key <= '9';
      const isNumberInputKey = isNumber || 
          e.key === 'Enter' || 
          e.key === 'Backspace' || 
          e.key === 'Delete' ||
          e.key === '-' ||
          e.key === '+';
      
      if (isNumberInputKey) {
        // Clear any existing timeout
        if (input._keyboardTimeout) {
          clearTimeout(input._keyboardTimeout);
          input._keyboardTimeout = null;
        }
        
        // Handle Enter to apply the value immediately
        if (e.key === 'Enter') {
          e.preventDefault();
          if (input._keyboardBuffer) {
            this.applyKeyboardValue(input, head, index, input._keyboardBuffer);
            input._keyboardBuffer = '';
          }
          return;
        }
        
        // Handle minus at the start of input
        if (e.key === '-' && input._keyboardBuffer === '') {
          e.preventDefault();
          input._keyboardBuffer = '-';
          return;
        }
        
        // Handle plus at the start (optional, for clarity)
        if (e.key === '+' && input._keyboardBuffer === '') {
          e.preventDefault();
          // Just start with empty buffer, + is implicit
          return;
        }
        
        // Handle number input
        if (isNumber) {
          e.preventDefault();
          input._keyboardBuffer += e.key;
          
          // Auto-apply after a short delay or if buffer gets too long (3 digits)
          if (input._keyboardBuffer.replace('-', '').length >= 3) {
            this.applyKeyboardValue(input, head, index, input._keyboardBuffer);
            input._keyboardBuffer = '';
          } else {
            // Set timeout to apply value after user stops typing (800ms)
            input._keyboardTimeout = setTimeout(() => {
              if (input._keyboardBuffer) {
                this.applyKeyboardValue(input, head, index, input._keyboardBuffer);
                input._keyboardBuffer = '';
              }
            }, 800);
          }
        }
        
        // Handle Backspace/Delete to clear buffer
        if (e.key === 'Backspace' || e.key === 'Delete') {
          e.preventDefault();
          input._keyboardBuffer = '';
          if (input._keyboardTimeout) {
            clearTimeout(input._keyboardTimeout);
            input._keyboardTimeout = null;
          }
          return;
        }
      }
    });
    
    // Handle focus to prepare for keyboard input
    input.addEventListener('focus', () => {
      input._keyboardBuffer = '';
      if (input._keyboardTimeout) {
        clearTimeout(input._keyboardTimeout);
        input._keyboardTimeout = null;
      }
    });
  }
  
  applyKeyboardValue(input, head, index, valueStr) {
    if (!valueStr || valueStr === '' || valueStr === '-') {
      return;
    }
    
    let value = parseInt(valueStr, 10);
    
    // Check if value is NaN
    if (isNaN(value)) {
      return;
    }
    
    // The range is 0-100, but displayed as -50 to +50
    // Allow users to type either:
    // 1. Displayed value (-50 to +50) - convert to 0-100
    // 2. Actual slider value (0-100) - use directly
    
    // If value is in -50 to +50 range, convert to 0-100 range
    if (value >= -50 && value <= 50) {
      value = 50 + value; // Convert -50 to 0, 0 to 50, +50 to 100
    }
    
    // Clamp value to valid range
    const [min, max] = this.range;
    value = Math.max(min, Math.min(max, value));
    
    // Update the slider value
    input.value = value;
    
    // Trigger the update
    this.showSliderValue(input, head, index);
    this.addDot(this.templates[index], index);
  }

  handlersItem() {
    const $self = this;
    this.templates = this.container.querySelectorAll('.custom-graph__item');
    if (!this.templates || this.templates.length === 0) return;
    this.templates.forEach((item, i) => {
      const itemAvatar = this.find(item, '.custom-graph__item-avatar');

      itemAvatar.addEventListener('click', function (e) {
        e.preventDefault();
        $self.removeDot(item, i);
      });

      item.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        $self.removeDot(this, i);
      });
    });
  }

  addDot(item, index) {
    if (this.getDots(item)) return;
    const { statusSide, avatar } = this.data[index];
    const html = `<div class="custom-graph__item-circle">
                            <div class="custom-graph__item-count"></div>
                            ${
                              statusSide !== undefined
                                ? `<div class="custom-graph__item-side">${statusSide}</div>`
                                : `<img src="${avatar}" alt=""/> <div class="value__missed"></div>`
                            }
                         </div>
                             <div class="custom-graph__item-line"></div>
                             <div class="custom-graph__item-polygon"></div>
                             <div class="custom-graph__item-trace"></div>`;
    item.classList.toggle('active');
    item.querySelector('.custom-graph__item-head').innerHTML = html;
    this.updateDots();
    this.update();
    this.effectDot(item);
    // console.log(item)
    // this.dependency(item, index)
  }

  removeDot(item, index) {
    if (!this.getDots(item)) return;
    item.classList.toggle('inactive');
    this.find(item, '.custom-graph__item-head').innerHTML = '';
    this.removeInLastDotLine();
    this.update();
    this.deleteDataStatus(index);
  }

  removeInLastDotLine() {
    const arrActive = this.container.querySelectorAll(
      '.custom-graph__item:not(.inactive)'
    );
    const searchItem = arrActive[arrActive.length - 1];
    if (searchItem) {
      this.find(searchItem, '.custom-graph__item-line').style.width = '0';
    }
  }

  effectDot(item) {
    clearTimeout(this.effect);
    item.classList.add('effect');
    this.effect = setTimeout(() => {
      item.classList.remove('effect');
    }, 1000);
  }

  deleteDataStatus(index) {
    delete this.data[index]['status'];
  }

  setDataStatus(index, value) {
    this.data[index]['status'] = value;
  }

  updateDots(fn = undefined) {
    this.container
      .querySelectorAll('.custom-graph__range')
      .forEach((item, i) => {
        const input = item;
        const head = item.nextSibling;
        this.showSliderValue(input, head, i);
        fn && fn(input, head, i);
      });
  }

  searchInnerEl(item, next) {
    return {
      avatar: this.find(item, '.custom-graph__item-avatar'),
      circle: this.find(item, '.custom-graph__item-circle'),
      polygon: this.find(item, '.custom-graph__item-polygon'),
      line: this.find(item, '.custom-graph__item-line'),
      nextItem: this.find(next, '.custom-graph__item-circle'),
    };
  }

  find(item, selectorSearch) {
    return item instanceof HTMLDivElement && item.querySelector(selectorSearch);
  }

  getDots(item) {
    return this.find(item, '.custom-graph__item-circle');
  }

  searchInnerElNextSearch(item) {
    const { nextSibling } = item;
    if (nextSibling instanceof HTMLDivElement) {
      if (this.getDots(nextSibling)) {
        return nextSibling;
      } else {
        return this.searchInnerElNextSearch(nextSibling);
      }
    }
  }

  searchInnerElNext(item) {
    const { polygon, circle, avatar } = this.searchInnerEl(item);

    this.renderPolygon(polygon, circle, avatar);

    if (!this.getDots(item)) {
      item.classList.add('inactive');
      return;
    }

    this.renderLine(item);
  }

  renderLine(item) {
    const isNextElement = this.searchInnerElNextSearch(item);
    if (!isNextElement) return;
    const { circle, line, nextItem } = this.searchInnerEl(item, isNextElement);
    if (!line || !circle || !nextItem) return;
    const lineWidth = this.calculateWidth(circle, nextItem);
    const deg_an = this.getDegAn(circle, nextItem);
    // Use transform3d for hardware acceleration
    line.style.width = `${lineWidth}px`;
    line.style.transform = `translate3d(-50%, -50%, 0) rotate(${deg_an}deg) translate3d(50%, 50%, 0)`;
    line.style.willChange = 'transform';
  }

  renderPolygon(polygon, circle, avatar) {
    if (polygon && circle && avatar) {
      const polygonWidth = this.calculateWidth(circle, avatar);
      if (window.innerWidth <= this.mobile) {
        // In Mobile: Linie soll nur bis zum Mittelpunkt des Avatars reichen
        // Avatar ist 50px breit, also reduzieren um 25px (Hälfte)
        const avatarRect = this.getRect(avatar);
        const adjustedWidth = polygonWidth - (avatarRect.width / 2);
        polygon.style.width = `${Math.max(0, adjustedWidth)}px`;
        polygon.style.height = '0';
      } else {
        polygon.style.height = `${polygonWidth}px`;
        polygon.style.width = '0';
      }
    }
  }

  getRect(item) {
    return item.getBoundingClientRect();
  }

  calculateWidth(prevItem, nextItem) {
    const prev = this.getRect(prevItem);
    const next = this.getRect(nextItem);

    return Math.sqrt(
      Math.pow(next.x - prev.x, 2) + Math.pow(next.y - prev.y, 2)
    );
  }

  getDegAn(prevItem, nextItem) {
    const prev = this.getRect(prevItem);
    const next = this.getRect(nextItem);

    const an = Math.atan2(next.y - prev.y, next.x - prev.x);
    return (an * 180) / Math.PI;
  }

  interpolateColor(color1, color2, ratio) {
    // Convert hex colors to RGB
    const hex1 = color1.replace('#', '');
    const hex2 = color2.replace('#', '');
    const r1 = parseInt(hex1.substring(0, 2), 16);
    const g1 = parseInt(hex1.substring(2, 4), 16);
    const b1 = parseInt(hex1.substring(4, 6), 16);
    const r2 = parseInt(hex2.substring(0, 2), 16);
    const g2 = parseInt(hex2.substring(2, 4), 16);
    const b2 = parseInt(hex2.substring(4, 6), 16);
    
    // Interpolate
    const r = Math.round(r1 + (r2 - r1) * ratio);
    const g = Math.round(g1 + (g2 - g1) * ratio);
    const b = Math.round(b1 + (b2 - b1) * ratio);
    
    // Convert back to hex
    return '#' + [r, g, b].map(x => {
      const hex = x.toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    }).join('');
  }

  update() {
    this.templates = this.container.querySelectorAll('.custom-graph__item');
    this.templates.forEach((item) => {
      this.searchInnerElNext(item);
      // Update dashed line in mobile view - DISABLED (line is hidden in mobile)
      // if (window.innerWidth <= this.mobile) {
      //   this.updateDashedLine(item);
      // }
    });
  }
  
  updateDashedLine(item) {
    // Update the dashed line (:after pseudo-element) in mobile view
    // The line should extend from the left edge (visible part of item) to the avatar/vote point
    // This shows the area from minimum (Triggerthema, left) to the vote point (avatar)
    const rangeInput = item.querySelector('.custom-graph__range');
    const thumb = rangeInput ? rangeInput.nextSibling : null;
    const avatar = item.querySelector('.custom-graph__item-avatar');
    
    if (rangeInput && thumb && avatar && window.innerWidth <= this.mobile) {
      // Get positions relative to the item container
      const itemRect = item.getBoundingClientRect();
      const avatarRect = avatar.getBoundingClientRect();
      
      // Calculate avatar center position relative to item (in pixels)
      // Avatar might have negative margin, so we need to account for that
      const avatarCenterX = avatarRect.left - itemRect.left + (avatarRect.width / 2);
      const itemWidth = itemRect.width;
      
      // If avatar is outside the item bounds (negative position), we need to adjust
      // The visible left edge of the item starts at itemRect.left
      // For the line, we want to start at the visible left edge (0% of item width)
      // and extend to where the avatar center is
      
      // Calculate the actual visible start point (accounting for negative margins)
      // The line should start at the left visible edge of the item
      // and extend to the avatar center
      
      // Avatar center position relative to item left edge (can be negative)
      // We want the line to go from left edge (0) to avatar center
      // If avatar is at negative position, line width should be minimal
      // If avatar is within item bounds, line extends to avatar
      
      const avatarCenterRelative = avatarCenterX;
      
      // The line starts at left: 0% and extends to the avatar
      // If avatar is at position X (which can be negative), we need to handle that
      // For now, let's clamp the position and calculate width from visible left edge
      
      // Get the visible left edge position (accounting for item padding/margins)
      const itemsContainer = item.closest('.custom-graph__items');
      const itemsRect = itemsContainer ? itemsContainer.getBoundingClientRect() : null;
      
      if (itemsRect) {
        // Calculate position relative to items container
        const avatarCenterRelativeToItems = avatarRect.left - itemsRect.left + (avatarRect.width / 2);
        const itemsWidth = itemsRect.width;
        
        // Avatar center position as percentage of items container width
        const avatarCenterPercent = (avatarCenterRelativeToItems / itemsWidth) * 100;
        
        // INVERTED LOGIC: Lower values (avatar left, small %) = longer line
        // Higher values (avatar right, large %) = shorter line
        // Line should extend from left edge to avatar center
        // When avatar is far left (low value, e.g. 1%), line should be long
        // When avatar is far right (high value, e.g. 99%), line should be short
        // Invert: lineWidth = 100 - avatarCenterPercent (remaining distance from avatar to right)
        // But we want line from left to avatar, so: lineWidth = avatarCenterPercent is correct
        // Wait, but user wants: left avatar = long line
        // So: lineWidth should be INVERSE of avatar position
        // If avatar at 10% (left), line should be 90% (long)
        // If avatar at 90% (right), line should be 10% (short)
        
        // User wants: "je näher der Avatar bei 1, desto länger die Linie"
        // This means: avatar near left (low values) = longer line
        //             avatar near right (high values) = shorter line
        
        // The line should go from the avatar center to the left edge
        // When avatar is at 10% (left), line should be long (show more distance)
        // When avatar is at 90% (right), line should be short (show less distance)
        
        // Line starts at avatar position and extends to left edge (0%)
        // So: left position = avatarCenterPercent, width = avatarCenterPercent
        // Avatar at 10% → left: 10%, width: 10% (short) ❌
        // Avatar at 90% → left: 90%, width: 90% (long) ❌
        
        // Wait, if line goes FROM avatar TO left, then:
        // Avatar at 10% → line from 10% to 0% = width 10% (short) ❌
        // But user wants this to be LONG
        
        // Maybe the line shows the "remaining" area? Let's try inverted:
        // Line width = 100 - avatarCenterPercent
        // Avatar at 10% → width = 90% (long) ✓
        // Avatar at 90% → width = 10% (short) ✓
        // But where does it start? If it starts at left: 0%, it goes to 90%, passing the avatar
        
        // Actually, maybe the line should start at the left edge and have inverted width?
        // Or maybe the line starts at avatar and goes left, but the width calculation is inverted?
        
        // Let me try: line starts at avatar, width = 100 - avatarCenterPercent (distance from avatar to right edge)
        // No, that goes right, not left
        
        // Let's try: line starts at left edge (0%), width = 100 - avatarCenterPercent
        // Avatar at 10% → line from 0% to 90% (long, goes past avatar to right) - wrong direction
        
        // User says line should go left (Triggerthema direction), so maybe:
        // Line starts at avatar position, extends left, width = 100 - avatarCenterPercent
        // Avatar at 10% → line from 10% to (10% - 90%) = -80% (outside) - doesn't work
        
        // User wants: "je näher der Avatar bei 1, desto länger die Linie"
        // This means: avatar near left (low values) = longer line
        //             avatar near right (high values) = shorter line
        
        // Line starts at avatar position (right edge of line at avatar), extends left
        // right position = 100 - avatarCenterPercent (distance from right edge to avatar)
        // width = 100 - avatarCenterPercent (inverted: low position = long line)
        // Avatar at 10% → right: 90%, width: 90% → line from 0% to 90% (long) ✓
        // Avatar at 90% → right: 10%, width: 10% → line from 80% to 90% (short) ✓
        
        const rightPositionPercent = 100 - avatarCenterPercent;
        const lineWidthPercent = 100 - avatarCenterPercent; // Inverted: low position = long line
        
        // Line: right edge at avatar, extends left
        // right = 100 - avatarCenter%, width = 100 - avatarCenter%
        // Avatar at 10% → right: 90%, width: 90% → line from 0% to 90% (long) ✓
        // Avatar at 90% → right: 10%, width: 10% → line from 0% to 10% (short) ✓
        
        item.style.setProperty('--dashed-line-right', `${Math.max(0, Math.min(100, rightPositionPercent))}%`);
        item.style.setProperty('--dashed-line-width', `${Math.max(0, Math.min(100, lineWidthPercent))}%`);
        
        // Debug log
        console.log('[DASHED LINE] avatarCenterRelativeToItems:', avatarCenterRelativeToItems.toFixed(2), 
                    'itemsWidth:', itemsWidth.toFixed(2), 
                    'avatarCenterPercent:', avatarCenterPercent.toFixed(2) + '%',
                    'lineWidthPercent (inverted):', lineWidthPercent.toFixed(2) + '%');
      } else {
        // Fallback: use item-based calculation, but clamp to handle negative positions
        const lineWidth = Math.max(0, Math.min(100, (avatarCenterX / itemWidth) * 100));
        item.style.setProperty('--dashed-line-width', `${lineWidth}%`);
      }
    }
  }

  showSliderValue(inputSlider, thumb, index) {
      const { value, min: inputMin, max: inputMax } = inputSlider;
      const innerWidthSlider = inputSlider.clientWidth - 40;
      const bulletPosition = (value - inputMin) / (inputMax - inputMin);
      const count = bulletPosition * innerWidthSlider;
      let filter = 0;
      if (window.innerWidth <= this.mobile) {
          // Add 30px offset to account for extended range input padding
          thumb.style.left = `${count + 30}px`;
          thumb.style.bottom = 'auto';
      } else {
          thumb.style.bottom = `${count}px`;
          thumb.style.left = '50%';
      }

      const countDot = this.find(thumb, `.custom-graph__item-count`);
      if (countDot) {
          let color = '';
          if (this.guess.length) {
              let circle = thumb.querySelector('.custom-graph__item-circle');
              let right = this.guess[index].statusSide;
              var diff = Math.abs(+value - right);
              if (diff <= 4) {
                  circle.classList.remove('missed');
                  filter = 90;
                  // Use green for correct guess
                  color = '#9FE2BF';
              } else {
                  circle.querySelector('.value__missed').innerText = value;
                  circle.classList.add('missed');
                  filter = 180;
                  // Use red for missed guess
                  color = '#fa5252';
              }
          } else {
              // Color gradient: low values = red, middle = orange, high = green
              // Normalize value to 0-1 based on input range
              const normalizedValue = Math.min(Math.max((+value - inputMin) / (inputMax - inputMin), 0), 1);
              
              if (normalizedValue <= 0.5) {
                  // Red to Orange: 0% to 50%
                  const ratio = normalizedValue * 2; // 0 to 1
                  color = this.interpolateColor('#fa5252', '#E29635', ratio);
              } else {
                  // Orange to Green: 50% to 100%
                  const ratio = (normalizedValue - 0.5) * 2; // 0 to 1
                  color = this.interpolateColor('#E29635', '#9FE2BF', ratio);
              }
          }

          // Subtract 50 from the displayed value
          countDot.innerHTML = value - 50;
          if (color) {
              countDot.style.color = color;
              countDot.style.filter = 'none';
          } else {
              countDot.style.filter = `hue-rotate(-${filter}deg)  saturate(200%)`;
          }
          index !== undefined && this.setDataStatus(index, value);
      }
      if (this.statistic) {
          const countSide = this.find(thumb, `.custom-graph__item-side`);
          if (countSide) {
              countSide.innerHTML = value;
              
              // Color gradient: low values = red, middle = orange, high = green
              // Normalize value to 0-1 based on input range
              const normalizedValue = Math.min(Math.max((+value - inputMin) / (inputMax - inputMin), 0), 1);
              let color = '';
              
              if (normalizedValue <= 0.5) {
                  // Red to Orange: 0% to 50%
                  const ratio = normalizedValue * 2; // 0 to 1
                  color = this.interpolateColor('#fa5252', '#E29635', ratio);
              } else {
                  // Orange to Green: 50% to 100%
                  const ratio = (normalizedValue - 0.5) * 2; // 0 to 1
                  color = this.interpolateColor('#E29635', '#9FE2BF', ratio);
              }
              
              countSide.style.color = color;
              countSide.style.filter = 'none';
              index !== undefined && this.setDataStatus(index, value);
          }
      }
      this.getDependency(inputSlider, thumb, index, value);
      
      // Update dashed line for mobile view when slider value changes - DISABLED (line is hidden)
      // if (window.innerWidth <= this.mobile) {
      //   const item = thumb.closest('.custom-graph__item');
      //   if (item) {
      //     setTimeout(() => {
      //       this.updateDashedLine(item);
      //     }, 0);
      //   }
      // }
      
      // Update lines dynamically when slider value changes
      // Use requestAnimationFrame for smooth performance
      if (!this._updateRequestId) {
        this._updateRequestId = requestAnimationFrame(() => {
          this.update();
          this._updateRequestId = null;
        });
      }
  }


  getDependency(inputSlider, thumb, index, value) {
    if (this.dependency) {
      const countSide = this.find(thumb, `.custom-graph__item-side`);
      if (countSide) {
        const amount = countSide.innerHTML - value;
        const amountMax = amount < 0 ? amount * -1 : amount;
        countSide.setAttribute('data-dependency', amountMax);
        countSide.style.filter = `hue-rotate(-${
          amount < 0 ? 180 : 80
        }deg)  saturate(200%)`;
        // index !== undefined && this.setDataStatus(index, value);
      }
    }
  }

render() {
    const [down, up] = this.range;  // This is [1, 99]
    const [labelDown, labelUp, labelMiddle] = this.labelRange;

    // Transform the display range for labels
    const transformedDown = down - 50;  // Transforms 1 to -49
    const transformedUp = up - 50;      // Transforms 99 to +49
    const transformedMiddle = 0;        // Middle value (50) should display as 0

    // Helper function to render label (handles both string and object with text/subtext)
    const renderLabel = (label) => {
        if (typeof label === 'object' && label !== null) {
            const text = label.text || '';
            const subtext = label.subtext || '';
            if (subtext) {
                return `<div>${text}<div class="custom-graph__status-sub">${subtext}</div></div>`;
            }
            return text;
        }
        return label || '';
    };

    let htmlDown = `
        <div class="custom-graph__status">
            <div class="custom-graph__status-down">${renderLabel(labelUp)}</div>
            <div class="custom-graph__status-up">${renderLabel(labelDown)}</div>
            ${
                labelMiddle
                ? `<div class="custom-graph__status-middle">${renderLabel(labelMiddle)} (${transformedMiddle})</div>`
                : ''
            }
        </div>
    `;

  // Update htmlUp to include the value 50 for each data point
  let htmlUp = `
    <div class="custom-graph__items">  
    <div class="custom-graph__safezone"></div>
    ${this.data.map(({ status, statusSide, avatar, name }, i) => {
      return `<div class="custom-graph__item"><input class="custom-graph__range" type="range" value="${
        this.statistic && statusSide !== undefined ? statusSide : status
      }" min="${down}" max="${up}"><div class="custom-graph__item-head">
                ${
                  status !== undefined ||
                  (statusSide !== undefined && this.statistic)
                    ? `<div class="custom-graph__item-circle">
                    ${
                      this.statistic && statusSide !== undefined
                        ? ``
                        : `<div class="custom-graph__item-count">${status}</div>`
                    }
                 ${
                   statusSide !== undefined
                     ? `<div class="custom-graph__item-side">${statusSide}</div>`
                     : `<img src="${avatar}" alt=""/>`
                 }
                 
                 </div>
                     <div class="custom-graph__item-line"></div>
                     <div class="custom-graph__item-polygon"></div>`
                    : ''
                }
                </div>
                <div class="custom-graph__item-foot">
                    <div class="custom-graph__item-avatar">
                         ${
                           avatar ? `<img src="${avatar}" alt=""/>` : ''
                         }
                    </div>
                   <div class="custom-graph__item-name">${
                     name ? name : ''
                   }</div>
                </div>
            <div class="custom-graph__item-name_mobile">${
              name ? name : ''
            }</div>
            <div class="custom-graph__item-trace"></div>
            </div>`;
    })}
    </div>`;

  // ... (rest of the code)



    const html =
      htmlDown +
      htmlUp.split(`,`).join('') +
      (window.innerWidth <= this.mobile ? htmlDown : '');

    this.container.innerHTML = `<div class="custom-graph ${
      this.statistic ? `statistic` : ''
    }">${html}</div>`;

    // Initialize templates and render lines after graph is built
    this.templates = this.container.querySelectorAll('.custom-graph__item');
    this.update();
    
    return this;
  }

  getData() {
    return this.data;
  }

  getDifference() {
    var guess_result = [];
    var uu = 0;
    while (uu < this.guess.length) {
      var ii = 0;
      while (ii < this.data.length) {
        if (this.guess[uu].id === this.data[ii].id) {
          guess_result.push(
            Math.abs(this.guess[uu].statusSide - this.data[ii].status)
          );
        }
        ii += 1;
      }
      uu += 1;
    }
    return guess_result;
  }
}
