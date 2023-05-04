
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

    /**************************** Main Order by function *****************************/
    
    const orderBy = (value) => {
        if (value === 'Name') {
            /* Send to name */
            orderName();
            // set the default value to Ascending, as it should be Ascending first
            ascOrDescEl.value = 'Ascending';
            // run the sortNameHandler function with the default value of Ascending
            sortNameHandler();

        } else if ( value === 'Price') {
            /* Send to price */
            orderPrice()
            // set the default value to Ascending, as it should be Ascending first
            ascOrDescEl.value = 'Ascending';
            // run the sortPriceHandler function with the default value of Ascending
            sortPriceHandler();
        } else {
            console.log('I was in here');
            if($(ascOrDescEl).is(":visible")) {
                $(ascOrDescEl).hide("slow");
            }

            // Repopulate the DOM when we select nothing in the Order by drop down.
            pizzaContainer.empty();
            pizzaContainer.append(pizzaList);
        }
    }

    /**************************** Order Wrapper functions *****************************/

    const orderName = () => {
        if($(ascOrDescEl).is(":hidden")) {
                $(ascOrDescEl).show("slow");
        }
        // remove previous event listener if exists
        orderChoiceEl.removeEventListener("change", sortNameHandler);

        // add new event listener, after removal
        orderChoiceEl.addEventListener("change", sortNameHandler);
    };

    const orderPrice = () => {
        if($(ascOrDescEl).is(":hidden")) {
            $(ascOrDescEl).show("slow");
        }

        // remove previous event listener if exists
        orderChoiceEl.removeEventListener("change", sortPriceHandler);

        // add new event listener, after removal
        orderChoiceEl.addEventListener("change", sortPriceHandler);
    }


    /**************************** Event Handler functions *****************************/

    // Handles the event listener changes and fires once whenever we use the order by
    const sortNameHandler = () => {
        if (orderChoiceEl.value === 'Ascending') {
            /* sort Ascending */

            // Turn the list to an Array, so we can sort through it
            const sortedPizzasAsc = Array.from(pizzaList);
            // Here we order by Ascending
            sortedPizzasAsc.sort((a,b) => {
               const pizzaA = a.dataset.name.toLowerCase();
               const pizzaB = b.dataset.name.toLowerCase();

               // With the -1, 1 and 0, we are specifying the order in which the elements get sorted

                // if pizzaA comes before pizzaB we return -1
               if (pizzaA < pizzaB) {
                   return -1;
               }
               // if pizzaB comes before pizzaA we return 1
               if (pizzaA > pizzaB) {
                   return 1;
               }
               // if they are equal we return 0, so those items do not need to swapped
               return 0;
            });

            pizzaContainer.empty();
            pizzaContainer.append(sortedPizzasAsc);

        } else if (orderChoiceEl.value === 'Descending') {
            /* sort Descending */

            // Functionality in here is almost the same as the above, but in here
            // we flip the return types, so if pizzaA comes before pizzaB in a normal scenario,
            // we return 1, so pizzaB comes before pizzaA
            const sortedPizzasDesc = Array.from(pizzaList);
            sortedPizzasDesc.sort((a, b) => {
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
            pizzaContainer.append(sortedPizzasDesc);

        } else {
            /* show all the pizzas again */
            pizzaContainer.empty();
            pizzaContainer.append(pizzaList);
        }
    };

    // Handles the event listener changes and fires once whenever we use the order by
    const sortPriceHandler = () => {
        if (orderChoiceEl.value === 'Ascending') {
            /* Sort price in Ascending order */

            // Turn the pizzaList to an array to sort
            const sortedPizzaPriceAsc = Array.from(pizzaList);

            sortedPizzaPriceAsc.sort((a, b) => {
                const priceA = a.dataset.price;
                const priceB = b.dataset.price;

                if (parseFloat(priceA) < parseFloat(priceB)) {
                    return 1;
                }
                if (parseFloat(priceA) > parseFloat(priceB)) {
                    return -1;
                }
                return 0;
            });

            pizzaContainer.empty();
            pizzaContainer.append(sortedPizzaPriceAsc);

        } else if (orderChoiceEl.value === 'Descending') {
            /* Sort price in Descending order */

            // Turn the pizzaList to an array to sort
            const sortedPizzaPriceDesc = Array.from(pizzaList);

            sortedPizzaPriceDesc.sort((a, b) => {
                const priceA = a.dataset.price;
                const priceB = b.dataset.price;

                if (parseFloat(priceA) < parseFloat(priceB)) {
                    return -1;
                }
                if (parseFloat(priceA) > parseFloat(priceB)) {
                    return 1;
                }
                return 0;
            });

            pizzaContainer.empty();
            pizzaContainer.append(sortedPizzaPriceDesc);

        } else {
            /* show all the pizzas again */
            pizzaContainer.empty();
            pizzaContainer.append(pizzaList);
        }
    }

});
