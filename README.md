# CS GO API
A cs go api to get matches from hltv website (unofficial api)

The current available features are:
- list of upcoming matches
- list of results

All the results are stored in pandas dataframes, to make it
easier to process this data afterwards.


# Exemple of use

```python
import hltvapi as hltv
import pandas as pd

results = hltv.results(20) # results from the previous 20 days
for t1, t2 in zip(results["teamnames1"], results["teamnames2"]):
  print(t1, "vs", t2) # print all matches names
```

## Thanks to akagna

I started this repository using the code from https://github.com/akagna/HLTV-Match-API as a basis
