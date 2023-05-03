
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

    // Retrieve Each offer image from the Content body to be able to display the offers.
    const offerList = document.querySelectorAll('.offers');
    offerList.forEach((offer) => {
       const img = offer.dataset.img;
       const id = offer.dataset.id;
       const offerImgEl = offer.querySelector(`#offerimg-${id}`);
       console.log(offerImgEl.src);
       offerImgEl.src = `/static/img/${img}`;
    });

    /* ----------------------------------Display Pages----------------------------------------- */

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

    /* ----------------------------------Filter Search----------------------------------------- */

    // The search bar element
    const searchEl = document.getElementById('searchBar');
    // Select the menu container element
    const pizzaContainer = $('#menu');
    // We turn the node list to an array to use filter on it.
    const pizzaArray = Array.from(document.querySelectorAll(('.pizza')));

    // Listen for input inside the search bar, does not require submit
    searchEl.addEventListener("input", () => {
        searchData(searchEl.value);
    });

    // A search function that filters the pizzas in the dom by name and repopulates based on filter
    const searchData = (value) => {
        const filteredPizzas = pizzaArray.filter((pizza) => {
            const pizzaName = pizza.dataset.name;
            return pizzaName.toLowerCase().includes(value.toLowerCase());
        });

        // remove all the existing pizza items from the container
        pizzaContainer.empty();

        // add the filtered pizza items to the container
        filteredPizzas.forEach((pizza) => {
            pizzaContainer.append(pizza);
        });
    }

});

