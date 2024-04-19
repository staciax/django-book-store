const cartAddForms = document.getElementsByName('cart-add-form');
for (const addForm of cartAddForms) {
  addForm.addEventListener('submit', function (event) {
    if (event.target.id >= 10) {
      event.preventDefault();
      alert('คุณสามารถสั่งซื้อสินค้าได้ไม่เกิน 10 ชิ้นต่อครั้ง');
    }
  });
}
//
const cartSubForms = document.getElementsByName('cart-sub-form');
for (const subForm of cartSubForms) {
  subForm.addEventListener('submit', function (event) {
    if (event.target.id <= 1) {
      event.preventDefault();
      alert('คุณต้องสั่งซื้อสินค้าอย่างน้อย 1 ชิ้น');
    }
  });
}
//
const deleteCartForms = document.getElementsByName('delete-cart-form');
for (const delForm of deleteCartForms) {
  delForm.addEventListener('submit', function (event) {
    const isDelete = confirm('คุณต้องการลบสินค้าใช่หรือไม่');
    if (!isDelete) {
      event.preventDefault();
    }
  });
}
