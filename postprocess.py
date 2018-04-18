import pandas as pd
import re

cc = re.findall("[^\n]+\n+:\n+[^\n]+",bb,flags=re.U)
pd.DataFrame([c.split(":") for c in cc])
