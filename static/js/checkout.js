
// Waits for the DOM to be loaded, helps with accessing DOM elements.
document.addEventListener('DOMContentLoaded', function() {
    // Get the user from the HTMl file
    const user = document.getElementById("user")

    // Hide checkout and review steps
    $("#2sts").hide();
    $("#3sts").hide();
    $("#4sts").hide();

    // Add functionality to back buttons
    const backButton2 = document.getElementById("GoBack2")
    const backButton3 = document.getElementById("GoBack3")

    backButton2.addEventListener("click", () => {
    $("#2sts").hide();
    $("#1sts").show();
    })

    backButton3.addEventListener("click", () => {
    $("#3sts").hide();
    $("#2sts").show();
    })

    // AutoFill if user has saved information
    const autofill = () => {
        const nationality = document.getElementById("country")
        if (user.dataset.country) {
            nationality.getElementsByTagName("option")[user.dataset.country].selected = "selected"
        }

        const streetname = document.getElementById("streetName")
        if (user.dataset.street) {
            streetname.value = user.dataset.street
        }

        const houseNumber = document.getElementById("houseNumber")
        if (user.dataset.house_number) {
            houseNumber.value = user.dataset.house_number
        }

        const city = document.getElementById("city")
        if (user.dataset.city) {
            city.value = user.dataset.city
        }

        const ZIPCode = document.getElementById("ZIPCode")
        if (user.dataset.zip) {
            ZIPCode.value = user.dataset.zip
        }
    }


    // Get the buttons
    const proceedToCheckout = document.getElementById("proceedToCheckout");
    const reviewPageButton = document.getElementById("toReviewPage");
    const finishOrder = document.getElementById("finishOrder");
    //const homeScreenButton = document.getElementById("homeScreenButton");

    proceedToCheckout.addEventListener("click", () => {
        valid = validatePersonalForm()
        if (valid) {
            $("#1sts").hide();
            $("#2sts").show();
        }

    });

    // Add an event listener to the button that takes the user to the review page
    reviewPageButton.addEventListener("click", () => {
        valid = validateCardForm()
        if (valid) {
            $("#2sts").hide();
            $("#3sts").show();

            // Update the display elements with the value
            // Personal information
            const fullnameInput = document.getElementById("fullname");
            const fullname = document.getElementById("displayName");
            fullname.innerText = fullnameInput.value;

            const countryInput = document.getElementById("country");
            const country = document.getElementById("displayCountry");
            country.innerText = countryInput.value;

            const streetnameInput = document.getElementById("streetName");
            const streetname = document.getElementById("displayStreet");
            streetname.innerText = streetnameInput.value;

            const ZIPCodeInput = document.getElementById("ZIPCode");
            const ZIPCode = document.getElementById("displayZIP");
            ZIPCode.innerText = ZIPCodeInput.value;

            const houseNumberInput = document.getElementById("houseNumber");
            const houseNumber = document.getElementById("displayHouse");
            houseNumber.innerText = houseNumberInput.value;

            const cityInput = document.getElementById("city");
            const city = document.getElementById("displayCity");
            city.innerText = cityInput.value;

            // Card information
            const nameInput = document.getElementById("name");
            const name = document.getElementById("displayCardName");
            name.innerText = nameInput.value;

            const numberInput = document.getElementById("number");
            const number = document.getElementById("displayCardNumber");
            number.innerText = numberInput.value.substring(0, 4) + " **** **** ****";

            const expdateInput = document.getElementById("expdate");
            const expiration = document.getElementById("displayExpiration");
            expiration.textContent = expdateInput.value;

            const CVCInput = document.getElementById("CVC");
            const CVC = document.getElementById("displayCVC");
            CVC.innerText = CVCInput.value[0] + "**";
        }
    });

    finishOrder.addEventListener("click", () => {
        $("#3sts").hide();
        $("#4sts").show();
    });

    //homeScreenButton.addEventListener("click", )


     /* ************************* Validate all Forms ******************** */
    function validatePersonalForm() {
        let x = document.forms["form-personal"]["fullname"].value;
        if (x == "") {
            alert("Name must be filled in");
            return false;
        } if (x.length > 254) {
            alert("Name is too long");
            return false;
        }

        x = document.forms["form-personal"]["streetName"].value;
        if (x == "") {
            alert("Street name must be filled in");
            return false;
        } if (x.length > 254) {
            alert("Street name is too long");
            return false;
        }

         x = document.forms["form-personal"]["houseNumber"].value;
        if (x.length > 254) {
            alert("House number is too long");
            return false;
        }

        x = document.forms["form-personal"]["city"].value;
        if (x == "") {
            alert("City must be filled in");
            return false;
        } if (x.length > 254) {
            alert("City name is too long");
            return false;
        }

        x = document.forms["form-personal"]["ZIPCode"].value;
        if (x == "") {
            alert("ZIP/postal code must be filled in");
            return false;
        } if (x.length != 3) {
            alert("ZIP/postal code not valid");
            return false;
        } if (isNaN(x)) {
            alert("ZIP must be a number")
            return false
        }

        return true
    }

    function validateCardForm() {
        let x = document.forms["form-card"]["number"].value;
        if (x == "") {
            alert("Card number must be filled in")
            return false
        } if (isNaN(x)) {
            alert("Card number must be all numbers")
            return false
        } if (x.length != 16) {
            alert("Card number must be 16 integers")
            return false
        }

        x = document.forms["form-card"]["name"].value;
        if (x == "") {
            alert("Name must be filled in")
            return false
        } if (x.length > 254) {
            alert("Name is too long")
            return false
        }

        x = document.forms["form-card"]["expdate"].value;
        if (x == "") {
            alert("Expiration date must be filled in (mm/yy)")
            return false
        } if (x.length != 5) {
            alert("Date not valid, example: '07/26'")
            return false
        } if (x.substring(2,3) != "/") {
            console.log(x.substring(2,3))
            alert("Please use a slash between the month and year, example: '07/26'")
            return false
        } if (isNaN(x.substring(0,2)) || isNaN(x.substring(3)) || x.substring(3) < 23 || x.substring(0,2) > 12 || x.substring(0,2) < 1)  {
            alert("Please use a valid month/year depicted as a number, example: '07/26'")
            return false
        }

        x = document.forms["form-card"]["CVC"].value;
        if (x == "") {
            alert("CVC must be filled in")
            return false
        } if (x.length != 3) {
            alert("CVC number must be 3 integers")
            return false
        } if (isNaN(x)) {
            alert("CVC must be all numbers")
            return false
        }

        return true
    }
        // 1234567890123456

    /* ************************* Cart functionality*********************** */
    const viewCart = () => {
        // get the CSRF token, cross-site request forgery
        // Security measure
        const csrftoken = getCookie('csrftoken');

        const apiUrl = `/cart/`;

        // make the AJAX request to get the cart
        return $.ajax({
            type: 'GET',
            url: apiUrl,
            data: {
                csrfmiddlewaretoken: csrftoken,
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
        });
    }

    const getCart = async () => {
        try {
            const cartData = await viewCart();
            generateCartHTML(cartData);
        } catch (err) {
            console.log(err);
        }
    }

    const generateCartHTML = async (response) => {
    let cartHtml = '';
    // for(const item of response.cart)
    for(const item of response.cart) {
        cartHtml += `<div class="cart" data-creation="${item.created_at}" data-sum="${item.cart_sum}">`;

        cartHtml += `<p id="cartAmount">Amount: ${item.cart_sum}$</p>`;

        if(item.pizza.length > 0) {
            // Generate the Pizzas for the cart
            const pizzaHtml = htmlPizzasCart(item);
            cartHtml += pizzaHtml;
        }

        if (item.offer.length > 0) {
            // Generate the Offers for the cart
            const offerHtml = await htmlOffersCart(item);
            cartHtml += offerHtml;
        }

        cartHtml += '</div>';
        $('#grandTotal').html(`$${item.cart_sum}$`)
    }

    // display the cart HTML
    $('#placeHolderForCart').html(cartHtml);

    }

    const htmlOffersCart = async (item) => {
        let offerHtml = '';
        for(const offer of item.offer) {
                offerHtml += `<div class="offerCart" data-id="${offer.offer_id}">`;
                    offerHtml += `<p>Offer: ${offer.offer_name} x${offer.quantity}</p>`;
                    let totalValue = parseFloat(offer.offer_price);

                    // Raises the price if there are more than one of the same item in the two for one.
                    if (offer.quantity > 1) {
                        const quant = offer.quantity;
                        totalValue = quant * totalValue;
                    }
                    offerHtml += `<p>Price: ${totalValue}$</p>`;
                    offerHtml += `<p>Pizzas selected: </p>`;
                    const pizzaList = await getPizzaOffer(offer);
                    // Pizzas belonging to each offer come in here
                    offerHtml += `<ul>`;

                        pizzaList.forEach(pizza => {
                           offerHtml += `<li>${pizza.pizza__name}</li>`;
                        });

                    offerHtml += `</ul>`;
                offerHtml += `</div>`;
        }
        return offerHtml;
    }

    const getPizzaOffer = async (offer) => {
    try {
        const pizzaList = await getPizzasInOffer(offer);

        cachedPizzaData = await Promise.all(pizzaList.pizzas);
        return cachedPizzaData;
    } catch (err) {
        console.log(err);
    }
    }

    const getPizzasInOffer = (offer) => {
        // get the CSRF token, cross-site request forgery
        // Security measure
        const csrftoken = getCookie('csrftoken');

        //
        const apiUrl = `/cart/offers/${offer.offer_id}/`;

        // make the AJAX request to delete the cart item
        // Return the ajax response
        return $.ajax({
            type: 'GET',
            url: apiUrl,
            data: {
                csrfmiddlewaretoken: csrftoken,
                offer_id: offer.offer_id,
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
        });
    }

    const htmlPizzasCart = (item) => {
        let pizzaHtml = '';
        item.pizza.forEach(pizza => {
            pizzaHtml += `<div class="pizzaCart" data-name="${pizza.name}" data-price="${pizza.price}" data-id="${pizza.id}">`;
            pizzaHtml += `<p>Pizza: ${pizza.name}</p>`;
            pizzaHtml += `<p>Price: ${pizza.price}$</p>`;
            pizzaHtml += `<p>Quantity: ${pizza.quantity}</p>`;
            pizzaHtml += `</div>`;
        });
        return pizzaHtml;
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

    getCart()
    autofill()
})
