var nodes = [
    {
        "id": 1,
        "label": "AI systems",
        "title": "Type: System<br>Tail: natural persons<br>Centrality: 0.000",
        "value": 0,
        "group": "System",
        "x": 0,
        "y": 0
    },
    {
        "id": 2,
        "label": "evaluate",
        "title": "Type: Action<br>Tail: <br>Centrality: 0.000",
        "value": 0,
        "group": "Action",
        "x": 0,
        "y": 0
    },
    {
        "id": 3,
        "label": "natural persons",
        "title": "Type: Person<br>Tail: AI systems, characteristics<br>Centrality: 0.000",
        "value": 0,
        "group": "Person",
        "x": 0,
        "y": 0
    },
    {
        "id": 4,
        "label": "characteristics",
        "title": "Type: Ethics<br>Tail: <br>Centrality: 0.000",
        "value": 0,
        "group": "Ethics",
        "x": 0,
        "y": 0
    },
    {
        "id": 5,
        "label": "AI systems",
        "title": "Type: System<br>Tail: natural persons<br>Centrality: 0.000",
        "value": 0,
        "group": "System",
        "x": 0,
        "y": 0
    },
    {
        "id": 6,
        "label": "natural persons",
        "title": "Type: Person<br>Tail: AI systems<br>Centrality: 0.000",
        "value": 0,
        "group": "Person",
        "x": 0,
        "y": 0
    }
];

var edges = [
    {
        "from": 1,
        "to": 3,
        "label": "interact with"
    },
    {
        "from": 3,
        "to": 1,
        "label": "interact with"
    },
    {
        "from": 3,
        "to": 4,
        "label": "contains"
    },
    {
        "from": 5,
        "to": 6,
        "label": "has implications for"
    },
    {
        "from": 6,
        "to": 5,
        "label": "is affected by"
    }
];