import sys
import math

def process_data(data):
    num_attribute = len(data[0]) - 1
    # print(num_attribute)
    label = []
    attributes = []
    for i in range(len(data)):
        buffer = data[i]
        label.append(buffer[0])
        attributes.append(buffer[1:])
    return label, attributes

def process_data_dt(data):
    res = []
    label = []
    for i in range(len(data)):
        label.append(int(data[i][0]))
        data[i].pop(0)
    # print(label)
    # print(data)
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = data[i][j].split(':')
            data[i][j][0] = int(data[i][j][0])
            data[i][j][1] = float(data[i][j][1])
    return data, label   

def cal_ini_gini(label):
    label_count = {}
    for i in range(len(label)):
        temp = label[i]
        if temp in label_count:
            label_count[temp] += 1
        else:
            label_count[temp] = 1
    # print(label_count)
    sum_val = sum(label_count.values())
    gini = 1
    for key, value in label_count.items():
        gini -= (value/sum_val)**2
    return gini

def cal_thres(data, index):
    # print(data)
    buffer = []
    for i in range(len(data)):
        buffer.append(data[i][index][1])
    # print(buffer)
    sort_data = sorted(buffer)
    # print(sort_data)
    thres = {}
    thres_buf = []
    margin_buf = []
    for i in range(len(sort_data)):
        if i+1 in range(len(data)):
            temp = (sort_data[i] + sort_data[i+1])/2
            thres_buf.append(temp)
            thres[temp] = 1
    # print(thres)
    return thres, thres_buf
                
            
def cal_gini(data, threshold, index, label):
    dim = len(data)
    # print(dim)
    big = 0.
    small = 0.
    big_label = {}
    small_label = {}
    for i in range(dim):
        # print(data[i][index])
        if data[i][index][1] <= threshold:
            small += 1.
            temp = label[i]
            if label[i] in small_label:
                small_label[temp] += 1
            else:
                small_label[temp] = 1
        else:
            big += 1.
            temp = label[i]
            
            if label[i] in big_label:
                big_label[temp] += 1
            else:
                big_label[temp] = 1
    sum_val = small + big
    big_poss = [*big_label.values()]
    small_poss = [*small_label.values()]
    big_poss_sum = 0
    small_poss_sum = 0
    for i in range(len(big_poss)):
        buffer = big_poss[i] / big
        big_poss_sum += buffer**2
    
    for i in range(len(small_poss)):
        buffer = small_poss[i] / small
        small_poss_sum += buffer**2
        
    gini = (big/sum_val)*(1 - big_poss_sum) + (small/sum_val)*(1 - small_poss_sum )
    # print("big_label", big_label,"small", small_label)
    # print("small:", small,"big:", big, "index", index, "threshold", threshold, "gini", gini)
    return gini

def split_db(data, label, index, thres):
    db1 = []
    db2 = []
    db1_label = []
    db2_label = []
    for i in range(len(data)):
        if data[i][index][1] <= thres:
            db1.append(data[i])
            db1_label.append(label[i])
        else:
            db2.append(data[i])
            db2_label.append(label[i])
    return db1,db1_label,db2,db2_label

