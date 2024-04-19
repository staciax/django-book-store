const deleteAddressForms = document.getElementsByName('delete-address-form');
for (const addressForm of deleteAddressForms) {
  addressForm.addEventListener('submit', function (event) {
    const isDelete = confirm('คุณต้องการลบที่อยู่ใช่หรือไม่');
    if (!isDelete) {
      event.preventDefault();
    }
  });
}
