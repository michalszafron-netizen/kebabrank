
// Corrected checkAndLoadRankings to include map update
async function checkAndLoadRankings(cityName, limit = 10) {
    console.log(`Loading rankings for ${cityName} with limit: ${limit}`);
    const container = $id('city-rankings');
    container.innerHTML = `<div class="loading">${translations[currentLang]['loading']}</div>`;

    try {
        // First get regular rankings with rank_change data
        const baseUrl = `/api/rankings/${encodeURIComponent(cityName)}?limit=${limit}`;
        console.log(`Making base API call to: ${baseUrl}`);
        const baseResponse = await fetch(baseUrl);
        const baseData = await baseResponse.json();

        if (baseData.status !== 'success') {
            throw new Error('Failed to load base rankings');
        }

        // Then get AI insights
        const aiUrl = `/api/rankings/${encodeURIComponent(cityName)}/ai?lang=${currentLang}&limit=${limit}`;
        console.log(`Making AI API call to: ${aiUrl}`);
        const aiResponse = await fetch(aiUrl);
        const aiData = await aiResponse.json();

        if (aiData.status !== 'success') {
            throw new Error('Failed to load AI data');
        }

        // Merge the data - preserve rank_change from baseData
        const mergedData = baseData.data.map(baseKebab => {
            const aiKebab = aiData.data.find(k => k.google_place_id === baseKebab.google_place_id);
            return {
                ...baseKebab,  // Keep all base data including rank_change
                ...aiKebab     // Overlay AI data
            };
        });

        // Update last refresh time in localStorage
        try {
            localStorage.setItem('lastUpdate', new Date().toISOString());
            localStorage.setItem('updateInterval', '6');
            console.log('Updated manual refresh time in localStorage');
        } catch (err) {
            console.error('Error updating localStorage:', err);
        }

        // UPDATE MAP
        console.log('Updating map with', mergedData.length, 'places');
        if (typeof updateMapWithKebabs === 'function') {
            updateMapWithKebabs(mergedData);
        } else {
            console.error('updateMapWithKebabs function not found');
        }

        // Display Rankings using the new function
        displayRankings(mergedData, container, cityName);
    } catch (error) {
        console.error('Error loading rankings:', error);
        container.innerHTML = `<p class="info-message">${translations[currentLang]['error-loading']}</p>`;
    }
}

// Alias displayAIRankings to consistency
function displayAIRankings(rankings, container, cityName, limit) {
    displayRankings(rankings, container, cityName);
}
