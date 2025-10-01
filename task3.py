def parse_rational(s):
    is_negative = s.startswith('-')
    if is_negative:
        s = s[1:]  
    
    if '.' in s:
        integer_part, decimal_part = s.split('.')
        decimal_part = decimal_part[:10]  
        denominator = 10 ** len(decimal_part)
        numerator = int(integer_part) * denominator + int(decimal_part)
        
        if is_negative:
            numerator = -numerator
        
        return (numerator, denominator)
    else:
        return (-int(s), 1) if is_negative else (int(s), 1)

def are_equal(rational1, rational2):
    num1, den1 = rational1
    num2, den2 = rational2
    
    return num1 * den2 == num2 * den1

def compare_rationals(rational1, rational2):
    num1, den1 = rational1
    num2, den2 = rational2
    
    val1 = num1 * den2
    val2 = num2 * den1
    
    if val1 < val2:
        return -1
    elif val1 > val2:
        return 1
    else:
        return 0

def find_position(sequence, target):
    for i, item in enumerate(sequence):
        if are_equal(item, target):
            return i + 1  
    return 0  

all_lines = []
while True:
    try:
        line = input()
        all_lines.append(line)
    except EOFError:
        break

line_index = 0

N = int(all_lines[line_index])
line_index += 1

sequence = []
for _ in range(N):
    s = all_lines[line_index].strip()
    rational = parse_rational(s)
    sequence.append(rational)
    line_index += 1

M = int(all_lines[line_index])
line_index += 1

for _ in range(M):
    query = all_lines[line_index].strip()
    target = parse_rational(query)
    position = find_position(sequence, target)  
    print(position)
    line_index += 1