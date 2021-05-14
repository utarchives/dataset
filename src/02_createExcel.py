import json
import yaml
import glob
import pandas as pd
import os

f = open("../settings.yml", "r+")
settings = yaml.safe_load(f)

files = glob.glob(settings["output_dir"] + "/api/items/*.json")

map = {}
properties = []
propertiesMap = {}

for i in range(len(files)):
    file = files[i]

    if i % 100 == 0:
        print(i+1, len(files))


    with open(file) as f:
        df = json.load(f)

        obj = {}

        for key in df:
            value = df[key]

            # nullの場合
            if not value:
                continue

            if "o:created" in key or "o:modified" in key:
                obj[key] = [value["@value"]]
            elif "o:media" in key:
                obj["_:media_size"] = [str(len(value))]
            elif "o:item_set" in key:
                values = []
                for e in value:
                    values.append(str(e["o:id"]))
                obj[key] = values
            elif "o:resource_class" in key or "o:resource_template" in key or "o:owner" in key:
                obj[key] = [str(value["o:id"])]
            elif "o:" in key:
                obj[key] = [str(value)]
            elif ":" in key:
                values = []
                for e in value:
                    values.append(e["@id"] if "@id" in e else e["@value"])

                    targets = ["property_label", "is_public", "type"]

                    if key not in propertiesMap:
                        tmp = {}
                        for t in targets:
                            tmp[t] = {}
                        propertiesMap[key] = tmp

                    propertiesObj = propertiesMap[key]
                    
                    

                    for t in targets:

                        property_label = e[t]

                        if property_label not in propertiesObj[t]:
                            propertiesObj[t][property_label] = 0
                        propertiesObj[t][property_label] += 1


                obj[key] = values
            elif "@type" in key:
                values = []
                for e in value:
                    if e != "o:Item":
                        values.append(e)

                obj[key] = values

        for key in obj:
            if key not in properties:
                properties.append(key)

        map[df["o:id"]] = obj

rows = []
properties = sorted(properties)

row = []
for p in properties:
    row.append(p)
rows.append(row)

for oid in sorted(map):
    row = []
    rows.append(row)
    item = map[oid]
    for p in properties:
        value = ""
        if p in item:
            value = "|".join(item[p])
        row.append(value)

df = pd.DataFrame(rows)

dirpath = "data"
os.makedirs(dirpath, exist_ok=True)

df.to_excel(dirpath + '/items_all.xlsx',
            index=False, header=False)

######

rows = []
rows.append(["id", "property_label", "is_public", "type"])

for pid in sorted(propertiesMap):
    propertiesObj = propertiesMap[pid]
    row = [pid, propertiesObj["property_label"], propertiesObj["is_public"], propertiesObj["type"]]
    rows.append(row)

df = pd.DataFrame(rows)
df.to_excel(dirpath + '/items_properties.xlsx',
            index=False, header=False)