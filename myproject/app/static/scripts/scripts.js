document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('itemForm');
    const itemsTable = document.getElementById('itemsTable');
    let items = [];

    function fetchItems() {
        console.log("Fetching items from API...");
        $.ajax({
            url: '/api/items/',
            method: 'GET',
            success: function (data) {
                console.log("Data fetched:", data);  // Print items to the console
                itemsTable.innerHTML = '';
                if (data && Array.isArray(data)) {
                    items = data;
                    items.forEach(item => addItemToTable(item));
                } else {
                    console.error("Invalid data format received from API:", data);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error fetching items:", status, error);
            }
        });
    }

    function addItemToTable(item) {
        const row = document.createElement('tr');
        row.setAttribute('id', `item-${item.id}`);
        console.log("name :", item.id)
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.description}</td>
            <td><img src="${item.image}" alt="${item.name}" width="50"></td>
            <td>
                <button class="btn btn-warning btn-custom" onclick="editItem(${item.id})">Edit</button>
                <button class="btn btn-danger btn-custom" onclick="deleteItem(${item.id})">Delete</button>
            </td>
        `;

        itemsTable.appendChild(row);
    }

    function editItem(id) {
        const item = items.find(itm => itm.id === id);
        if (item) {
            document.getElementById('name').value = item.name;
            document.getElementById('description').value = item.description;
            form.dataset.id = id;
        }
    }

    function deleteItem(id) {
        $.ajax({
            url: `/api/items/${id}/`,
            method: 'DELETE',
            success: function () {
                document.getElementById(`item-${id}`).remove();
                items = items.filter(item => item.id !== id);
            }
        });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const id = form.dataset.id ? parseInt(form.dataset.id) : null;
        const name = document.getElementById('name').value;
        const description = document.getElementById('description').value;
        const image = document.getElementById('image').files[0];

        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        if (image) {
            formData.append('image', image);
        }

        const url = id ? `/api/items/${id}/` : '/api/items/';
        const method = id ? 'PUT' : 'POST';

        $.ajax({
            url: url,
            method: method,
            data: formData,
            processData: false,
            contentType: false,
            success: function (item) {
                if (id) {
                    document.getElementById(`item-${id}`).remove();
                }
                addItemToTable(item);
                form.reset();
                form.dataset.id = '';
            }
        });
    });

    fetchItems();
});
