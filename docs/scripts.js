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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// sigma.plugins.relativeSize(s, 1);

sigma.parsers.json(
    'graph.json',
    s,
    async function () {
        s.refresh();
        s.startForceAtlas2({
            worker: true,
            barnesHutOptimize: false,
            scalingRatio: 1
        });
        await sleep(3000);
        s.killForceAtlas2();
    }
);

// window.setTimeout(function () { s.killForceAtlas2() }, 5000);