var s = new sigma({
    renderer: {
        container: document.getElementById('container'),
        type: 'canvas'
    },
    settings: {
        minArrowSize: 10,
        enableEdgeHovering: true,
        edgeHoverSizeRatio: 2,
        // defaultEdgeColor: "#ff0000"
    }
});

sigma.parsers.json(
    'graph.json',
    s,
    function () {
        s.refresh();
    }
);

// s.startForceAtlas2();