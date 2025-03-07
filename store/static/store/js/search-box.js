const searchForm = document.getElementById('search-form');
searchForm.addEventListener('submit', function (event) {
    const searchInput = document.getElementById('search-input');
    if (searchInput.value.trim() == '') {
        event.preventDefault();
    }
});
