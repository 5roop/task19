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

def extract_remarks(full_text: str) -> list:
    """Extracts remarks from full text.
    
    Returns list like [spoken text:str, ['gap_inaudible', raw text in the remark:str], spoken text:str...]

    Args:
        full_text (str): input text

    Returns:
        list: list of segments (either spoken text:str or remarks:list[str, str])
    """    
    import re
    separators = [
        {"Gap_inaudible": r"""([/(][^/()]{0,100}[nN]e razumije[^/()]{0,50}[/)]|[/(][^/()]{0,100}[nN]e čuj[^/()]{0,50}[/)]|[/(].{0,50}[iI]sključen mikrofon[^/()]{0,2}[/)]|[/(][nN]ije uključen mikrofon.{0,1}[/)]|[/(][^/()]{0,30}[gG]ovorni[^/()]{1,4} naknadno uključ[^/()]{0,50}[/)]|[/(][^/()]{0,100}nije snimljen[^/()]{0,3}[/)]|[/(][^/()]{0,100}nema prijevoda[^/()]{0,30}[/)]|[/(][^/()]{0,100}nema preklopa[^/()]{0,30}[/)]|[/(][^/()]{0,50}isključenje[^/()]{0,2}[/)]|[/(][^/()]{0,50}nije izaš[^/()]{0,5} za govornicu[^/()]{0,2}[/)]|[/(][^/()]{0,30}[nN]ismo dobili tekst[^/()]{0,30}[/)]|[/(][^/()]{0,50}nije uključen[^/()]{0,50}[/)]|[/(][^/()]{0,10}[gG]ovori s mjesta[^/()]{0,10}[/)])"""},
        {"Incident_action": r"""([/(][iI]ntoniranje himne[/)]|[/(]INTONIRANJE HIMNE[/)]|[/(][^/()]{0,100}[iI]zvođavanje himne[^/()]{0,100}[/)]|[/(]POLAGANJE SVEČANE ZAKLETVE[/)]|[/(][^/()]{0,30}ZAKLET[^/()]{0,50}[/)]|[/(]MINU.A ŠUTNJE[/)]|[/(][Mm]inuta šutnje[/)]|[/(][^/()]{0,50}Kolegij[^/()][/)]|[/(][^/()]{0,30}diskusija[^/()]{0,20}[/)]|[/(][dD]avanje svečane izjave[/)]|[/(]Čitanje svečane izjave[/)])"""},
        {"Note_time": r"""([/(][^/()]{0,10}sednic[^/()]{0,20}[/)]|[/(][^/()]{0,50}pauz[^/()]{0,50}[/)]|[/(][^/()]{0,30}STANK[^/()]{0,50}[/)]|[/(][^/()][Ss][ej]{1,2}dnica je završena[^/()]{0,50}[/)]|[/(][^/()][sS][ej]{1,2}dnica je počela[^/()]{0,50}[/)]|NASTAVAK NAKON STANKE U.{0,10}SATI)"""}, 
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
            for j, c in enumerate(chunks):
                if re.search(pattern, c) is not None:
                    # print(c, "\t"+name)
                    new_text_list.append([name, c.strip()])
                else:
                    new_text_list.append(c.strip())
        text_list = new_text_list
    return new_text_list

def fix_component(file: Union[str,Path],
                  out_file: Union[str,Path]):
    if isinstance(file, Path):
        assert file.exists(), f"File {file} existn't!"
        file = str(file)
    
        
    from parse import compile
    pattern = '''{beginning}<body>{body}</body>{ending}'''
    pattern = compile(pattern)

    with open(file) as f:
        content = f.read()
    parsing_results = pattern.search(content).named
    div = fromstring(parsing_results["body"])
    us = div.findall("u")
    us = fix_us(us)
    # us = [Element("test")]
    div = Element("div")
    div.set("type", "debateSection")
    for i in us:
        div.append(i)
    div_str = pretty_string(div)
    div_str = div_str.replace('<?xml version="1.0" ?>', '').replace("\n", "\n\t\t\t")
    
    with open(str(out_file), "w") as f:
        f.write(
            f"""{parsing_results['beginning']}<body>{div_str}</body>{parsing_results['ending']}"""
        )
    
    
def fix_us(us: list):
    returnlist = []
    
    for u in us:
        n = 0
        attribs = u.attrib
        xmlid = attribs['{http://www.w3.org/XML/1998/namespace}id']
        del attribs['{http://www.w3.org/XML/1998/namespace}id']
        attribs["xml:id"] = xmlid
        newu = Element("u")
        newu.attrib = attribs
        segs = u.findall("seg")
        texts = [s.text for s in segs]
        text = " ".join(texts)
        content = extract_remarks(text)
        for c in content:
            if isinstance(c, str):
                seg = SubElement(newu, "seg")
                seg.set("xml:id", xmlid+f".s{n}")
                seg.text = c
                n = n + 1
            if isinstance(c, list):
                # push what we have so far into list:
                returnlist.append(newu)
                # make new elements based on interruption type:
                element = remark_handler(c)
                returnlist.append(element)
                # make new u
                newu = Element("u")
                newu.attrib = attribs
        # Push last element, if needed
        if isinstance(content[-1], str):
            returnlist.append(newu)
    return returnlist
            
def remark_handler(c: list):
    name, text = c[0], c[1]
    if name == "Gap_inaudible":
        gap = Element("gap")
        gap.set("reason", "inaudible")
        desc = SubElement(gap, "desc")
        desc.text = text
        return gap
    elif name.startswith("Incident"):
        incident = Element("incident")
        if "action" in name:
            incident.set("type", "action")
        else:
            incident.set("type", "break")
        desc = SubElement(incident, "desc")
        desc.text = text
        return incident
    elif name.startswith("Vocal"):
        vocal = Element("vocal")
        if "interruption" in name:
            vocal.set("type", "interruption")
        else:
            vocal.set("type", "murmur")
        desc = SubElement(vocal, "desc")
        desc.text = text
        return vocal
    elif name.startswith("Kinesic"):
        kinesic = Element("kinesic")
        kinesic.set("type", "applause")
        desc = SubElement(kinesic, "desc")
        desc.text = text
        return kinesic
    else:
        assert name == "Note_time"
        note = Element("note")
        note.set("type", "time")
        note.text = text
        return note
    
