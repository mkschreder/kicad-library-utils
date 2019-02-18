import argparse
from schlib import *
from suds.client import Client
import time

with open("mouser-key.txt", 'r') as keyfile:
    mouser_key = keyfile.read().replace('\n', '');

client = Client("https://api.mouser.com/service/searchapi.asmx?WSDL")

header = client.factory.create("ns0:MouserHeader")
header.AccountInfo.PartnerID = mouser_key
client.set_options(soapheaders=header);

parser = argparse.ArgumentParser(description='Check KiCad project library for missing part numbers')
parser.add_argument('libfiles', nargs='+')
parser.add_argument('--fix', help='Try to fix all issues with the libraries automatically', action='store_true')
parser.add_argument('--online', help='Check component availability online and report any errors', action='store_true')
parser.add_argument('--update', help='Update fields information from online server even if vendor is assigned', action='store_true')
parser.add_argument('--dump', help='Dump all component information', action='store_true')
parser.add_argument('--footprints', help='Dump list of all footprints used', action='store_true')
args = parser.parse_args();

footprints = {};
for libfile in args.libfiles:
    lib = SchLib(libfile);
    for component in lib.components:
        footprint = component.fields[2];
        if not component.fields[0]["reference"].startswith("\"#") and not footprint["name"]:
            print("Component %s: Missing footprint!" % component.name);
        else:
            footprints[footprint["name"]] = footprint["name"];
        mpn = component.field("MPN")
        if mpn:
            if mpn["visibility"] == 'V':
                if args.fix:
                    mpn["visibility"] = 'I';
                else:
                    print("Component %s: MPN is visible!" % component.name);
            if args.online and not mpn["name"].startswith("#") and (not component.field("Vendor") or not component.field("Availability") or not component.field("Description") or not component.field("LifeCycle") or not component.field("Price") or args.update):
                try:
                    time.sleep(2); # up to 30 calls per minute
                    res = client.service.SearchByPartNumber(mpn["name"])
                except:
                    break
                if(len(res.Parts) == 0):
                    print("Component %s: Not found online!" % component.name);
                else:
                    part = res.Parts[0][0];
                    component.addField({"fieldname": "Availability", "name": part.Availability if hasattr(part, "Availability") else "Not Available"});
                    component.addField({"fieldname": "Description", "name": part.Description or ""});
                    component.addField({"fieldname": "LifeCycle", "name": part.LifecycleStatus or "OK"});
                    component.addField({"fieldname": "Vendor", "name": "Mouser"});
                    #component.addField({"fieldname": "Datasheet", "name": part.DataSheetUrl or ""});
                    component.fields[3]["name"] = part.DataSheetUrl or "";
                    component.addField({"fieldname": "Price", "name": part.PriceBreaks[0][0].Price.encode("ascii", "ignore").replace(",", ".") + " " + part.PriceBreaks[0][0].Currency if len(part.PriceBreaks) > 0 else "Not Available"});
                    #print("Component %s: Availability: %s, Description: %s, Lifecycle: %s, Price: %s" % (component.name, part.Availability if hasattr(part, "Availability") else "Not Available", part.Description, part.LifecycleStatus, part.PriceBreaks[0][0].Price if len(part.PriceBreaks) > 0 else "Not Available"));
                #print res
            if not mpn["name"].startswith("#") and args.dump:
                try:
                    print("Component %s: Availability: %s, Description: %s, Lifecycle: %s, Price: %s, Footprint: %s" % (component.name, component.field("Availability")["name"], component.field("Description")["name"], component.field("LifeCycle")["name"], component.field("Price")["name"], footprint["name"]));
                except:
                    pass
        else:
            print("Component %s missing MPN!" % component.name);
            
    if args.fix:
        lib.save();

if args.footprints: 
    for key in footprints:
        print(key);
