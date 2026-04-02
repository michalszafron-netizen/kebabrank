import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import DatabaseService

def generate_report():
    load_dotenv()
    
    db_service = DatabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
    
    print("\n" + "="*60)
    print("📊 KEBAB RANK - RANKING UPDATE REPORT")
    print("="*60)
    
    # 1. Get last two batches (cycles)
    cycles = db_service.get_last_two_batches()
    if len(cycles) < 2:
        print("❌ Not enough update history to generate a report.")
        print(f"Cycles found: {len(cycles)}")
        return
    
    current_cycle = cycles[0]
    previous_cycle = cycles[1]
    
    # Display date range for cycles
    def get_cycle_label(cycle_list):
        if not cycle_list: return "Empty"
        labels = [ts.split('T')[0] for ts in cycle_list]
        unique_labels = sorted(list(set(labels)))
        if len(unique_labels) == 1:
            return unique_labels[0]
        return f"{unique_labels[0]} to {unique_labels[-1]}"

    current_label = get_cycle_label(current_cycle)
    previous_label = get_cycle_label(previous_cycle)
    
    print(f"Comparing current cycle:  {current_label} ({len(current_cycle)} updates)")
    print(f"Against previous cycle: {previous_label} ({len(previous_cycle)} updates)")
    
    # 2. Fetch rankings for both cycles
    current_rankings = db_service.get_rankings_by_batch(current_cycle)
    previous_rankings = db_service.get_rankings_by_batch(previous_cycle)
    
    print(f"Current places: {len(current_rankings)}")
    print(f"Previous places: {len(previous_rankings)}")
    
    # 3. Process changes
    prev_map = {r['google_place_id']: r for r in previous_rankings}
    
    gainers = []
    losers = []
    new_entries = []
    winner_changes = []
    
    # Track top 1 in each city
    prev_top1 = {}
    for r in previous_rankings:
        if r['city_rank'] == 1:
            prev_top1[r['city']] = r['name']
            
    curr_top1 = {}
    for r in current_rankings:
        if r['city_rank'] == 1:
            curr_top1[r['city']] = r['name']
            
    for city, name in curr_top1.items():
        if city in prev_top1 and prev_top1[city] != name:
            winner_changes.append({
                'city': city,
                'old': prev_top1[city],
                'new': name
            })

    for curr in current_rankings:
        pid = curr['google_place_id']
        if pid in prev_map:
            prev = prev_map[pid]
            change = prev['city_rank'] - curr['city_rank']
            
            if change > 0:
                gainers.append({'name': curr['name'], 'city': curr['city'], 'change': change, 'rank': curr['city_rank']})
            elif change < 0:
                losers.append({'name': curr['name'], 'city': curr['city'], 'change': change, 'rank': curr['city_rank']})
        else:
            if curr['city_rank'] <= 10:
                new_entries.append({'name': curr['name'], 'city': curr['city'], 'rank': curr['city_rank']})
                
    # Sort gainers and losers
    gainers = sorted(gainers, key=lambda x: x['change'], reverse=True)
    losers = sorted(losers, key=lambda x: x['change'])
    
    # 4. Generate Markdown
    report_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_filename = f"reports/ranking_report_{report_date}.md"
    
    os.makedirs('reports', exist_ok=True)
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🥙 Kebab Rank - Update Report ({datetime.now().strftime('%Y-%m-%d')})\n\n")
        f.write(f"**Batch Comparison**: `{current_batch}` vs `{previous_batch}`\n\n")
        
        f.write("## 🏆 New #1 Champions\n")
        if winner_changes:
            for wc in winner_changes:
                f.write(f"- **{wc['city']}**: ✨ {wc['new']} (Previously: {wc['old']})\n")
        else:
            f.write("No changes in #1 spots across cities.\n")
        f.write("\n")
        
        f.write("## 🆕 New Top 10 Entries\n")
        if new_entries:
            for item in new_entries:
                f.write(f"- **{item['name']}** ({item['city']}) - Entered at **#{item['rank']}**\n")
        else:
            f.write("No new entries in Top 10 lists.\n")
        f.write("\n")
        
        f.write("## 🚀 Biggest Gainers\n")
        if gainers:
            for item in gainers[:10]:
                f.write(f"- **{item['name']}** ({item['city']}): +{item['change']} spots (Now #{item['rank']})\n")
        else:
            f.write("No gainers tracked.\n")
        f.write("\n")
        
        f.write("## 🔻 Biggest Losers\n")
        if losers:
            for item in losers[:10]:
                f.write(f"- **{item['name']}** ({item['city']}): {item['change']} spots (Now #{item['rank']})\n")
        else:
            f.write("No significant drops.\n")
            
    print(f"\n✅ Report generated: {report_filename}")
    return report_filename

if __name__ == "__main__":
    generate_report()
