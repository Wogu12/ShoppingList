document.getElementById('item-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/add_item', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const table = document.getElementById('items-table');
            const row = document.createElement('tr');
            row.innerHTML = `<td class="item">${data.item.ItemName}</td><td class="quan">${data.item.Quantity}</td><td class="bought">
                                <label>
                                    <input type="checkbox" class="filled-in" onchange="updateBought(${data.item.ItemID}, this.checked)">
                                    <span></span>
                                </label>
                            </td><td class="del"><button class="btn-small red" onclick="deleteItem(${data.item.ItemID})">usun</button></td>`;
            table.appendChild(row);
        }
    })
    .catch(error => console.error('Error:', error));
});

function updateBought(itemId, bought) {
    fetch(`/update_bought/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bought: bought })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Error updating bought status');
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteItem(itemId) {
    fetch(`/delete_item/${itemId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`button[onclick="deleteItem(${itemId})"]`).closest('tr').remove();
        }
    })
    .catch(error => console.error('Error:', error));
}