import os

def fix_css():
    style_path = 'static/css/style.css'
    header_path = 'full_header.css'
    
    print(f"Reading {style_path}...")
    try:
        with open(style_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading style.css: {e}")
        return

    # Extract tail (lines 232 onwards, 0-indexed is 232)
    # Line 232 in 1-indexed is index 231.
    # Let's look for the marker "/* --- RESTORED CONTENT FROM TAIL --- */"
    
    tail_start_index = -1
    for i, line in enumerate(lines):
        if "/* --- RESTORED CONTENT FROM TAIL --- */" in line:
            tail_start_index = i
            break
            
    if tail_start_index == -1:
        print("Could not find tail marker in style.css. Using line 232 as fallback.")
        tail_start_index = 231 # Fallback
        
    tail_lines = lines[tail_start_index:]
    print(f"Found tail starting at line {tail_start_index + 1}. Tail length: {len(tail_lines)} lines.")

    print(f"Reading {header_path}...")
    try:
        with open(header_path, 'r', encoding='utf-8') as f:
            header_lines = f.readlines()
    except Exception as e:
        print(f"Error reading full_header.css: {e}")
        return

    print(f"Header length: {len(header_lines)} lines.")
    
    new_content = header_lines + tail_lines
    
    print(f"Writing combined content to {style_path}...")
    try:
        with open(style_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        print("Success! style.css has been updated.")
    except Exception as e:
        print(f"Error writing style.css: {e}")

if __name__ == "__main__":
    fix_css()
