
// Waits for the DOM to be loaded, helps with accessing DOM elements.
document.addEventListener('DOMContentLoaded', function() {
    const cartIdEl = document.getElementById('cart');
    // Select the menu container element
    const pizzaContainer = $('#menu');
    // Select all pizzas, with the class .pizza
    const pizzaList = document.querySelectorAll('.pizza');
    // Select all pizzas, with the class .pizza
    const offerList = document.querySelectorAll('.offer');

    /* ----------------------------------Display Pizza----------------------------------------- */

    // Retrieve Each pizza image from the Content body to be able to display the pizzas.
    pizzaList.forEach((pizza) => {
        // Onclick Event for each pizza, to trigger view pizza:
        // Set the 'hover' effect on the pizza
        pizza.style.cursor = 'pointer';

        pizza.onclick = () => {
            viewPizza(pizza);
        }

        const img = pizza.dataset.img;
        const id = pizza.dataset.id;
        const imgElm = pizza.querySelector(`#img-${id}`);
        imgElm.src = `/static/img/${img}`;
    });

    /* ----------------------------------Display Offer----------------------------------------- */

    // Retrieve Each offer image from the Content body to be able to display the offers.
    offerList.forEach((offer) => {
       // Onclick Event for each pizza, to trigger choose offer:
        // Set the 'hover' effect on the offer
        offer.style.cursor = 'pointer';

        offer.onclick = () => {
            chooseOffer(offer);
        }

        const img = offer.dataset.img;
        const id = offer.dataset.id;
        const offerImgEl = offer.querySelector(`#offerimg-${id}`);
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
        // Clear the select options
        clearOrder();
        clearType();

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
        // Reset the order select element
        clearOrder();
        clearSearch();

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
        // Clear the Selected 'Select Type' and the Search value
        clearType();
        clearSearch();

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
    /* ----------------------------------Clear Select options----------------------------------------- */
    const clearType = () => {
        const pizzaTypes = document.getElementById('pizzaTypes');
        pizzaTypes.value = '';
    }

    const clearOrder = () => {
        orderEl.value = '';
        if($(ascOrDescEl).is(":visible")) {
            $(ascOrDescEl).hide("slow");
        }
    }

    const clearSearch = () => {
        searchEl.value = '';
    }

    // Have these set to default at the load of the JS:
    clearOrder();
    clearType();
    clearSearch();

    /* ----------------------------------About us Functionality----------------------------------------- */

    // selecting the elements for which we want to add a tooltip
    const target = document.getElementById("pizzaAbout");
    const tooltip = document.getElementById("aboutUsText");

    // change display to 'block' on mouseover
    target.addEventListener('mouseover', () => {
      tooltip.style.display = 'block';
    }, false);

    // change display to 'none' on mouseleave
    target.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    }, false);


    /* ----------------------------------View Specific Pizza----------------------------------------- */
    const viewPizza = (pizza) => {
        // Start by emptying the contentBody
        pizzaContainer.empty();
        // And hide the filter
        $("#filter").hide();

        /** Generating the view template **/
        const pizzaName = pizza.dataset.name;
        const pizzaDesc = pizza.dataset.description;
        const pizzaImg = pizza.dataset.img;
        const pizzaPrice = pizza.dataset.price;
        const pizzaId = pizza.dataset.id;

        // Take the topping dataset and split it into an array
        const pizzaToppings = pizza.dataset.topping.split(',');

        let toppingsHTML = '';
        pizzaToppings.forEach((topping) => {
           toppingsHTML += `<li>${topping}</li>`;
        });

        pizzaContainer.html(`
            <div id="viewPizza">
                <!-- Back option, replace '<-' with image maybe? DONE -->
                <button id="returnMenu">
                    <img class="backarrow" src="/static/img/backIcon.png" alt="'Back arrow'  "
                    <p>Back</p>
                </button>
                <!-- The name of the selected pizza -->
                <p class="viewPizzaText">${pizzaName}</p>
                <!-- Image of the pizza -->
                <img class="viewPizzaImg" src="/static/img/${pizzaImg}" alt="Pizza image">
                <!-- Price of the pizza -->
                <p class="viewPizzaText">Price: ${pizzaPrice}$</p>
                <!-- Description of the pizza -->
                <p class="viewPizzaText">Description: ${pizzaDesc}</p>
                <p class="viewPizzaText">Toppings: </p>
                <ul class="viewPizzaText">
                    ${toppingsHTML}
                </ul>
                <button id="addToCart">
                    <img class="CartIcon" src="/static/img/CartIcon.png" alt="Image of a cart">
                    <p id="cartText">Add to cart</p>
                </button>
            </div>`
        );

        // Retrieve the addToCart button element
        const addCartEl = document.getElementById('addToCart');
        addCartEl.onclick = () => {
            addToCart(pizza);
        }

        const backEl = document.getElementById('returnMenu');
        backEl.style.cursor = 'pointer';
        backEl.onclick = () => {
            populatePizzas();
        };

    }

    const populatePizzas = () => {
        $("#filter").show();

        pizzaContainer.empty();
        pizzaContainer.append(pizzaList);
    }

    /* ----------------------------------Add to cart----------------------------------------- */


    const addToCart = (pizza) => {
        //console.log(pizza);

        const user_id = 1;

        // get the CSRF token, cross-site request forgery
        // Security measure
        const csrftoken = getCookie('csrftoken');

        //
        const apiUrl = `addToCart/${pizza.dataset.id}/${user_id}/`;

        // make the AJAX request
        $.ajax({
            type: 'POST',
            url: apiUrl,
            data: {
                csrfmiddlewaretoken: csrftoken,
                pizza_id: pizza.dataset.id,
                user_id: user_id,
            },
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.log(error);
        }
        });
    }

    // This code IS NOT WRITTEN BY US, this is from the django documentation:
    // link: https://docs.djangoproject.com/en/3.2/ref/csrf/#ajax
    // All credit goes to them.
    // Used in the purpose of CSRF protection
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /* ----------------------------------Display Cart----------------------------------------- */

    const cartEl = document.getElementById('navOrder');

    // Make the div hoverable
    cartEl.style.cursor = 'pointer';
    // Onclick we display the cart
    cartEl.onclick = () => {
        if($(cartIdEl).is(":hidden")) {
            $(cartIdEl).show("slow");
        } else {
            $(cartIdEl).hide("slow");
        }

        displayCart();
    }

    const displayCart = () => {
        const cartContainer = document.querySelectorAll('.cart .pizzaCart');

        cartContainer.forEach((item) => {

        });
    }

    /* ----------------------------------Use offer----------------------------------------- */
    const chooseOffer = (offer) => {
        // Start by emptying the contentBody
        choosePizza()

        // Retrieve the addToCart button element
        // const addCartEl = document.getElementById('addToCart');
        // addCartEl.onclick = () => {
        //    addToCart(offer);
        //}

    }

        const choosePizza = () => {
        $("#offers").hide()
        $("#menu").show()
        populatePizzas()
    }

    const populateOffers = () => {
        offerContainer.empty();
        offerContainer.append(offerList);
    }

});



