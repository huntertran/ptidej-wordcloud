var s = new sigma({
    renderer: {
        container: document.getElementById('container'),
        type: 'canvas'
    },
    settings: {
        minArrowSize: 10
    }
});

sigma.parsers.json(
    'graph.json',
    s,
    function () {
        s.refresh();
    }
);