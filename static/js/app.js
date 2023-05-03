
// Waits for the DOM to be loaded, helps with accessing DOM elements with query selectors.
document.addEventListener('DOMContentLoaded', function() {
    /* ----------------------------------Display Pizza----------------------------------------- */

    // Retrieve Each pizza image from the Content body to be able to display the pizzas.
    const pizzaList = document.querySelectorAll('.pizza');
    pizzaList.forEach((pizza) => {
        const img = pizza.dataset.img;
        const id = pizza.dataset.id;
        const imgElm = pizza.querySelector(`#img-${id}`);
        imgElm.src = `/static/img/${img}`;
    });

    /* ----------------------------------Display Offer----------------------------------------- */

    const offerList = document.querySelectorAll('.offers');
    offerList.forEach((offer) => {
       const img = offer.dataset.img;
       const id = offer.dataset.id;
       const offerImgEl = offer.querySelector(`#offerimg-${id}`);
       console.log(offerImgEl.src);
       offerImgEl.src = `/static/img/${img}`;
    });

    /* ----------------------------------Display Filter----------------------------------------- */
    // If the endpoint menu is called, we display the filter menu.
    if(window.location.pathname == '/menu/') {
        $("#filter").show();
        $("#menu").show();
    } else {
        $("#filter").hide();
        $("#menu").hide();
    }
    if(window.location.pathname == '/offers/') {
        $("#offer").show();
    } else {
        $("#offer").hide();
    }
});

