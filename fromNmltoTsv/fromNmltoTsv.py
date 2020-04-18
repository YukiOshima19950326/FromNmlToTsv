import xml.etree.ElementTree as ET
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", type=str,help="input file path")
    parser.add_argument("-o","--output", type=str,help="output file path")
    args = parser.parse_args()

    tree = ET.parse(args.input) 
    root = tree.getroot()
    
    tracklist=[]
    for i in root[2]:
        record = []
        try: record.append(i.attrib["ARTIST"])
        except: record.append(None)

        try: record.append(i.attrib["TITLE"])
        except: record.append(None)

        try: record.append(i.find("ALBUM").attrib["TITLE"])
        except: record.append(None)

        try: record.append(i.find("LOCATION").attrib["VOLUME"]+i.find("LOCATION").attrib["DIR"]+i.find("LOCATION").attrib["FILE"])
        except: record.append(None)

        try: record.append(i.find("INFO").attrib["LABEL"])
        except: record.append(None)

        try: record.append(i.find("TEMPO").attrib["BPM"])
        except: record.append(None)

        tracklist.append(record)

    order =[]
    for i in root[4][0][0][0][0]:
        order.append(i[0].attrib["KEY"])


    track_data = pd.DataFrame(tracklist,columns=["ARTIST","TITLE","ALBUM","LOCATION","LABEL","BPM"])
    order_data = pd.DataFrame(order,columns=["KEY"])

    data = order_data.merge(track_data,how="inner",left_on="KEY",right_on="LOCATION").loc[:,["ARTIST","TITLE","ALBUM","LABEL","BPM"]]
    data.index = data.index + 1
    data.to_csv(args.output,sep='\t',index=True)

if __name__ == "__main__":
    main()