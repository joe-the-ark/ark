class AppFeedback {
    constructor({container, data, loadEnd, update}) {
        //this.order = order;
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

        // this.onClick();
    }


    render() {

        // const htmlHead = `<div class="fields-fill__head swiper-wrapper">${this.data.map(({name, avatar}, i) =>
        //                     `<div class="swiper-slide">
        //                         <div class="fields-fill__connect">
        //                                         <img src="${avatar}" alt="avatar ${name}"/>
                                                
        //                         </div>
        //                     </div>`).join('')}
        //                 </div>`;

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


//         const htmlHead = `<div class="fields-fill__head swiper-wrapper">${this.data.map(({name, avatar}, i) =>
//             `<div class="swiper-slide">
// <div class="fields-fill__connect">
//                                 <img src="${avatar}" alt="avatar ${name}"/>
//                                 <div class="fields-fill__connect-name">${name}</div>
// </div>
//                             </div>`).join('')}</div>`;


        const htmlBody = `<div class="fields-fill__body">${this.data.map(({feedback}) =>
            `<div class="fields-fill__field-wrapper">${feedback.map(({title, text}) =>
                `<div class="fields-fill__field">
                                <p class="bold">
                                   ${title}
                                </p>
                                a<textarea minlength="25" placeholder="Schreib hier dein Feedback…">${text}</textarea>
                            </div>
        `).join('')}</div>`).join('')}</div>`;

        this.container.innerHTML = `<div class="fields-fill swiper-container">
                                        ${htmlHead}${htmlBody}
                                        <div class="slider-button-prev"></div>
                                        <div class="slider-button-next"></div>
                                    </div>`;
        //this.order = this.order + 1;
        return this;
    }

    
    getData() {
        return this.data;
    }

}