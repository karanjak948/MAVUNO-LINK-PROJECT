document.addEventListener("DOMContentLoaded", function () {
    console.log("Product JS loaded");

    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach(card => {
        card.addEventListener("click", () => {
            alert(`You clicked on ${card.dataset.name}`);
        });
    });
});
