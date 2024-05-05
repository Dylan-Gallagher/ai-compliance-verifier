# Knowledge Graph README

## This directory contains files related to the knowledge graph generated from the AI Act

## `sample_knowledge_graph.png`
Sample human-generated knowledge graph (visual) of the AI Act based on `sample_knowledge_graph_section.txt`.

## `sample_knowledge_graph.txt`
Sample human-generated knowledge graph (text-based) of the AI Act based on `sample_knowledge_graph_section.txt`.

## `sample_knowledge_graph_section.txt`
Section from the AI Act that is used to test NER and RE models.

## `knowledge_graph.html`
HTML file that contains the knowledge graph of the AI Act. It's generated using `rebel_re_model.py`.

## `relations.jsonl`
Relations generated from the relation extraction model in JSONL format (for use with frontend).
Each line is a separate relation, represented with `head`, `type` and `tail`.

## `relations.pkl`
Python Pickle file containing the extracted relations. Used to prevent re-running the model unnecessarily.