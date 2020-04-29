import sys

minSup = 2
minLen = 2
maxLen = 5
input_raw = []
for line in sys.stdin:
    input_raw.append(line)
    
# input_raw = ['good grilled sandwich and french fries , but the service is bad\n', 'disgusting fish sandwich , but good french fries\n', 'their grilled fish sandwich is the best fish sandwich , but pricy\n','A B A B A B A']
d1 = {}
d2 = {}
for i in range(len(input_raw)):
    input_prop = input_raw[i].split();
    for j in range(len(input_prop)):
        if input_prop[j] in d1:
            d1[input_prop[j]] += 1
        else:
            d1[input_prop[j]] = 1
# print(d1)

for p in range(len(input_raw)):
    # every line
    input_prop = input_raw[p].split();
    for i in range(len(input_prop)):
        #every single word 
        j = i + 1
        if d1[input_prop[i]] < minSup:
            continue
        else:
            while j < len(input_prop) and j < i + maxLen:
                if d1[input_prop[j]] < minSup:
                    break
                buffer = []
                for index in range(i,j+1):
                    buffer.append(input_prop[index])
                buffer_str = ' '.join(buffer)
                j += 1
                if buffer_str not in d2:
                    d2[buffer_str] = 1
                else:
                    d2[buffer_str] += 1
buf = d2.copy()
for (key,value) in buf.items():
    if value < minSup:
        d2.pop(key)
        
sorted_dict=sorted(d2.items(),key=lambda x:(-x[1],x[0]))
size = len(sorted_dict)
if size > 20:
    size = 20
for i in range(size):
    print("[",sorted_dict[i][1],", '",sorted_dict[i][0],"']",sep='')