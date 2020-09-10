class AppGraph {
    constructor({ container, data, range, statistic, mobile, labelRange, auto = true, dependency = false }) {
        this.container = document.querySelector(container);
        this.data = data;
        this.range = range;
        this.labelRange = labelRange;
        this.statistic = statistic;
        this.mobile = mobile;
        this.auto = auto;
        this.dependency = dependency;
        this.effect = function() {};

        this.auto && this.buildGraph();
    }

    safeArea() {
        var css_change = function(t, s) {
            s = document.createElement('style');
            s.innerText = t;
            document.body.appendChild(s);
        };
        var data_list = []
        var uu = 0;
        while (uu < this.data.length) {
            data_list.push((this.data)[uu].statusSide)
            uu += 1;
        }

        let _median = arr => {
            arr.sort();
            //求中位数
            if (arr.length % 2 == 0) {
                return (arr[arr.length / 2 - 1] + arr[arr.length / 2]) / 2;
            } else {
                return arr[Math.floor(arr.length / 2)];
            }
        };
        var median = _median(data_list);
        var low = median - 16;
        var high = median + 16;
        if (low < 0) {
            low = 0;
        }
        if (high > 100) {
            high = 100;
        }
        var blue_range = high - low;
        //console.log(this.data);
        css_change(`.statistic .custom-graph__items:before{left:${low}%;width:min(${blue_range}%);}`);
    }

    isPermission({ dynamic, statics }) {
        this.prePermission();
        if (!this.statistic) {
            return dynamic;
        } else {
            return statics;
        }
    }

    getMaxOfArray(numArray) {
        return Math.max.apply(null, numArray);
    }

    prePermission() {
        const wrappers = document.querySelectorAll('.custom-graph');
        wrappers.forEach((item, i) => {
            const status = item.querySelector('.custom-graph__status');
            if (window.innerWidth > this.mobile) {

                const statusChildren = status.children;
                const searchInnerWidth = [...statusChildren].map((child) => child.clientWidth);
                const offsetStatus = this.getMaxOfArray(searchInnerWidth);
                item.style.paddingLeft = `${offsetStatus + 20}px`;
                status.style.left = `${offsetStatus + 16}px`;
            } else {
                item.style.paddingLeft = `inherit`;
                status.style.left = `inherit`;
            }
        });
    }

    buildGraph() {
        this.render();

        window.addEventListener('resize', () => {
            this.updateDots()
            this.prePermission();
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
                            ${statusSide !== undefined ? `<div class="custom-graph__item-side">${statusSide}</div>` : `<img src="${avatar}" alt=""/>`}
                         </div>
                             <div class="custom-graph__item-line"></div>
                             <div class="custom-graph__item-polygon"></div>
                             <div class="custom-graph__item-trace"></div>`;
        item.classList.toggle('inactive');
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
        this.safeArea();
    }

    showSliderValue(inputSlider, thumb, index) {
        const {value, max} = inputSlider;
        const innerWidthSlider = inputSlider.clientWidth - 40;
        const bulletPosition = (value / max);
        const count = bulletPosition * innerWidthSlider;
        if (window.innerWidth <= this.mobile) {
            thumb.style.left = `${count}px`;
            thumb.style.bottom = 'auto';

        } else {
            thumb.style.bottom = `${count}px`;
            thumb.style.left = '50%';
        }
        const countDot = this.find(thumb, `.custom-graph__item-count`);
        if (countDot) {
            countDot.innerHTML = value;
            countDot.style.filter = `hue-rotate(-${180 - +value}deg)  saturate(200%)`;
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
                // index !== undefined && this.setDataStatus(index, value);
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
}