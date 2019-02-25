# DB_SortMergeJoin
This app is an join simulator. There are implemented SortMergeJoin and NestedLoopJoin (base version and block-optimized). 
A main goal is making experiments. Simulator measures disk accesses that needs
to compute join result with some environment settings like buffer size or expected selectivity.     

### Quick start
Example experiment is located in collect_data.py. Script uses mainly Experiment class which configures join implementation, collects data and dumps it to output dir in csv format.

```bash
python3 collect_data.py
```

### How to run tests
Be careful with py-cache!
```bash
python3 -m unittest discover -v -p "*Test.py"
```
Above command run all tests that match pattern. TestCases named "*TestUnused.py" are disabled from that because are very slow.

### To do
- shared buffer between two relations(tables), now simulator uses dedicated memory space for each table
- some performance improvements
- translations of debug messages to english
