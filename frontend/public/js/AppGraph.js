class AppGraph {
    constructor({ container, data, safezoneData = [], graphNumber=0, range, statistic, mobile, labelRange, auto = true, dependency = false, guess = [] }) {
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
        this.effect = function() {};

        this.auto && this.buildGraph();
        this.safeLow = 0;
        this.safeHigh = 0;
    }

    safeArea() {
        let sum = () => {
            let itog = 0;
            for (let item of this.safezoneData) {
                itog+= item;
            }
            return itog
        }
        let median = Math.round(sum()/this.safezoneData.length);
        var low = median - 16;
        var high = median + 16;
        if (low < 0) {
            low = 0;
        }
        if (high > 100) {
            high = 100;
        }
        let slide = ".slide-"+this.graphNumber.toString()
        let spanung = document.querySelector(slide);
        this.container.children[0].setAttribute('low',low)
        this.container.children[0].setAttribute('high',high)
        this.safeLow = low;
        this.safeHigh = high;
        var blue_range = high - low;
        let halfAvatar = document.querySelector('div.custom-graph__item-avatar').clientHeight/2;
        let height = document.querySelector('.custom-graph__item').clientHeight;
        let width = document.querySelector('.custom-graph__item').clientWidth;
        let mobRight = Math.round(width*((100-high)/100));
        let mobWidth = Math.round(width*(blue_range/100))-10;
        let screenTop = Math.round(height*((100-high)/100));
        let screenHeight = Math.round(height*(blue_range/100))-10;

        let qall = this.container.parentNode.querySelectorAll('.custom-graph__safezone');

        if (window.innerWidth <= this.mobile) {
            qall[this.graphNumber].style['right'] = mobRight.toString() + "px";
            qall[this.graphNumber].style['width'] = mobWidth.toString() + "px";
            qall[this.graphNumber].style['top'] = "0";
            qall[this.graphNumber].style['height'] = '100%-2px';
        } else {
            qall[this.graphNumber].style['top'] = screenTop.toString() + "px";
            qall[this.graphNumber].style['height'] = screenHeight.toString() + "px";
            qall[this.graphNumber].style['right'] = "0";
            qall[this.graphNumber].style['width'] = '100%-2px';
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
                let searchInnerWidth = [...statusChildren].map((child) => child.clientWidth);
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
        this.render();
        this.safeArea();

        window.addEventListener('resize', () => {
            setTimeout( () => {
                this.safeArea();
                this.updateDots();
                this.isAuto();
            }, 500)
            
        });

        this.auto ? window.addEventListener('load', () => this.isAuto()) : this.isAuto();
    }

    isAuto() {
        this.isPermission({
            dynamic: () => {
                this.updateDots((input, head, index) => this.handlersDots(input, head, index));
                this.handlersItem();
            },
            statics: () => this.updateDots()
        })();
    }

    handlersDots(input, head, index) {
        input.addEventListener('input', () => this.showSliderValue(input, head, index));
        input.addEventListener('change', () => this.addDot(this.templates[index], index));
    }

    handlersItem() {
        const $self = this;
        this.templates.forEach((item, i) => {
            const itemAvatar = this.find(item, '.custom-graph__item-avatar');

            itemAvatar.addEventListener('click', function(e) {
                e.preventDefault();
                $self.removeDot(item, i);
            });

            item.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                $self.removeDot(this, i);
            })
        })
    }

    addDot(item, index) {
            if (this.getDots(item)) return;
            const { statusSide, avatar } = this.data[index];
            const html = `<div class="custom-graph__item-circle">
                            <div class="custom-graph__item-count"></div>
                            ${statusSide !== undefined ? `<div class="custom-graph__item-side">${statusSide}</div>` : `<img src="${avatar}" alt=""/> <div class="value__missed"></div>`}
                         </div>
                             <div class="custom-graph__item-line"></div>
                             <div class="custom-graph__item-polygon"></div>
                             <div class="custom-graph__item-trace"></div>`;
        item.classList.toggle('inactive');
        item.querySelector('.custom-graph__item-head').innerHTML = html;
        this.updateDots();
        this.update();
        this.effectDot(item);
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
        const arrActive = this.container.querySelectorAll('.custom-graph__item:not(.inactive)');
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
        }, 1000)
    }

    deleteDataStatus(index) {
        delete this.data[index]['status'];
    }

    setDataStatus(index, value) {
        this.data[index]['status'] = value;
    }

    updateDots(fn = undefined) {
        this.container.querySelectorAll('.custom-graph__range').forEach((item, i) => {
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
            nextItem: this.find(next, '.custom-graph__item-circle')
        }
    }

    find(item, selectorSearch) {
        return item instanceof HTMLDivElement && item.querySelector(selectorSearch);
    }

    getDots(item) {
        return this.find(item, '.custom-graph__item-circle');
    }

    searchInnerElNextSearch(item) {
        const {nextSibling} = item;
        if (nextSibling instanceof HTMLDivElement) {
            if (this.getDots(nextSibling)) {
                return nextSibling
            } else {
                return this.searchInnerElNextSearch(nextSibling)
            }
        }
    }

    searchInnerElNext(item) {
        const {polygon, circle, avatar} = this.searchInnerEl(item);

        this.renderPolygon(polygon, circle, avatar);

        if (!this.getDots(item)) {
            item.classList.add('inactive');
            return;
        }

        this.renderLine(item);
    };

    renderLine(item) {
        const isNextElement = this.searchInnerElNextSearch(item);
        if (!isNextElement) return;
        const {circle, line, nextItem} = this.searchInnerEl(item, isNextElement);
        const lineWidth = this.calculateWidth(circle, nextItem);
        const deg_an = this.getDegAn(circle, nextItem);
        line.style.width = `${lineWidth}px`;
        line.style.transform = `translate(-50%, -50%) rotate(${deg_an}deg) translate(50%, 50%)`;
    }

    renderPolygon(polygon, circle, avatar) {
        if (polygon && circle && avatar) {
            const polygonWidth = this.calculateWidth(circle, avatar);
            if (window.innerWidth <= this.mobile) {
                polygon.style.width = `${polygonWidth}px`;
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

        return Math.sqrt(Math.pow(next.x - prev.x, 2) + Math.pow(next.y - prev.y, 2));
    }

    getDegAn(prevItem, nextItem) {
        const prev = this.getRect(prevItem);
        const next = this.getRect(nextItem);

        const an = Math.atan2(next.y - prev.y, next.x - prev.x);
        return an * 180 / Math.PI;
    }

    update() {
        this.templates = this.container.querySelectorAll('.custom-graph__item');
        this.templates.forEach((item) => {
            this.searchInnerElNext(item);
        });
        

    }

    showSliderValue(inputSlider, thumb, index) {
        
        const {value, max} = inputSlider;
        const innerWidthSlider = inputSlider.clientWidth - 40;
        const bulletPosition = (value / max);
        const count = bulletPosition * innerWidthSlider;
        let filter = 0;
        if (window.innerWidth <= this.mobile) {
            thumb.style.left = `${count}px`;
            thumb.style.bottom = 'auto';

        } else {
            thumb.style.bottom = `${count}px`;
            thumb.style.left = '50%';
        }

        const countDot = this.find(thumb, `.custom-graph__item-count`);
        if (countDot) {
            let hueRotate = 0;
            if (this.guess.length) {
                let circle = thumb.querySelector('.custom-graph__item-circle');
                let right = this.guess[index].statusSide;
                var diff = Math.abs(+value - right)
                if (diff <= 4){
                    circle.classList.remove('missed');
                    filter = 90
                }else{
                    console.log('circle', circle)
                    circle.querySelector('.value__missed').innerText = value;
                    circle.classList.add('missed');
                    filter = 180
                }
            }
            else {
                filter = 180 - +value;
            }
    
            // For guess part, showing the difference of the guess and the value
            countDot.innerHTML = value;
            if (this.guess.length){
                countDot.innerHTML = '±' + Math.abs(value - this.guess[index].statusSide).toString()
                if (Math.abs(value - this.guess[index].statusSide) === 0){
                    countDot.innerHTML = 'Perfect'
                }
            }

            countDot.style.filter = `hue-rotate(-${filter}deg)  saturate(200%)`;
            index !== undefined && this.setDataStatus(index, value);
        }
        if (this.statistic) {
            const countSide = this.find(thumb, `.custom-graph__item-side`);
            if (countSide) {
                countSide.innerHTML = value;
                countSide.style.filter = `hue-rotate(-${180 - +value}deg)  saturate(200%)`;
                index !== undefined && this.setDataStatus(index, value);
            }
        }
        this.getDependency(inputSlider, thumb, index, value);
        this.update();
    }

    getDependency(inputSlider, thumb, index, value) {
        if (this.dependency) {
            const countSide = this.find(thumb, `.custom-graph__item-side`);
            if (countSide) {
                const amount = countSide.innerHTML - value;
                const amountMax = amount < 0 ? amount * -1 : amount;
                countSide.setAttribute('data-dependency', amountMax);
                countSide.style.filter = `hue-rotate(-${amount < 0 ? 180 : 80}deg)  saturate(200%)`;
            }
        }
    }

    render() {
        const [down, up] = this.range;
        const [labelDown, labelUp, labelMiddle] = this.labelRange;
        let htmlDown = `
                    <div class="custom-graph__status">
                        <div class="custom-graph__status-down">${labelDown}</div>
                        <div class="custom-graph__status-up">${labelUp}</div>
                        ${labelMiddle ? `<div class="custom-graph__status-middle">${labelMiddle}</div>` : ''}
                    </div>
            `;

        let htmlUp = `
            <div class="custom-graph__items">  
            <div class="custom-graph__safezone"></div>
            ${this.data.map(({status, statusSide, avatar, name}, i) => {
            return `<div class="custom-graph__item"><input class="custom-graph__range" type="range" value="${this.statistic && statusSide !== undefined ? statusSide : status}" min="${down}" max="${up}"><div class="custom-graph__item-head">
                        ${status !== undefined || (statusSide !== undefined && this.statistic) ? `<div class="custom-graph__item-circle">
                            ${this.statistic && statusSide !== undefined ? `` : `<div class="custom-graph__item-count">${status}</div>`}
                         ${statusSide !== undefined ? `<div class="custom-graph__item-side">${statusSide}</div>` : `<img src="${avatar}" alt=""/>`}
                         
                         </div>
                             <div class="custom-graph__item-line"></div>
                             <div class="custom-graph__item-polygon"></div>` : ''}
                        </div>
                        <div class="custom-graph__item-foot">
                            <div class="custom-graph__item-avatar">
                                 ${avatar ? `<img src="${avatar}" alt=""/>` : ''}
                            </div>
                           <div class="custom-graph__item-name">${name ? name : ''}</div>
                        </div>
                    <div class="custom-graph__item-name_mobile">${name ? name : ''}</div>
                    <div class="custom-graph__item-trace"></div>
                    </div>`
        })}
            </div>`;

        const html = htmlDown + htmlUp.split(`,`).join('') + (window.innerWidth <= this.mobile ? htmlDown : '');

        this.container.innerHTML = `<div class="custom-graph ${this.statistic ? `statistic` : ''}">${html}</div>`;

        return this;
    }

    getData() {
        return this.data
    }

    getDifference(){
        var guess_result = []
        var uu = 0
        while (uu < this.guess.length){
            var ii = 0
            while (ii < this.data.length){
                if (this.guess[uu].id === this.data[ii].id){
                    guess_result.push(Math.abs(this.guess[uu].statusSide - this.data[ii].status))
                }
                ii += 1
            }
            uu += 1
        }
        return guess_result
    }
        
}
