abc = 'SUBBA RAJUdjqj^&^^&&^788,,,,90,@%^&&},:;'
cleaned_value = abc.strip('''"',:;!?.()[]{}<>-''')
print(cleaned_value)  # Output: SUBBA RAJU
exit('PP')
abc = [[{"value":"SUBBA RAJU","ids":["1005","1006"]},{"value":"SUBBA RAJU","ids":["1043","1044"]},{"value":"SUBBA RAJU","ids":["1062","1063"]},{"value":"SUBBA RAJU","ids":["1077","1078"]},{"value":"SUBBA RAJU","ids":["1083","1084"]},{"value":"SUBBA RAJU","ids":["1090","1091"]},{"value":"SUBBA RAJU","ids":["1098","1099"]},{"value":"SUBBA RAJU","ids":["1107","1108"]},{"value":"SUBBA RAJU","ids":["1124","1125"]}],[{"value":"VEERAYYA","id":["1021"]},{"value":"VEERAYYA","id":["1055"]},{"value":"VEERAYYA","id":["1076"]},{"value":"VEERAYYA","id":["1088"]},{"value":"VEERAYYA","id":["1095"]},{"value":"VEERAYYA","id":["1103"]}],[{"value":"SULOCHANA","id":["1146"]}]]

def get_pairs(data):
    pairs = []
    for sublist in data:
        for item in sublist:
            if "id" in item:
                # for id_ in item["id"]:
                pairs.append((item["value"], tuple(item["id"])))
            elif "ids" in item:
                # for id_ in item["ids"]:
                pairs.append((item["value"], tuple(item["ids"])))   
    return pairs

print(get_pairs(abc))
exit('PLLLLLLLLL')

def calculate_metrics(actual_pairs, predicted_pairs):
    actual_set = set(actual_pairs)
    predicted_set = set(predicted_pairs)

    true_positives = actual_set & predicted_set  # Intersection
    print(f"True Positives: {true_positives}")
    precision = len(true_positives) / len(predicted_set) if predicted_set else 0.0
    recall = len(true_positives) / len(actual_set) if actual_set else 0.0

    # Optional: Print missed predictions
    false_negatives = actual_set - predicted_set
    for value, id_ in false_negatives:
        print(f"Not found: {value} with id {id_}")

    return precision, recall

precision, recall = calculate_metrics(actual_pairs, predicted_pairs)

abc = [[{'value': 'GOVARDHAN', 'ids': ['1006']}, {'value': 'GOVARDHAN', 'ids': ['1032']}, {'value': 'GOVARDHAN', 'ids': ['1058']}, {'value': 'GOVARDHAN', 'ids': ['1066']}, {'value': 'GOVARDHAN', 'ids': ['1080']}, {'value': 'GOVARDHAN', 'ids': ['1081']}], [{'value': 'MARILYN,', 'ids': ['1018']}], [{'value': 'MANAGER', 'ids': ['1057']}, {'value': 'MANAGER', 'ids': ['1070']}, {'value': 'MANAGER', 'ids': ['1079']}, {'value': 'MANAGER,', 'ids': ['1045']}]]


def get_pairs(data):
    pairs = []
    for sublist in data:
        for item in sublist:
            if "id" in item:
                for id_ in item["id"]:
                    pairs.append((item["value"], id_))
            elif "ids" in item:
                for id_ in item["ids"]:
                    pairs.append((item["value"], id_))
    return pairs





print(get_pairs(abc))