def make_tree(data_dt, label_dt):
    gini_min = 1
    threta = 0
    gini_index = 0
    # gini_buffer = []
    thres_buffer = []
    margin_buffer = []
    for i in range (len(data_dt[0])):
        thres, thres_index = cal_thres(data_dt, i)
        # sort_thres = sorted(thres.items(), key = lambda x:x[0])
        thres_key = [*thres.keys()]
        thres_buffer.append(thres_index)
        # margin_buffer.append(margin)
        # print(thres)
        for key, value in thres.items():
            # print(key)
            gini = cal_gini(data_dt, key, i, label_dt)
            # gini_buffer.append([gini,key,i])
            # print("gini", gini, "threshold", key,"index", i)
            if gini < gini_min:
                gini_min = gini
                gini_index = i
                threta = key
            elif gini == gini_min:
                if gini_index == i:
                    if threta > key:
                        threta = key
                elif gini_index > i:
                    gini_index = i
                    threta =key    
    # # print(gini_min,"index_min", gini_index,"thres_min", threta)
    # gini_sorted = sorted(gini_buffer, key =lambda x:x[0])
    # # print(gini_sorted)
    # baseline = gini_sorted[0][0]
    # index = sys.maxsize
    # thre = []
    # # print(baseline)
    # for i in range(len(gini_sorted)):
    #     if gini_sorted[i][0] == baseline:
    #         if gini_index == gini_sorted[i][2]:
    #             thre.append(gini_sorted[i][1])
    # # if len(thre) != 1:
    # #     temp = thres_buffer[gini_index]
    # #     # print("thres_buffer = ",thres_buffer[gini_index])
    # #     temp1 = margin_buffer[gini_index]
    # #     # print("margin", temp1)
    # #     # print(thre)
    # #     best = -sys.maxsize
    # #     record = 0.
    # #     for i in range(len(thre)):
    # #         idx = temp.index(thre[i])
    # #         mar = temp1[idx]
    # #         if mar > best:
    # #             best = mar
    # #             record = thre[i]
    # #     # print(record)
    # #     threta = record
    # # print(sorted(thre))
    # # print(thre)
    # # print(thres_buffer[index])
    
    res = [gini_index, threta]
    db1,db1_label,db2,db2_label = split_db(data_dt, label_dt, gini_index, threta)
    return db1,db1_label,db2,db2_label,res
    
def dtree(data_dt, label_dt):
    ini_gini = cal_ini_gini(label_dt)
    lv1_left,lv1_left_label,lv1_right,lv1_right_label, res1 = make_tree(data_dt, label_dt)
    # print("first: index", res1[0],"threshold", res1[1])
    db1,db1_l,db2,db2_l, res2 = make_tree(lv1_left, lv1_left_label)
    
    label_1 = {}
        
    for i in range(len(db1_l)):
        temp = db1_l[i]
        if temp in label_1:
            label_1[temp] += 1
        else:
            label_1[temp] = 1
    label_2 = {}

    for i in range(len(db2_l)):
        temp = db2_l[i]
        if temp in label_2:
            label_2[temp] += 1
        else:
            label_2[temp] = 1
            
    # print("left: index", res2[0],"threshold", res2[1])
    # print("label left", label_1)
    # print("label right", label_2)

    db3,db3_l,db4,db4_l,res3 = make_tree(lv1_right, lv1_right_label)
    
    label_3 = {}
    # if len(db3_l) == 0:
    #     db3_l = db4_l
    for i in range(len(db3_l)):
        temp = db3_l[i]
        if temp in label_3:
            label_3[temp] += 1
        else:
            label_3[temp] = 1
            
    label_4 = {}

    for i in range(len(db4_l)):
        temp = db4_l[i]
        if temp in label_4:
            label_4[temp] += 1
        else:
            label_4[temp] = 1
    
    # print("right: index", res3[0],"threshold", res3[1])
    # print("label left", label_3)
    # print("label right", label_4)
    
    label_res1 = sorted(label_1.items(),key = lambda item:item[1], reverse = True)
    label_res2 = sorted(label_2.items(),key = lambda item:item[1], reverse = True)
    label_res3 = sorted(label_3.items(),key = lambda item:item[1], reverse = True)
    label_res4 = sorted(label_4.items(),key = lambda item:item[1], reverse = True)
    
    # print(label_res1[0][0])
    # print(label_res2[0][0])
    # print(label_res3[0][0])
    # print(label_res4[0][0])
    helper1 = label_res1[0][0]
    baseline1 = label_res1[0][1]
    # print(baseline)
    for i in range(len(label_res1)):
        buffer = label_res1[i][1]
        buffer_l = label_res1[i][0]
        # print(buffer)
        if buffer == baseline1:
            if buffer_l < helper1:
                helper1 = buffer_l

    
    helper2 = label_res2[0][0]
    baseline2 = label_res2[0][1]
    # print(baseline)
    for i in range(len(label_res2)):
        buffer = label_res2[i][1]
        buffer_l = label_res2[i][0]
        # print(buffer)
        if buffer == baseline2:
            if buffer_l < helper2:
                helper2 = buffer_l
                
    helper3 = label_res3[0][0]
    baseline3 = label_res3[0][1]
    # print(baseline)
    for i in range(len(label_res3)):
        buffer = label_res3[i][1]
        buffer_l = label_res3[i][0]
        # print(buffer)
        if buffer == baseline3:
            if buffer_l < helper3:
                helper3 = buffer_l
                
    
    helper4 = label_res4[0][0]
    baseline4 = label_res4[0][1]
    # print(baseline)
    for i in range(len(label_res4)):
        buffer = label_res4[i][1]
        buffer_l = label_res4[i][0]
        # print(buffer)
        if buffer == baseline4:
            if buffer_l < helper4:
                helper4 = buffer_l
                
                
    label_res = [helper1, helper2, helper3, helper4]
    thres_val = [res1, res2, res3]

    return label_res, thres_val

