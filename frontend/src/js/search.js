document.addEventListener("DOMContentLoaded", function() {
    let debounceTimer;
    const cache = {};

    async function fetchSuggestions() {
        const query = document.getElementById("searchInput").value.trim().toLowerCase();
        const suggestionsList = document.getElementById("searchSuggestionsList");

        // Hide suggestions if input is less than 2 characters.
        if (query.length < 2) {
            suggestionsList.style.display = "none";
            return;
        }

        // Check if the result is already cached.
        if (cache[query]) {
            renderSearchSuggestions(cache[query]);
            return;
        }

        // Debounce request to avoid sending too many requests.
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(async () => {
            const response = await fetch("https://jsonplaceholder.typicode.com/users");
            const users = await response.json();

            const suggestions = {
                users: users.filter(user => user.name.toLowerCase().includes(query)).map(user => user.name),
                groups: ["Group A", "Group B", "Group C"].filter(group => group.toLowerCase().includes(query)),
                services: ["Service 1", "Service 2", "Service 3"].filter(service => service.toLowerCase().includes(query))
            };

            // Cache the result for future queries.
            cache[query] = suggestions;
            renderSuggestionsList(suggestions);
        }, 100);
    }

    function renderSuggestionsList(suggestions) {
        const suggestionsList = document.getElementById("searchSuggestionsList");
        suggestionsList.innerHTML = "";
        suggestionsList.style.display = suggestions.users.length ? "block" : "none";
        
        if (suggestions.users.length) {
            const userHeading = document.createElement("li");
            userHeading.className = "list-group-item list-group-item-info";
            userHeading.textContent = "Users";
            suggestionsList.appendChild(userHeading);

            suggestions.users.forEach(item => {
                const listItem = document.createElement("li");
                listItem.className = "list-group-item";
                listItem.textContent = item;
                listItem.onclick = () => {
                    document.getElementById("searchInput").value = item;
                    suggestionsList.style.display = "none";
                };
                suggestionsList.appendChild(listItem);
            });
        }
    }

    // Comment out until suggestions list design is finalised.
    //document.querySelector("#searchInput").addEventListener("input", fetchSuggestions);
});