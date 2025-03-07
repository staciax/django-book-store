let currentInputQuantity = 1;
const form = document.getElementById('form');
const inputQuantity = document.getElementById('input-quantity');
const subtrctInputQuantity = document.getElementById('subtrct-input-quantity');
const increaseInputQuantity = document.getElementById(
    'increase-input-quantity',
);

const productQuantity = Number(
    document.getElementById('product-quantity').value,
);

function updateCartQuantity(value) {
    inputQuantity.innerHTML = value;
}

// eslint-disable-next-line
subtrctInputQuantity.addEventListener('click', (event) => {
    if (currentInputQuantity <= 1) {
        return;
    }
    updateCartQuantity(--currentInputQuantity);
});

// eslint-disable-next-line
increaseInputQuantity.addEventListener('click', (event) => {
    if (currentInputQuantity >= 10) {
        return;
    }
    if (currentInputQuantity >= productQuantity) {
        return;
    }
    // if (currentQuantity >= productQuantity) {
    //   currentQuantity = productQuantity - 1;
    // }
    updateCartQuantity(++currentInputQuantity);
});

form.addEventListener('submit', (event) => {
    const product = event.target.product;
    form.action = `/cart-add-product/${product.id}/${currentInputQuantity}/`;
});