def get_label(test, label, thres):
    for i in range (len(test)):
        label_res = 0
        buffer = test[i]
        ini = thres[0]
        left = thres[1]
        right = thres[2]
        if buffer[ini[0]][1] <= ini[1]:
#             left
            if buffer[left[0]][1] <= left[1]:
                label_res = label[0]
            else:
                label_res = label[1]
        else:
            if buffer[right[0]][1] <= right[1]:
                label_res = label[2]
            else:
                label_res = label[3]
        print(label_res)

    
def KNN(data,label,test,k):
    attri = []
    dim = len(test)
    num_attri = len(data)
    distance = []
    # print(data)
    for i in range(num_attri):
        buffer = data[i]
        buf_l = int(label[i])
        sum_val = 0
        for j in range(dim):
            temp1 = float((buffer[j].split(':'))[1])
            temp2 = float((test[j].split(':'))[1])
            sum_val += (temp1 - temp2)**2
            res = sum_val**0.5
        distance.append([res, buf_l])
    # print(distance)
    sort_dis = sorted(distance, key = lambda x:x[0])
    # print(sort_dis)
    labels_count = {}
    no_0 = sort_dis[0][1]
    no_1 = sort_dis[1][1]
    if sort_dis[2][0] == sort_dis[3][0]:
        if sort_dis[2][1] > sort_dis[3][1]:
            no_2 = sort_dis[3][1]
        else:
            no_2 = sort_dis[2][1]
    else:
        no_2 = sort_dis[2][1]
    
    labels_count[no_0] = 1
    if no_1 in labels_count:
        labels_count[no_1] += 1
    else:
        labels_count[no_1] = 1
    
    if no_2 in labels_count:
        labels_count[no_2] += 1
    else:
        labels_count[no_2] = 1
    
    # print(labels_count)
    sorted_label = sorted(labels_count.items(), key=lambda d:d[1], reverse=True)
    if len(labels_count) == 3:
        keys = [*labels_count.keys()]
        sort_keys = sorted(keys)
        print(sort_keys[0])
    else:
        print(sorted_label[0][0])
    
#     helper = sys.maxsize
#     baseline = sorted_label[0][1]
    
#     for i in range(len(sorted_label)):
#         buffer = sorted_label[i][1]
#         buffer_l = int(sorted_label[i][0])
#         if buffer == baseline:
#             if buffer_l < helper:
#                 helper = buffer_l
#     print(helper)
    
    
if __name__ == "__main__":
    k_val = 3
    input_raw =[]
    for line in sys.stdin:
        input_raw.append(line)
    data_set = []
    test_case = []
    num_input = len(input_raw)
    for i in range(num_input):
        buffer = input_raw[i]
        list = buffer.split()
        if list[0] == '0':
            test_case.append(list)
        else:
            data_set.append(list)
    
    data_label, data_attri = process_data(data_set)
    _,test_attri = process_data(test_case)
    data_dt, label_dt = process_data_dt(data_set)
    test_dt, _ = process_data_dt(test_case)
    # print(test_dt)
    label_res, thres_val = dtree(data_dt, label_dt)
    get_label(test_dt, label_res, thres_val)
    print('')
#   KNN part

    for i in range (len(test_attri)):
        res = KNN(data_attri,data_label,test_attri[i],k_val)    
    
    
    


