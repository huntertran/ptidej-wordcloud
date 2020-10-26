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
    async function () {
        await config();
    }
);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function config() {
    s.refresh();

    // sigma.plugins.relativeSize(s, 5);

    s.startForceAtlas2({
        worker: true,
        barnesHutOptimize: false,
        scalingRatio: 1
    });
    await sleep(3000);
    s.killForceAtlas2();

    var noOverLapListener = s.configNoverlap({
        nodeMargin: 3.0,
        scaleNodes: 1.3
    });
    s.startNoverlap();

    var dragListener = new sigma.plugins.dragNodes(s, s.renderers[0]);
    CustomShapes.init(s);
    s.refresh();
}