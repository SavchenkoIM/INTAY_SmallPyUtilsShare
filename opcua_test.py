
import opcua
import time
from datetime import datetime

def print_tree(root, ident = 0):
    for node in root.get_children():
        print('    ' * ident + node.get_display_name().Text)
    try:
        print_tree(node, ident+1)
    except:
        pass


client = opcua.Client("opc.tcp://192.168.10.10:4840")
client.connect()

#print_tree(client.get_objects_node())

quant = 50

readList = []
for i in range(quant):
    readList.append(client.get_node(f"ns=2;s=Application.GVL.READ"+str(i+1).zfill(2)))
writeList = []
for i in range(quant):
    writeList.append(client.get_node(f"ns=2;s=Application.GVL.WRIRE"+str(i+1).zfill(2)))

writearr = client.get_node(f"ns=2;s=Application.GVL.WRIRE_ARR")
readarr  = client.get_node(f"ns=2;s=Application.GVL.READ_ARR")


while(True):
    ts = datetime.now()
    writearr.set_attribute(opcua.ua.AttributeIds.Value, opcua.ua.DataValue(readarr.get_value()))
    time.sleep(0.1)
    print(int((datetime.now() - ts).total_seconds()*1000), "msec")


exit()


#while(True):
#    ts = datetime.now()
#    for i in range(quant):
#        writeList[0].set_value(opcua.ua.DataValue(opcua.ua.Variant(readList[i].get_value(), opcua.ua.VariantType.Int32)))
#    #time.sleep(0.098)
#    print(int((datetime.now() - ts).total_seconds()*1000), "msec")


