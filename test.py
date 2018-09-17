import hltvapi as hltv
import pandas as pd

def test_upcoming():
    upcoming = hltv.upcomingmatches(2)
    for t1, t2 in zip(upcoming["teamnames1"], upcoming["teamnames2"]):
        print(t1, "vs", t2)

def test_results():
    results = hltv.results(20)
    for t1, t2 in zip(results["teamnames1"], results["teamnames2"]):
        print(t1, "vs", t2)

def results_filtered():
    results = hltv.results(50)
    for t1, t2 in zip(results["teamnames1"], results["teamnames2"]):
        print(t1, "vs", t2)
    results = results[(results.teamnames1 == "G2")]
    print(results)
    for t1, t2 in zip(results["teamnames1"], results["teamnames2"]):
        print(t1, "vs", t2)

if __name__ == "__main__":
    results_filtered()