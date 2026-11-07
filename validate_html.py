with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Check line 6306
lines = text.split('\n')
print(f"Line 6304: {lines[6303]}")
print(f"Line 6305: {lines[6304]}")
print(f"Line 6306: {lines[6305]}")
print(f"Line 6307: {lines[6306]}")
print(f"Line 6308: {lines[6307]}")

# Extract inline script
s_idx = text.find('<!-- Embedded Dashboard Data & Logic -->')
sub = text[s_idx:]
start = sub.find('<script>') + 8
end = sub.find('</script>')
js = sub[start:end]

# Check template literals in js
in_backtick = False
in_single = False
in_double = False
escape = False

for line_idx, line in enumerate(js.split('\n'), 1):
    for char_idx, c in enumerate(line):
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '`' and not in_single and not in_double:
            in_backtick = not in_backtick
        elif c == "'" and not in_backtick and not in_double:
            in_single = not in_single
        elif c == '"' and not in_backtick and not in_single:
            in_double = not in_double

print(f"Final state: in_backtick={in_backtick}, in_single={in_single}, in_double={in_double}")
if not in_backtick and not in_single and not in_double:
    print("ALL quotes and template literals in JavaScript are completely balanced and closed!")
