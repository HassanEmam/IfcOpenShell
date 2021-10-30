import os
import sys
import argparse

from p6xer2ifc import P6XER2Ifc
from p62ifc import P62Ifc
from msp2ifc import MSP2Ifc
import ifcopenshell

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--file', action='store', type=str, 
                           required=True, help="schedule file name to be parsed")
    cli_parser.add_argument('--schedule', action='store', required=True,
                           type=str, help='file format as xer, p6xml, mspxml')
    cli_parser.add_argument('--ifcfile', action='store', required=True,
                           type=str, help='ifc file name as string e.g. \"file.ifc\"')
    args = cli_parser.parse_args()
    print(args, args.file, args.schedule)
    
    if args.schedule== "xer":
        p6xer = P6XER2Ifc()
        p6xer.xer = args.file
        p6xer.file = ifcopenshell.open(args.ifcfile)
        res = p6xer.execute()
    elif args.schedule == "mspxml":
        msp = MSP2Ifc()
        msp.xml = args.file()
        msp.file = ifcopenshell.open(args.ifcfile)
        res = msp.execute()
    elif args.schedule == "p6xml":
        p6xml = P62Ifc()
        p6xml.xml = args.file
        p6xml.file = ifcopenshell.open(args.ifcfile)
        res = p6xml.execute()
    else:
        print("schedule type you selected is not implemented at the moment")

