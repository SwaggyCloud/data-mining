import sys

input_raw = []
for line in sys.stdin:
    input_raw.append(line)
min_support = int(input_raw[0])
input_raw.pop(0)
input_prop = []
size = len(input_raw)
index = 0
while index < size:
    ss = input_raw[index]
    ss = ss.strip()
    input_prop.append(ss.split())
    index = index + 1


def apriori(data, minSup):
    dictOneItem = {}
    for transaction in data:
        for item in transaction:
            if item in dictOneItem:
                dictOneItem[item] += 1
            else:
                dictOneItem[item] = 1
    keys = dictOneItem.keys()

    keys1 = []
    for i in keys:
        keys1.append([i])
    cutKeys1 = []
    for k in keys1[:]:
        if dictOneItem[k[0]] >= minSup:
            cutKeys1.append(k)
    cutKeys1.sort()
    keys = cutKeys1
    all_keys = []
    all_keys_dict = {}
    support = []
    while keys != []:
        keys.sort()
        C = getSupport(data, keys)
        cutKeys = prune(keys, C, minSup, support,all_keys_dict)
        for key in cutKeys:
            str = ' '.join(key)
            all_keys.append(str)
        keys = combaine(cutKeys)
    sorted_dict=sorted(all_keys_dict.items(),key=lambda x:(-x[1],x[0]))
    return all_keys_dict,sorted_dict

def getSupport(D, keys):
    support = []
    for key in keys:
        buffer = 0
        for T in D:
            flag = True
            for k in key:
                if k not in T:
                    flag = False
            if flag:
                buffer += 1
        support.append(buffer)
    return support

def prune(keys, C, minSup, support, all_keys_dicts):
    buffer = keys
    bufferSupport = C
    i = 0
    for item in buffer.copy():
        if bufferSupport[i] < minSup:
            buffer.remove(item)
        else:
            str = ' '.join(item)
            all_keys_dicts[str] = C[i];
            support.append(bufferSupport[i])
        i += 1
    return buffer

def combaine(keys1):
    keys2 = []
    for k1 in keys1:
        for k2 in keys1:
            if k1 != k2:
                key = []
                for k in k1:
                    if k not in key:
                        key.append(k)
                for k in k2:
                    if k not in key:
                        key.append(k)
                key.sort()
                if key not in keys2:
                    keys2.append(key)
    return keys2

def getClosed(frequent,dict):
    closed = []
    delClosed = []
    for i in range(len(frequent)):
        closed.append(frequent[i][0])
    # print ('closed = ',closed)
    buffer = closed.copy()
    for index in range(len(buffer)):
        for i in range(len(buffer)):
            l1 = buffer[i].split()        
            for j in range(len(buffer)):
                if i == j:
                    continue
                l2 = buffer[j].split()
                if len(l1) > len(l2):
                    longer = l1
                    shorter = l2
                    strLonger = ' '.join(l1)
                    strShorter = ' '.join(l2)
                else:
                    longer = l2
                    shorter = l1
                    strLonger = ' '.join(l2)
                    strShorter = ' '.join(l1)
                counter = len(shorter)
                for item in shorter:
                    if item in longer:
                        counter -= 1
                if counter == 0 and dict.get(strShorter) <= dict.get(strLonger):
                    str = " ".join(shorter)
                    if str in closed:
                        if str not in delClosed:
                            delClosed.append(str)
                # max.remove()
    for i in range(len(delClosed)):
        closed.remove(delClosed[i])
    return closed

def getMaximal(frequent):
    deleteMax = []
    max = []
    for i in range(len(frequent)):
        max.append(frequent[i][0])
    buffer = max.copy()
    for i in range(len(buffer)):
        l1 = buffer[i].split()        
        for j in range(len(buffer)):
            if i == j:
                continue
            l2 = buffer[j].split()
            if len(l1) > len(l2):
                longer = l1
                shorter = l2
            else:
                longer = l2
                shorter = l1
            counter = len(shorter)
            for item in shorter:
                if item in longer:
                    counter -= 1
            if counter == 0:
                str = " ".join(shorter)
                if str in max:
                    if str not in deleteMax:
                        deleteMax.append(str)
                # max.remove()
    for i in range(len(deleteMax)):
        max.remove(deleteMax[i])
    # print('max =', max)
    return max


d, sup = apriori(input_prop, 2)
closed = getClosed(sup, d)
max = getMaximal(sup)
for i in range(len(sup)):
    print(sup[i][1],' [',sup[i][0],']',sep='')
print('')
for i in range(len(closed)):
    print(d.get(closed[i]),' [',closed[i],']',sep='')
print('')
for i in range(len(max)):
    print(d.get(max[i]),' [',max[i],']',sep='')