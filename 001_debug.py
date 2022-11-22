test_file = "../SRB/S/ParlaMint-RS_T08S3.xml"
test_file = "../S/ParlaMint-HR_T09_S01.xml"
test_file = "../BiH/S/ParlaMint-BA_T02S03.xml"
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
        {"Gap_inaudible": r"""([/(][^/()]{0,100}[nN]e razumije[^/()]{0,50}[/)]|[/(][^/()]{0,100}[nN]e čuj[^/()]{0,50}[/)]|[/(].{0,50}[iI]sključen mikrofon[^/()]{0,2}[/)]|[/(][nN]ije uključen mikrofon.{0,1}[/)]|[/(][^/()]{0,30}[gG]ovorni[^/()]{1,4} naknadno uključ[^/()]{0,50}[/)]|[/(][^/()]{0,100}nije snimljen[^/()]{0,3}[/)]|[/(][^/()]{0,100}nema prijevoda[^/()]{0,30}[/)]|[/(][^/()]{0,100}nema preklopa[^/()]{0,30}[/)]|[/(][^/()]{0,50}isključenje[^/()]{0,2}[/)]|[/(][^/()]{0,50}nije izaš[^/()]{0,5} za govornicu[^/()]{0,2}[/)]|[/(][^/()]{0,30}[nN]ismo dobili tekst[^/()]{0,30}[/)])"""},
        {"Incident_action": r"""([/(][iI]ntoniranje himne[/)]|[/(]INTONIRANJE HIMNE[/)]|[/(][^/()]{0,100}[iI]zvođavanje himne[^/()]{0,100}[/)]|[/(]POLAGANJE SVEČANE ZAKLETVE[/)]|[/(][^/()]{0,30}ZAKLET[^/()]{0,50}[/)]|[/(]MINU.A ŠUTNJE[/)]|[/(][Mm]inuta šutnje[/)]|[/(][^/()]{0,50}Kolegij[^/()][/)]|[/(][^/()]{0,30}diskusija[^/()]{0,20}[/)]|[/(][dD]avanje svečane izjave[/)]|[/(]Čitanje svečane izjave[/)])"""},
        {"Note_time": r"""([/(][^/()]{0,10}sednic[^/()]{0,20}[/)]|[/(][^/()]{0,50}pauz[^/()]{0,50}[/)]|[/(][^/()]{0,30}STANK[^/()]{0,50}[/)]|[/(][^/()][Ss][ej]{1,2}dnica je završena[^/()]{0,50}[/)]|[/(][^/()][sS][ej]{1,2}dnica je počela[^/()]{0,50}[/)])"""},
        {"Incident_break": r"""([/(]PAUZA[/)]|[/(][Čč]eka se[^/()]{0,100}[/)]|[/(][čČ]ekanje.{0,100}[/)]|[/(].{0,3}auza.{0,3}[/)]|[/(][sS][je]{1,2}dnica [^/()]{0,10}prekinuta[^/()]{0,50}[/)])"""},
        {"Vocal_interruption":r"""([/(][[U|u]padic[ae][^/()]{0,200}[/)]|[/(][^/()]{0,30} upozor.{0,10}vrijeme[^/()]{0,50}[/)]|[/(][^/()]{0,50} replik[^/()]{0,50}[/)]|[/(].obacivanje[^/()]{0,100}[/)]|[/(][^/()]{0,30}s[a]{0,1} mjesta[^/()]{0,100}[/)]|[/(][^/()]{0,30}[iI]z klupe[^/()]{0,100}[/)])"""},
        {"Vocal_murmur":r"""([/(][^)]{0,50}[žŽ]a[mg]or[^/()]{0,50}[/)])"""},
        {"Kinesic_applause":r"""([/(][^/()]{0,30}plau[^/()]{0,30}[/)]|[/(]APLAUZ[/)]|[/(][pP]ljesak.[/)])"""},
    
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
                if re.search(pattern, c) is not None:
                    import sys
                    print(c, "\t"+name, 
                          file=sys.stdout
                           )
                    new_text_list.append([name, c.strip()])
                else:
                    new_text_list.append(c.strip())
        text_list = new_text_list
    return new_text_list


c = fromstring(content)
us = c.findall(".//u")



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
