// Retrieve Each pizza image from the Content body to be able to display the pizzas.
document.addEventListener('DOMContentLoaded', function() {
    const pizzaList = document.querySelectorAll('.pizza');
    pizzaList.forEach((pizza) => {
        const img = pizza.dataset.img;
        const id = pizza.dataset.id;
        const imgElm = pizza.querySelector(`#img-${id}`);
        imgElm.src = `/static/img/${img}`;
    });
});