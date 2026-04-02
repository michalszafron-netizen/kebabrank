import os

app_path = r'static/js/app.js'
fix_path = r'final_fix.js'

try:
    with open(app_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Keep first 1782 lines
    head = lines[:1782]
    
    with open(fix_path, 'r', encoding='utf-8') as f:
        fix_content = f.read()
    
    # Add newline if needed
    if not head[-1].endswith('\n'):
        head.append('\n')
        
    new_content = "".join(head) + fix_content
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully rebuilt app.js: {len(head)} lines from head + {len(fix_content.splitlines())} lines from fix.")

except Exception as e:
    print(f"Error: {e}")
