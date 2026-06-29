from pathlib import Path
path = Path(r'C:/Users/GOKUL PAWAR/OneDrive/Desktop/SheStarts AI Career Counselor/app.py')
text = path.read_text(encoding='utf-8')
pattern = 'elif page == "Dashboard":'
pos = text.find(pattern)
if pos == -1:
    raise SystemExit('pattern not found')
new_text = text[:pos] + 'elif page == "Career Counselor":' + text[pos + len(pattern):]
path.write_text(new_text, encoding='utf-8')
print('patched')
