// custom node renderer

sigma.utils.pkg('sigma.canvas.nodes');
sigma.canvas.nodes.image = (function () {
    var _cache = {},
        _loading = {},
        _callbacks = {};

    // Return the renderer itself:
    var renderer = function (node, context, settings) {
        var args = arguments,
            prefix = settings('prefix') || '',
            size = node[prefix + 'size'],
            color = node.color || settings('defaultNodeColor'),
            url = node.image.url;
            w = node.image.w;
            h = node.image.h;
            scale = 0.1;

        if (_cache[url]) {
            context.save();

            // // Draw the clipping disc:
            // context.beginPath();
            // context.arc(
            //     node[prefix + 'x'],
            //     node[prefix + 'y'],
            //     node[prefix + 'size'],
            //     0,
            //     Math.PI * 2,
            //     true
            // );
            // context.closePath();
            // context.clip();

            // Draw the image
            context.drawImage(
                _cache[url],
                node[prefix + 'x'] - size,
                node[prefix + 'y'] - size,
                w * scale * size,
                h * scale * size
            );

            // console.log("draw image: W" + w + " | H: " + h + " | Size: " + size)

            // // Quit the "clipping mode":
            // context.restore();

            // // Draw the border:
            // context.beginPath();
            // context.arc(
            //     node[prefix + 'x'],
            //     node[prefix + 'y'],
            //     node[prefix + 'size'],
            //     0,
            //     Math.PI * 2,
            //     true
            // );
            // context.lineWidth = size / 5;
            // context.strokeStyle = node.color || settings('defaultNodeColor');
            // context.stroke();
        } else {
            sigma.canvas.nodes.image.cache(url);
            sigma.canvas.nodes.def.apply(
                sigma.canvas.nodes,
                args
            );
        }
    };

    // Let's add a public method to cache images, to make it possible to
    // preload images before the initial rendering:
    renderer.cache = function (url, callback) {
        if (callback)
            _callbacks[url] = callback;

        if (_loading[url])
            return;

        var img = new Image();

        img.onload = function () {
            _loading[url] = false;
            _cache[url] = img;

            if (_callbacks[url]) {
                _callbacks[url].call(this, img);
                delete _callbacks[url];
            }
        };

        _loading[url] = true;
        img.src = url;
    };

    return renderer;
})();

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function config() {
    // s.refresh();

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
    // CustomShapes.init(s);
    // s.refresh();
}

var s = new sigma({
    renderer: {
        container: document.getElementById('container'),
        type: 'canvas'
    },
    settings: {
        minArrowSize: 10,
        enableEdgeHovering: true,
        edgeHoverSizeRatio: 2,
        zoomMin: 0.001
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