class AppFeedback {
    constructor({container, data, loadEnd, update}) {
        this.container = document.querySelector(container);
        this.data = data;
        this.loadEnd = loadEnd;
        this.update = update;
        this.buildRange();
    }


    async buildRange() {
        await this.render();
        window.addEventListener('load', () => this.handlers());
    }

    handlers() {
        this.bodyItems = document.querySelectorAll('.fields-fill__field-wrapper');
        this.loadEnd && this.loadEnd(this.bodyItems);
        this.update && this.update();

    }


    render() {


        const htmlHead = `<div class="fields-fill__head swiper-wrapper">
                        <div class="fields-fill__connect"> 
                        <img src="${this.data[0].avatar}" alt="">
                        <div class="fields-fill__connect-name">${this.data[0].name}</div>
                                                <ul id="menu" class="dropdown-menu">
                    ${this.data.map(({name, avatar}, i) =>
                            `<li class="player">${name}</li>`).join('')}
                        </ul>
                        </div>
                        </div>`;




        const htmlBody = `<div class="fields-fill__body">${this.data.map(({feedback}) =>
            `<div class="fields-fill__field-wrapper">${feedback.map(({title, text}) =>
                `<div class="fields-fill__field">
                                <p class="bold">
                                   ${title}
                                </p>
                                a<textarea class="textarea_" minlength="25" placeholder="Schreib hier dein Feedback…">${text}</textarea>
                            </div>
        `).join('')}</div>`).join('')}</div>`;

        this.container.innerHTML = `<div class="fields-fill swiper-container">
                                        ${htmlHead}${htmlBody}

                                    </div>`;
        return this;
    }

    
    getData() {
        return this.data;
    }

}