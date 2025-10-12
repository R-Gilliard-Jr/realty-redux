const reportForm = document.getElementById('reportForm')

reportForm.addEventListener("submit", async(e) => {
        e.preventDefault();
        const form = e.target;
        const data = {};
        for (let element of form.elements) {
            if (!element.name) continue;
            if (element.name === 'rental_units') {
                try {
                    data[element.name] = JSON.parse(element.value);
                } catch {
                    alert('Rental Units must be valid JSON array');
                    return;
                }
            } else if (element.type === 'number' || element.type === 'range') {
                data[element.name] = element.value === '' ? null : Number(element.value);
            } else {
                data[element.name] = element.value;
            }
        }
        fetch('/report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.text())
        .then(result => {
            document.getElementById('results').innerHTML = result;
        })
        .catch(err => {
            document.getElementById('results').innerHTML = '<b>Error:</b> ' + err;
        });
    }
)