var nodes = [
    {
        "id": 1,
        "label": "Regulation",
        "title": "Type: DOC<br>Tail: AI system<br>Centrality: 0.007568083464775972",
        "value": 0.3236118737247383,
        "group": "DOC",
        "x": 18,
        "y": 16
    },
    {
        "id": 2,
        "label": "AI system",
        "title": "Type: SYS<br>Head: Regulation<br>Tail: legal certainty<br>Centrality: 0.004767488389108175",
        "value": 0.32510767310166944,
        "group": "SYS",
        "x": -97,
        "y": -86
    },
    {
        "id": 3,
        "label": "international organisations",
        "title": "Type: ORG<br>Tail: artificial intelligence<br>Centrality: 0.0031829575871720607",
        "value": 0.18501055280119472,
        "group": "ORG",
        "x": 74,
        "y": 95
    },
    {
        "id": 4,
        "label": "artificial intelligence",
        "title": "Type: ALG<br>Head: international organisations<br>",
        "value": 0.9101601740797578,
        "group": "ALG",
        "x": -34,
        "y": -37
    },
    {
        "id": 5,
        "label": "legal certainty",
        "title": "Type: ETH<br>Head: AI system<br>",
        "value": 0.7309965722951413,
        "group": "ETH",
        "x": -81,
        "y": -36
    }
];

var edges = [
    {
        "from": 1,
        "to": 2,
        "label": "governs_or_guides"
    },
    {
        "from": 3,
        "to": 4,
        "label": "works_with"
    },
    {
        "from": 2,
        "to": 5,
        "label": "consider"
    }
];