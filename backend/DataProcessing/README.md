Data Transformation Pipeline

1. Input: Raw jsonl 
2. spellCheckerV2.py
        Handles spell checks, case correction, removal of random individual letters at the start of some nodes.
3.  mergeNodes.py
        Merges similar nodes
4. dataParser
        Handles node creation and edge creation, handles duplicate nodes, handles duplicate edges.
5. Output: .js file for graph rendering in the front end