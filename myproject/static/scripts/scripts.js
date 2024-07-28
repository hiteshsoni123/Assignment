document.addEventListener('DOMContentLoaded', () => {
    const itemList = document.getElementById('item-list');
    const addItemForm = document.getElementById('add-item-form');

    // Fetch and display items
    fetch('/api/items/')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.innerHTML = `
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    ${item.image ? `<img src="${item.image}" alt="${item.name}" width="100">` : ''}
                `;
                itemList.appendChild(itemDiv);
            });
        });

    // Handle form submission
    addItemForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const description = document.getElementById('description').value;
        const image = document.getElementById('image').files[0];

        const reader = new FileReader();
        reader.onloadend = () => {
            const imageData = reader.result;

            fetch('/api/items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, description, image: imageData })
            })
            .then(response => response.json())
            .then(data => {
                const itemDiv = document.createElement('div');
                itemDiv.innerHTML = `
                    <h3>${data.name}</h3>
                    <p>${data.description}</p>
                    ${data.image ? `<img src="${data.image}" alt="${data.name}" width="100">` : ''}
                `;
                itemList.appendChild(itemDiv);
            });
        };

        if (image) {
            reader.readAsDataURL(image);
        } else {
            fetch('/api/items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, description })
            })
            .then(response => response.json())
            .then(data => {
                const itemDiv = document.createElement('div');
                itemDiv.innerHTML = `
                    <h3>${data.name}</h3>
                    <p>${data.description}</p>
                `;
                itemList.appendChild(itemDiv);
            });
        }
    });
});
