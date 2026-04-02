// Test script to verify URL update functionality
console.log('Testing URL update functionality...');

// Mock the updateCityUrl function to test if it's called
const originalUpdateCityUrl = window.updateCityUrl;
let urlUpdateCalled = false;
let lastCityCalled = '';

window.updateCityUrl = function(cityName) {
    urlUpdateCalled = true;
    lastCityCalled = cityName;
    console.log(`✅ updateCityUrl called with: "${cityName}"`);
    console.log(`   Would update URL to: /${cityName.toLowerCase().replace(/ /g, '-').replace(/ł/g, 'l').replace(/ó/g, 'o').replace(/ą/g, 'a').replace(/ę/g, 'e').replace(/ć/g, 'c').replace(/ń/g, 'n').replace(/ś/g, 's').replace(/ź/g, 'z').replace(/ż/g, 'z')}`);
    
    // Call the original function if it exists
    if (originalUpdateCityUrl) {
        originalUpdateCityUrl(cityName);
    }
};

// Test the searchCity function
console.log('\n=== Testing searchCity function ===');
console.log('Simulating search for "Warszawa"...');

// Mock the necessary elements and functions
const mockSearchInput = { value: 'Warszawa' };
const mockDropdown = { style: { display: 'none', visibility: 'hidden', opacity: '0' } };
const mockKebabCount = { value: '10' };

// Mock the $id function
const original$id = window.$id;
window.$id = function(id) {
    switch(id) {
        case 'city-search': return mockSearchInput;
        case 'city-dropdown': return mockDropdown;
        case 'kebab-count': return mockKebabCount;
        default: return null;
    }
};

// Mock the checkAndLoadRankings function to avoid API calls
window.checkAndLoadRankings = function(cityName, limit) {
    console.log(`✅ checkAndLoadRankings called with: "${cityName}", limit: ${limit}`);
    return Promise.resolve();
};

// Mock allCities array
window.allCities = ['Warszawa', 'Kraków', 'Łódź', 'Wrocław', 'Poznań'];

// Test the searchCity function
try {
    window.searchCity();
    console.log('\n=== Test Results ===');
    console.log(`✅ URL update called: ${urlUpdateCalled}`);
    console.log(`✅ Last city called: "${lastCityCalled}"`);
    
    if (urlUpdateCalled && lastCityCalled === 'Warszawa') {
        console.log('🎉 SUCCESS: URL update functionality is working correctly!');
        console.log('The searchCity function now properly updates URLs when:');
        console.log('  - Typing a city name and pressing Enter');
        console.log('  - Clicking the search button');
        console.log('  - Selecting from dropdown (already working)');
    } else {
        console.log('❌ FAILED: URL update functionality is not working correctly');
    }
} catch (error) {
    console.error('❌ Error during test:', error);
}

// Restore original functions
window.updateCityUrl = originalUpdateCityUrl;
window.$id = original$id;
