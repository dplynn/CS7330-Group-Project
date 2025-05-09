function addField() {
    const container = document.getElementById('fields-container');
    const fieldGroup = document.createElement('div');
    fieldGroup.className = 'field-group';
    
    fieldGroup.innerHTML = `
        <label><p></p></label>
        <input type="text" name="field_name[]" placeholder="Field Name" required>
        <button type="button" onclick="removeField(this)">Remove</button>
    `;
    container.appendChild(fieldGroup);
    renumberFields();
}

function renumberFields() {
    const labels = document.querySelectorAll('#fields-container .field-group label');
    labels.forEach((label, index) => {
        label.textContent = `Field Name ${index + 1}:`;
    });
}

function removeField(button) {
    button.parentElement.remove();
    renumberFields();
}

window.onload = function() {
    addField();
};