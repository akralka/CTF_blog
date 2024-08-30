function navigateTo(url) {
    window.location.href = url;
}

function searchResults(event) {
    event.preventDefault();

    const query = document.getElementById('search-input').value.trim();
    const resultsContainer = document.getElementById('search-res-sqli');

    if (query.length > 0) {
        fetch(`/search_suggestions?query=${encodeURIComponent(query)}`)
            .then(response => {
                return response.json();
            })
            .then(data => {
                resultsContainer.innerHTML = '';
                if (data.message) {
                    resultsContainer.innerHTML = `<p>${data.message}</p>`;
                } else if (Array.isArray(data) && data.length > 0) {
                    resultsContainer.innerHTML = '<h2><strong>Search results:</strong></h2>';
                    data.forEach(suggestion => {
                        const resultItem = document.createElement('div');
                        resultItem.className = 'result-item';
                        resultItem.innerHTML = `
                            <strong>Title:</strong> ${suggestion.title} 
                            <strong>URL:</strong> <a href="${suggestion.url}">${suggestion.url}</a>
                        `;
                        resultsContainer.appendChild(resultItem);
                    });
                } else {
                    resultsContainer.innerHTML = '<p>There is no such article!</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching search suggestions:', error);
                resultsContainer.innerHTML = '<p>There was an error fetching suggestions.</p>';
            });
    } else {
        resultsContainer.style.display = 'none';
    }
}