// Test script to verify frontend loading behavior
// Run this in browser console to test URL routing

function testFrontendLoading() {
    console.log('🧪 Testing Frontend URL Routing and Loading');
    console.log('===========================================');
    
    // Test 1: Check if handleUrlRouting is called
    console.log('✅ Test 1: handleUrlRouting function exists:', typeof handleUrlRouting === 'function');
    
    // Test 2: Check if initialCity is set
    console.log('✅ Test 2: initialCity variable:', window.initialCity);
    
    // Test 3: Check if search input has correct value
    const searchInput = document.getElementById('city-search');
    console.log('✅ Test 3: Search input value:', searchInput ? searchInput.value : 'NOT FOUND');
    
    // Test 4: Check if rankings container has content
    const rankingsContainer = document.getElementById('city-rankings');
    const hasRankings = rankingsContainer && rankingsContainer.innerHTML !== '';
    console.log('✅ Test 4: Rankings container has content:', hasRankings);
    
    // Test 5: Check if map is initialized
    console.log('✅ Test 5: City map initialized:', typeof kebabMap !== 'undefined' && kebabMap !== null);
    console.log('✅ Test 6: Global map initialized:', typeof globalKebabMap !== 'undefined' && globalKebabMap !== null);
    
    // Test 6: Check if cities are loaded
    console.log('✅ Test 7: Cities loaded:', allCities && allCities.length > 0 ? `${allCities.length} cities` : 'NOT LOADED');
    
    // Test 7: Check current URL path
    console.log('✅ Test 8: Current path:', window.location.pathname);
    
    // Test 8: Manually trigger URL routing to see what happens
    console.log('🔄 Manually triggering handleUrlRouting...');
    handleUrlRouting();
    
    console.log('===========================================');
    console.log('🧪 Test Complete - Check console for results');
}

// Run the test
testFrontendLoading();
