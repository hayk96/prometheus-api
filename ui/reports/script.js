document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("exportModal");
    const btn = document.getElementById("openModalBtn");
    const span = document.getElementsByClassName("close")[0];

    
    modal.style.display = "none";

    btn.onclick = function() {
        modal.style.display = "flex"; 
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    document.getElementById('exportForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const expr = document.getElementById('expr').value;
        const start = document.getElementById('start').value ? new Date(document.getElementById('start').value).toISOString() : null;
        const end = document.getElementById('end').value ? new Date(document.getElementById('end').value).toISOString() : null;
        const step = document.getElementById('step').value;
        const timestamp_format = document.getElementById('timestamp_format').value;
        const format = document.getElementById('format').value;

        const replaceFields = {};
        document.querySelectorAll('.replace-field').forEach(field => {
            const key = field.querySelector('.replace-key').value;
            const value = field.querySelector('.replace-value').value;
            if (key && value) {
                replaceFields[key] = value;
            }
        });

        const data = {
            expr: expr,
            start: start,
            end: end,
            step: step,
            timestamp_format: timestamp_format,
            replace_fields: replaceFields
        };

        try {
            const response = await fetch('/api/v1/export?format=' + format, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `data.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            document.getElementById('results').innerHTML = `<p style="color: red;">${error.message}</p>`;
        }
    });

    document.getElementById('addReplaceField').addEventListener('click', function() {
        const container = document.getElementById('replaceFieldsContainer');
        const newField = document.createElement('div');
        newField.className = 'replace-field';
        newField.innerHTML = `
            <input type="text" class="replace-key" placeholder="Source field">
            <input type="text" class="replace-value" placeholder="Target field">
            <button type="button" class="remove-field">‒</button>
        `;
        container.appendChild(newField);
    });

    document.getElementById('replaceFieldsContainer').addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-field')) {
            event.target.parentElement.remove();
        }
    });
});
