import json, xmltodict, yaml

def csv_to_json(data):
    tempDec = {}
    json_data = []
    rows = data['data'].split("\n")
    keys = rows.pop(0).split(",")
    for i in range(len(rows)):
        rows[i] = rows[i].split(",")
    for i in range(len(rows)-1):
        for j in range(len(keys)):
            tempDec[keys[j]] = rows[i][j]
        json_data.append(json.loads(json.dumps(tempDec)))
    return json_data

def to_common_data_type(data):
    data_resp = []
    if 'mime_type' in data:
        if data['mime_type'] == 'application/xml':
            for dt in json.loads(json.dumps(xmltodict.parse(data['data'])))['dataset']['record']:
                data_resp.append(dt)
        elif data['mime_type'] == 'text/csv':
            for dt in (csv_to_json(data)):
                data_resp.append(dt)
        elif data['mime_type'] == 'application/x-yaml':
            for dt in json.loads(json.dumps(yaml.safe_load(data['data']))):
                data_resp.append(dt)
    else:
        tmp = str(data['data'])
        # FCINKG COMMA
        if tmp[len(tmp)-3] == ',':
            tmp = tmp[0:-3]
            tmp = tmp + ']'            
        for dt in json.loads(tmp):
            data_resp.append(dt)   
    return data_resp