import os
from pathlib import Path
from utils import fix_component

f = "/home/rupnik/parlamint/SRB/S/ParlaMint-RS_T12Sv9.xml"
fout = "./003_test.xml"
fix_component(f, fout)