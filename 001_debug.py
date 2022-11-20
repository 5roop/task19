test_file = "../SRB/S/ParlaMint-RS_T04S3.xml"

from typing import Union, List
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from xml.etree.ElementTree import Element, SubElement, tostring, XML, parse, fromstring

from xml.dom import minidom
def pretty_print(s) -> None:
    print(minidom.parseString(tostring(s).decode("utf")).toprettyxml("\t"))
def pretty_string(s) -> None:
    return minidom.parseString(tostring(s).decode("utf")).toprettyxml("\t")

with open(test_file, "r") as f:
    content = f.read().replace('<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang',
                               '<TEI xml:lang')
    
    
def extract_remarks(full_text: str) -> list:
    import re
    separators = [
        {"Gap_inaudible": r"""([/(].{0,50}[nN]e razumije.{0,50}[/)]|[/(].{0,50}ne čuje.{0,50}[/)]|[/(].{0,50}[iI]sključen mikrofon.{0,2}[/)]|[/(][nN]ije uključen mikrofon.{0,1}[/)]|[/(][gG]ovorni.{1,4} naknadno uključ.{0,50}[/)]|[/(].{0,50}nije snimljen.{0,3}[/)])"""},
        {"Incident_action": r"""([/(]Intoniranje himne[/)]|[/(]INTONIRANJE HIMNE[/)]|[/(]POLAGANJE SVEČANE ZAKLETVE[/)]|[/(]MINU.A ŠUTNJE[/)]|[/(].{0,50}Kolegij.[/)]|[/(].{0,30}diskusija.{0,20}[/)])"""},
        {"Note_time": r"""([/(].{0,10}sednic.{0,20}[/)]|[/(].{0,10}pauz.{0,10}[/)])"""},
        {"Incident_break": r"""([/(]PAUZA[/)]|[/(][Čč]eka se.{0,100}[/)]|[/(][čČ]ekanje.{0,100}[/)]|[/(].auza[/)]|[/(].obacivanje.{0,100}[/)])"""},
        {"Vocal_interruption":r"""([/(][[U|u]padica.{0,100}[/)]|[/(].{0,30} upozor.{0,10}vrijeme.{0,10}[/)]|[/(].{0,100} replik.{0,20}[/)])"""},
        {"Vocal_murmur":r"""([/(].{0,30}[žŽ]agor.{0,30}[/)])"""},
        {"Kinesic_applause":r"""([/(].{0,10}plau.{0,10}[/)]|[/(]APLAUZ[/)]|[/(][pP]ljesak.[/)])"""},
    
    ]
    text_list = [full_text]
    for separator in separators:
        new_text_list = []  
        name = list(separator.keys())[0]
        pattern = separator[name]
        for i, segment in enumerate(text_list):
            if isinstance(segment, list):
                new_text_list.append(segment)
                continue
            chunks = [i for i in re.split(pattern,segment) if i!= ""]
            if len(chunks) == 1:
                new_text_list.extend(chunks)
                continue
            if len(chunks) % 2 == 0:
                pass #raise RuntimeError(f"Len chunks is divisible by 2, inspect!")
            for j, c in enumerate(chunks):
                if j % 2 == 1:
                    print(c, name)
                    new_text_list.append([name, c])
                else:
                    new_text_list.append(c)
        text_list = new_text_list
    return new_text_list

# extracted = extract_remarks("Dobar dan. /Aplauz/ Danes so bile volitve. /žagor/Potem sem jedel makarone. /Aplauz/ Sonja mi je dala fanto /žagor/")  
# for i in extracted:
#     print(i)

c = fromstring(content)
us = c.findall(".//u")

firstu = us[26]

for firstu in us:
    segs = firstu.findall("./seg")
    full_text = " ".join(
    seg.text for seg in segs
    )
    extracted = extract_remarks(full_text)
    # if not len(extracted) == 1:
    #     for i in extracted:
    #         if isinstance(i, str):
    #             print(i[:40], "...", i[-40:])
    #         else:
    #             print(i)
