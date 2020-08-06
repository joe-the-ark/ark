class AppUiSlider {
    constructor({inputSlider, countSlider, thumbSlider, range, callback}) {
        this.inputSlider = document.querySelector(inputSlider);
        this.countSlider = document.querySelector(countSlider);
        this.thumbSlider = document.querySelector(thumbSlider);
        this.callback = callback;
        this.range = range;

        this.didUpdate().update();
    }

    showSliderValue() {
        const {value, max} = this.inputSlider;
        const innerWidthSlider = this.inputSlider.clientWidth - 110;
        const bulletPosition = (value / max);
        const count = bulletPosition * innerWidthSlider;

        this.countSlider.innerHTML = value;
        this.thumbSlider.style.transform = `translateX(${count}px)`;

        this.callback(value)
    }

    didUpdate() {
        const {parentNode} = this.inputSlider;
        const newMin = document.createElement('div');
        newMin.innerHTML = `<span>${this.range.min}</span><span>${this.range.max}</span>`
        parentNode.append(newMin);

        this.inputSlider.setAttribute('min', this.range.min);
        this.inputSlider.setAttribute('max', this.range.max);
        this.thumbSlider.style.transform = `translateX(8.71717px)`;

        return this;
    }

    update() {
        this.inputSlider.addEventListener("input", () => this.showSliderValue());
        this.inputSlider.addEventListener("change", () => {

        });
        window.addEventListener("resize", () => this.showSliderValue());
    }

}
