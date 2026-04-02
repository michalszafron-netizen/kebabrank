// This file is a backup of the critical functions in app.js after the UI Refinements (Batch 3)
// It includes the updated displayRankings with AI Score display and other core functions.

// Regular rankings display function
function displayRankings(rankings, container, cityName, isGlobal = false) {
    if (rankings.length === 0) {
        container.innerHTML = `<p class="text-center text-gray-500 py-4">${translations[currentLang]['no-kebabs']}</p>`;
        return;
    }

    // Ensure rankings are properly sorted by rank_score descending
    const sortedRankings = [...rankings].sort((a, b) => {
        if (b.rank_score !== a.rank_score) {
            return b.rank_score - a.rank_score;
        }
        // Secondary sort by rating if scores are equal
        return b.rating - a.rating;
    });

    let html = '';

    sortedRankings.forEach((kebab, index) => {
        const rank = kebab.rank || index + 1;
        const hasAI = kebab.has_ai_analysis === true || (kebab.ai_summary && kebab.ai_summary.length > 0);

        // Rank Colors/Styles
        let rankBadgeClass = "bg-surface-dark text-gray-400";
        if (rank === 1) rankBadgeClass = "bg-yellow-500 text-black";
        else if (rank === 2) rankBadgeClass = "bg-gray-400 text-black";
        else if (rank === 3) rankBadgeClass = "bg-orange-700 text-white";

        // Rank change indicator
        let rankChangeHtml = '';
        if (kebab.rank_change_indicator === 'up') rankChangeHtml = `<span class="text-green-500 text-xs ml-1">▲</span>`;
        else if (kebab.rank_change_indicator === 'down') rankChangeHtml = `<span class="text-red-500 text-xs ml-1">▼</span>`;
        else if (kebab.rank_change_indicator === 'new') rankChangeHtml = `<span class="text-blue-500 text-xs ml-1 font-bold">NEW</span>`;

        const kebabImage = kebab.image_url || "https://lh3.googleusercontent.com/aida-public/AB6AXuAPZml7HBCvOmxHc3pErimDG6i7ruSOL6NrxB8S8CkUtAIZ9sjOe5U0TSzY4AbGN8NSPkGQZHCdrnALIQoLgGNrze3MwVl9x7OGSn2Gz7CvsUTB4izX8Xatv_tIbLYX6kiuSDVdT3HoS7MKLCnQparIKmg8UVIl7QU1CTAKEBVF9M8_NiLS2ccsanJPm-7kevE10rqP_NKMyBgiXUpcsUtj4e9eJlwKM02h-oL83bYxG2QwVRiuDKWgPfePcvFNWLVGzfpHYYn_Nl4";

        html += `
            <div class="glass-card rounded-xl p-4 flex gap-4 relative overflow-hidden group cursor-pointer hover:bg-white/5 hover:border-primary/30 mb-4 transition-all duration-300"
                 onclick="${isGlobal ? `centerGlobalMapOnKebab(${index})` : `centerMapOnKebab(${index})`}"
                 data-rank="${rank}">
                 
                <!-- Rank Badge -->
                <div class="absolute top-4 left-4 ${rankBadgeClass} font-black text-xs px-2 py-0.5 rounded flex items-center gap-1 z-20 shadow-lg">
                    <span class="material-icons text-xs">emoji_events</span> #${rank}
                </div>

                <!-- Image -->
                <div class="w-24 h-24 shrink-0 rounded-lg overflow-hidden shadow-lg bg-surface-dark">
                    <img alt="${kebab.name}" class="w-full h-full object-cover transition-transform duration-500" src="${kebabImage}"/>
                </div>

                <!-- Content -->
                <div class="flex-1 flex flex-col min-w-0">
                    <div>
                        <div class="flex justify-between items-start">
                             <h3 class="text-lg font-bold text-white group-hover:text-primary transition-colors truncate pr-2">${kebab.name} ${rankChangeHtml}</h3>
                              <div class="flex flex-col items-end gap-1">
                                <div class="px-2 py-1 rounded bg-[#1e293b] border border-white/10 flex flex-col items-end">
                                    <span class="text-[10px] text-gray-400 uppercase font-bold">Score</span>
                                    <span class="text-base font-black text-primary">${kebab.rank_score ? kebab.rank_score.toFixed(1) : 'N/A'}</span>
                                </div>
                                ${kebab.ai_score ? `
                                <div class="px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20 flex flex-col items-end">
                                    <span class="text-[8px] text-blue-400 uppercase font-bold tracking-tighter">AI Score</span>
                                    <span class="text-xs font-black text-blue-400">${kebab.ai_score.toFixed(1)}</span>
                                </div>
                                ` : ''}
                             </div>
                        </div>
                        <p class="text-xs text-gray-400 mt-1 flex items-center gap-1 truncate mb-2">
                            <span class="material-icons text-xs">place</span> ${kebab.address}, ${kebab.city || window.currentCity || ''}
                        </p>
                    </div>

                    <!-- Stats Row -->
                    <div class="flex items-center gap-4 text-xs text-gray-300 mb-3 border-b border-white/5 pb-2">
                        <div class="flex items-center gap-1">
                            <span class="material-icons text-yellow-500 text-sm">star</span>
                            <span class="font-bold text-white text-sm">${kebab.rating.toFixed(1)}</span>
                            <span class="text-gray-500">Google Rating</span>
                        </div>
                         <div class="flex items-center gap-1">
                            <span class="material-icons text-blue-400 text-sm">reviews</span>
                            <span class="font-bold text-white text-sm">${kebab.total_reviews.toLocaleString()}</span>
                            <span class="text-gray-500">Reviews</span>
                        </div>
                    </div>

                    <!-- AI Sections (Collapsible) -->
                     <div class="space-y-2">
                        <!-- AI Summary -->
                         <div class="border border-white/10 rounded overflow-hidden">
                            <button onclick="event.stopPropagation(); toggleSection('ai-summary-${index}-${isGlobal ? 'g' : 'c'}')" 
                                    class="w-full flex items-center justify-between bg-white/5 px-2 py-1 hover:bg-white/10 transition-colors">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 flex items-center gap-1">
                                    <span class="material-icons text-[10px]">auto_awesome</span> AI Summary
                                </span>
                                <span class="material-icons text-gray-400 text-[10px] arrow">expand_more</span>
                            </button>
                            <div id="ai-summary-${index}-${isGlobal ? 'g' : 'c'}" class="hidden p-2 bg-[#0f172a] text-[11px] text-gray-300 leading-relaxed border-t border-white/10">
                                ${kebab.ai_summary ? `"${kebab.ai_summary}"` : '<em class="text-gray-500">AI analysis forthcoming...</em>'}
                            </div>
                        </div>

                        <!-- AI Insights -->
                         ${hasAI && kebab.ai_insights ? `
                            <div class="border border-white/10 rounded overflow-hidden">
                                <button onclick="event.stopPropagation(); toggleSection('ai-insights-${index}-${isGlobal ? 'g' : 'c}')" 
    class="w-full flex items-center justify-between bg-white/5 px-2 py-1 hover:bg-white/10 transition-colors" >
                                    <span class="text-[10px] font-bold uppercase tracking-wider text-purple-400 flex items-center gap-1">
                                        <span class="material-icons text-[10px]">analytics</span> AI Insights
                                    </span>
                                    <span class="material-icons text-gray-400 text-[10px] arrow">expand_more</span>
                                </button >
        <div id="ai-insights-${index}-${isGlobal ? 'g' : 'c'}" class="hidden p-2 bg-[#0f172a] border-t border-white/10">
            <div class="grid grid-cols-2 gap-2">
                <div class="flex flex-col">
                    <span class="text-[9px] text-gray-500 uppercase">Sentiment</span>
                    <span class="text-[10px] font-bold ${getSentimentColorClass(kebab.ai_insights.sentiment)}">
                        ${getSentimentLabel(kebab.ai_insights.sentiment)}
                    </span>
                </div>
                <div class="flex flex-col">
                    <span class="text-[9px] text-gray-500 uppercase">Trend</span>
                    <span class="text-[10px] font-bold text-white">
                        ${getTrendLabel(kebab.ai_insights.trend)}
                    </span>
                </div>
            </div>
        </div>
                            </div >
        ` : ''}
                    </div>
                </div>
            </div>
        `;
});

container.innerHTML = html;
}
