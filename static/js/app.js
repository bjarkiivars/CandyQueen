
// Waits for the DOM to be loaded, helps with accessing DOM elements with query selectors.
document.addEventListener('DOMContentLoaded', function() {

    // Select the menu container element
    const pizzaContainer = $('#menu');
    // Select all pizzas, with the class .pizza
    const pizzaList = document.querySelectorAll('.pizza');


    /* ----------------------------------Display Pizza----------------------------------------- */

    // Retrieve Each pizza image from the Content body to be able to display the pizzas.
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

    // If the endpoint offers is called, we display the offers menu.
    if(window.location.pathname == '/offers/') {
        $("#offer").show();
    } else {
        $("#offer").hide();
    }

    /* ----------------------------------Filter Search----------------------------------------- */

    // The search bar element
    const searchEl = document.getElementById('searchBar');

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

    /* ----------------------------------Filter Type----------------------------------------- */

    const pizzaTypes = document.getElementById('pizzaTypes');

    // The elements that are populated in the DOM from our view
    const typeEl = document.querySelectorAll('.pizzaType');

    pizzaTypes.addEventListener("change", event =>
        filterType(event.target.value)
    );

    const filterType = (value) => {
        let filteredPizzas;

        if (value === '' || value.toLowerCase() === 'n/a') {
            // Show all pizzas
            filteredPizzas = pizzaArray;

        } else {

            // find the corresponding pizza type from both the Pizza class and pizzaType class
            // Then assign the value.
            typeEl.forEach((pizzaType) => {
                if (value === pizzaType.dataset.type) {
                    value = pizzaType.dataset.id;
                }
            });

            filteredPizzas = pizzaArray.filter((pizza) => {
                const typeId = pizza.dataset.type;
                return typeId === value;
            });
        }

        pizzaContainer.empty();

        filteredPizzas.forEach((pizza) => {
           pizzaContainer.append(pizza);
        });
    }

    /* ----------------------------------Order by Price, Name----------------------------------------- */

    // Get the select element for Asc or Desc order
    const orderChoiceEl = document.getElementById('orderChoice');

    // We want to have this element hidden until the user wants to order by price or name
    const ascOrDescEl = document.getElementById('ascOrDesc');
    $(ascOrDescEl).hide();

    const orderEl = document.getElementById('pizzaOrderBy');

    // Check which order by option is selected and send it to a helper function
    orderEl.addEventListener("change", event =>
        orderBy(event.target.value)
    );

    const orderBy = (value) => {
        if (value === 'Name') {
            /* Send to name */
            orderName();
        } else if ( value === 'Price') {
            /* Send to price */
        }
        if($(ascOrDescEl).is(":visible")) {
            $(ascOrDescEl).show("slow");
        }
    }

    const orderName = () => {
        if($(ascOrDescEl).is(":hidden")) {
                $(ascOrDescEl).show("slow");
        }
        const sortHandler = () => {
            if (orderChoiceEl.value === 'Ascending') {
                /* sort Ascending */

                const sortedPizzas = Array.from(pizzaList);
                sortedPizzas.sort((a,b) => {
                   const pizzaA = a.dataset.name.toLowerCase();
                   const pizzaB = b.dataset.name.toLowerCase();

                   if (pizzaA < pizzaB) {
                       return -1;
                   }
                   if (pizzaA > pizzaB) {
                       return 1;
                   }
                   return 0;
                });

                pizzaContainer.empty();
                pizzaContainer.append(sortedPizzas);

            } else if (orderChoiceEl.value === 'Descending') {
                /* sort Descending */

                const sortedPizzas = Array.from(pizzaList);
                sortedPizzas.sort((a, b) => {
                    const pizzaA = a.dataset.name.toLowerCase();
                    const pizzaB = b.dataset.name.toLowerCase();

                    if (pizzaA < pizzaB) {
                        return 1;
                    }
                    if (pizzaA > pizzaB) {
                        return -1;
                    }
                    return 0;
                });

                pizzaContainer.empty();
                pizzaContainer.append(sortedPizzas);

            } else {
                /* show all the pizzas again */
                pizzaContainer.empty();
                pizzaContainer.append(pizzaList);
            }
      };

      // remove previous event listener if exists
      orderChoiceEl.removeEventListener("change", sortHandler);

      // add new event listener, after removal
      orderChoiceEl.addEventListener("change", sortHandler);
    };

    const orderPrice = () => {

    }





});
