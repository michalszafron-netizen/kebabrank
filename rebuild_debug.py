import os

app_path = r'static/js/app.js'
fix_path = r'final_fix.js'

# Read Fix Content
with open(fix_path, 'r', encoding='utf-8') as f:
    fix_content = f.read()
    
fix_lines = fix_content.splitlines()
print(f"Fix line 7: {fix_lines[6]}")

# Read App Head
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
head = lines[:1782]

# Construct New Content
new_content = "".join(head)
if not new_content.endswith('\n'):
    new_content += '\n'
new_content += fix_content

# Delete existing app.js to be sure
try:
    os.remove(app_path)
    print("Deleted app.js")
except Exception as e:
    print(f"Delete failed: {e}")

# Write New Content
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print(f"Wrote app.js with {len(new_content.splitlines())} lines.")

# Verify Content
with open(app_path, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()
    
print(f"Verify line 1789 (index 1788?): {verify_lines[1788]}")
print(f"Verify line 1789 (index 1789?): {verify_lines[1789]}")

# Check for displayRankings
if "function displayRankings" in new_content:
    print("displayRankings FOUND in new content")
else:
    print("displayRankings NOT FOUND in new content")
