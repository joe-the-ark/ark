class AppRange {
    constructor({container, innerWrapper = 'rang', data, callback, update, load, loadEnd}) {
        this.container = document.querySelector(container);
        this.data = data;
        this.callback = callback;
        this.update = update;
        this.load = load;
        this.loadEnd = loadEnd;
        this.innerWrapper = innerWrapper;
        this.buildRange();
    }


    async buildRange() {
        await this.render();
        this.defaultLoad();
        window.addEventListener('load', () => this.handlers());
    }

    handlers() {
        this.onClick();
        this.loadEnd && this.loadEnd();
    }


    onClick() {
        this.getItems((item, i) => {
            this.callback && item.addEventListener('click', () => this.onChange(item, i));
        });

    }

    getItems(fn) {
        this.container.querySelectorAll('.rang__item').forEach(fn);
    }

    onChange(item, index) {
        this.updateRange();
        this.callback(item, index)
    }

    updateRange() {
        this.getItems((item, i) => {
            this.update && this.update(item, i);
        });
    }

    defaultLoad() {
        this.load && this.load(this.container.children)
        this.getItems((item, i) => {
            const count = item.querySelector('.rang__item-count');
            // Only apply filter if element doesn't have tension-high class
            // (tension-high elements should be dark red, not color-shifted)
            if (!count.classList.contains('tension-high')) {
                count.style.filter = `hue-rotate(-${180 - +count.innerHTML}deg)  saturate(200%)`;
            }
            window.innerWidth > 1200 && i === 0 && item.classList.add('active')
        })
    }

    render() {
        // Helper function to format tension with sign
        const formatTension = (tension) => {
            if (tension > 0) {
                return `+${tension}`;
            } else if (tension < 0) {
                return `${tension}`; // Already has minus sign
            } else {
                return `0`; // Neutral
            }
        };
        
        let html = `
            <div class="${this.innerWrapper}">${this.data.map(({value, tension}, i) => {
            // console.log(value)
            const [firstName, lastName] = value.split(' ');
            const formattedTension = formatTension(tension);
            return `<div class="rang__item swiper-slide" data-tension="${tension}" data-tension-sign="${tension > 0 ? 'positive' : tension < 0 ? 'negative' : 'neutral'}">
                        <div class="rang__item-wrapper">
                            <div class="rang__item-name">
                                ${firstName}
                            </div>
                            <div class="rang__item-count" data-tension="${tension}">
                                ${formattedTension}
                            </div>
                            <div class="rang__item-name">
                                ${lastName}
                            </div>
                        </div>
                    </div>`
        })}</div><div class="rang-button-prev"></div>
                    <div class="rang-button-next"></div>
                    <div class="swiper-pagination"></div>`;

        this.container.innerHTML = html.split(`,`).join('');

        return this;
    }

}
