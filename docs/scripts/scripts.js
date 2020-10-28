var wordcloud = {
    data: 'data/graph.json',
    s: undefined,
    rendererArgs: {
        _cache: {},
        _loading: {},
        _callbacks: {}
    },

    renderer: function (node, context, settings) {
        var args = arguments,
            prefix = settings('prefix') || '',
            size = node[prefix + 'size'],
            color = node.color || settings('defaultNodeColor'),
            url = node.image.url;
        w = node.image.w;
        h = node.image.h;
        scale = 0.1;

        if (wordcloud.rendererArgs._cache[url]) {
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
                wordcloud.rendererArgs._cache[url],
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
    },

    rendererCache: function (url, callback) {
        if (callback)
            wordcloud.rendererArgs._callbacks[url] = callback;

        if (wordcloud.rendererArgs._loading[url])
            return;

        var img = new Image();

        img.onload = function () {
            wordcloud.rendererArgs._loading[url] = false;
            wordcloud.rendererArgs._cache[url] = img;

            if (wordcloud.rendererArgs._callbacks[url]) {
                wordcloud.rendererArgs._callbacks[url].call(this, img);
                delete wordcloud.rendererArgs._callbacks[url];
            }
        };

        wordcloud.rendererArgs._loading[url] = true;
        img.src = url;
    },

    customRender: function () {
        // custom node renderer

        sigma.utils.pkg('sigma.canvas.nodes');
        sigma.canvas.nodes.image = (function () {
            // Let's add a public method to cache images, to make it possible to
            // preload images before the initial rendering:
            wordcloud.renderer.cache = wordcloud.rendererCache;

            return wordcloud.renderer;
        })();
    },

    sleep: function (ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    config: async function () {
        // s.refresh();

        // sigma.plugins.relativeSize(s, 5);

        wordcloud.s.startForceAtlas2({
            worker: true,
            barnesHutOptimize: false,
            scalingRatio: 1
        });
        await wordcloud.sleep(3000);
        wordcloud.s.killForceAtlas2();

        var noOverLapListener = wordcloud.s.configNoverlap({
            nodeMargin: 3.0,
            scaleNodes: 1.3
        });
        wordcloud.s.startNoverlap();

        var dragListener = new sigma.plugins.dragNodes(wordcloud.s, wordcloud.s.renderers[0]);
        // CustomShapes.init(s);
        // s.refresh();
    },

    addButtonClickEvent: function () {
        feedbackBtn = document.getElementById('feedback_btn');
        feedbackBtn.onclick = this.feedbackClicked;

        closeFeedBackBtn = document.getElementById('close_feedback_btn');
        closeFeedBackBtn.onclick = this.closeFeedbackClicked;
    },

    feedbackClicked: function () {

    },

    closeFeedbackClicked: function () {

    },

    init: function () {
        wordcloud.customRender();

        wordcloud.s = new sigma({
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
            wordcloud.data,
            wordcloud.s,
            async function () {
                await wordcloud.config();
            }
        );
    }
}

wordcloud.init();