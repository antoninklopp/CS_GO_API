import hltvapi as hltv
import pandas as pd

if __name__ == "__main__":
    upcoming = hltv.upcomingmatches(2)
    for t1, t2 in zip(upcoming["teamnames1"], upcoming["teamnames2"]):
        print(t1, "vs", t2)

    hltv.results()