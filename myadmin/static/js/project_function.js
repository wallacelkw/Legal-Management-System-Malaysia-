function autocompleteState(postcode) {
    console.log("MY Code")
    fetch('{% static "postcode1.csv" %}')
        .then(response => response.text())
        .then(csvData => {
            const lines = csvData.split('\n');
            for (const line of lines) {
                const [csvPostcode, state] = line.split(',');
                if (csvPostcode === postcode) {
                    document.getElementById('customerState').value = state;
                    return;
                }
            }
            document.getElementById('customerState').value = '';
        })
        .catch(error => {
            console.error('Error fetching CSV data:', error);
        });
}