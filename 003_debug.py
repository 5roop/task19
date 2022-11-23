import os
from pathlib import Path
from utils import fix_component

f = "/home/rupnik/parlamint/S_3/ParlaMint-HR_T05_S11.xml"
fout = "./003_test.xml"
fix_component(f, fout)