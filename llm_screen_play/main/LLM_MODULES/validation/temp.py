def split_list(lst, length):
    return [lst[i:i+length] for i in range(0, len(lst), length)]

def gt_convert(a):
    b = []
    for group in a:
        print(f"Processing group: {group}")
        for item in group:
            print(f"Processing item: {item}")
            value = item['value']
            if 'id' in item:
                ids = [item['id']]
            elif 'ids' in item:
                ids = item['ids']
            ids = [item for sublist in ids for item in sublist]
            value_len = max(1, len(value.split(' ')))
            print(f"Value: {value}, IDs: {ids}, Value Length: {value_len}")
            chunks = split_list(ids, value_len)
            print(f"Chunks: {chunks}")
            # Generate output
            expanded = []
            id_count = 0
            for chunk in chunks:
                expanded.append({'value': value, 'ids': chunk})
                
                # if chunk:
                #     for id_ in chunk:
                #         expanded.append({'value': value, 'ids': [id_]})
                #         id_count += 1
                # else:
                #     expanded.append({'value': value, 'ids': ['unable to assign ids']})

            b.append(expanded)

    return b

a = [[
    {"value": "BUM", "id": ["1008", "1081", "1170", "1192", "1207", "1227", "1242", "1249", "1265"]},
    {"value": "CHINTHAN BABA", "id": ["1024", "1025", "1065", "1066", "1070", "1071", "1105", "1106", "1141", "1142", "1160", "1161", "1179", "1180", "1199", "1200", "1215", "1216", "1234", "1235", "1271", "1272"]},
    {"value": "SHAM GOPAL VERMA", "id": ["1037", "1038", "1039", "1086", "1087", "1088", "1129", "1130", "1131"]}
    ]]
print(gt_convert(a))