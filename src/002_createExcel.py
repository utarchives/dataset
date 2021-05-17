import json
import yaml
import glob
import pandas as pd
import os
import argparse

######

parser = argparse.ArgumentParser()

parser.add_argument("type", help='items, item_sets, ..')

args = parser.parse_args()

target = args.type

######

f = open("../settings.yml", "r+")
settings = yaml.safe_load(f)

######

# 出力フォルダ

dirpath = "data/" + target
os.makedirs(dirpath, exist_ok=True)

######

files = glob.glob(settings["output_dir"] + "/api/"+target+"/*.json")

dataMap = {}
properties = []
propertiesMap = {}

for i in range(len(files)):
    file = files[i]

    if i % 100 == 0:
        print(i+1, len(files), file)

    with open(file) as f:
        df = json.load(f)

        obj = {}

        for key in df:
            value = df[key]

            # nullの場合
            if not value:
                continue

            if key in ["o:created", "o:modified"]:
                values = []
                if type(value) is str:
                    values = [value]
                else:
                    values = [value["@value"]]
                obj[key] = values
            elif key in ["o:media"]:
                obj["_:media_size"] = [str(len(value))]
            elif "o:item_set" in key:
                values = []
                for e in value:
                    values.append(str(e["o:id"]))
                obj[key] = values
            elif key in ["o:resource_class", "o:resource_templates", "o:owner", "o:item"]:
                obj[key] = [str(value["o:id"])]
            elif key in ["o:thumbnail_urls"]:
                continue
            elif "o:" in key:
                obj[key] = [str(value)]
            elif ":" in key:
                values = []
                for e in value:
                    try:
                        values.append(e["@id"] if "@id" in e else e["@value"])

                        targets = ["property_label", "is_public", "type"]

                        if key not in propertiesMap:
                            tmp = {}
                            for t in targets:
                                tmp[t] = {}
                            propertiesMap[key] = tmp

                        propertiesObj = propertiesMap[key]

                        for t in targets:
                            if t in e:
                                property_label = e[t]
                                if property_label not in propertiesObj[t]:
                                    propertiesObj[t][property_label] = 0
                                propertiesObj[t][property_label] += 1

                    except Exception as err:
                        print("Err", key, e, err)

                obj[key] = values
            elif "@type" in key:
                values = []

                if type(value) is str:
                    value = [value]

                for e in value:
                    if e != "o:Item":
                        values.append(e)

                obj[key] = values

        for key in obj:
            if key not in properties:
                properties.append(key)

        dataMap[df["o:id"]] = obj

######　出力

rows = []
properties = sorted(properties)

row = []
for p in properties:
    row.append(p)
rows.append(row)

for oid in sorted(dataMap):
    row = []
    rows.append(row)
    item = dataMap[oid]
    for p in properties:
        value = ""
        if p in item:
            value = "|".join(item[p])
        
        # 数字の場合は変換
        if value.isdecimal():
            value = int(value)
        row.append(value)

df = pd.DataFrame(rows)
df.to_excel(dirpath + '/list.xlsx',
            index=False, header=False)

######　プロパティの出力

rows = []
rows.append(["id", "property_label", "is_public", "type"])

for pid in sorted(propertiesMap):
    propertiesObj = propertiesMap[pid]
    row = [pid, propertiesObj["property_label"], propertiesObj["is_public"], propertiesObj["type"]]
    rows.append(row)

df = pd.DataFrame(rows)
df.to_excel(dirpath + '/properties.xlsx',
            index=False, header=False)