
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

    /* ----------------------------------Display Filter----------------------------------------- */
    // If the endpoint menu is called, we display the filter menu.
    if(window.location.pathname == '/menu/') {
        $("#filter").show();
        $("#menu").show();
    } else {
        $("#filter").hide();
        $("#menu").hide();
    }
    if(window.location.pathname == '/offer/') {
        $("#offer").show();
    } else {
        $("#offer").hide();
    }
});

