var wordcloud = {
    data: 'data/graph.json',
    s: undefined,
    reviewStatus: 0,
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
        let w = node.image.w;
        let h = node.image.h;
        let scale = 0.1;

        if (wordcloud.rendererArgs._cache[url]) {
            context.save();

            // Draw the image
            context.drawImage(
                wordcloud.rendererArgs._cache[url],
                node[prefix + 'x'] - size,
                node[prefix + 'y'] - size,
                w * scale * size,
                h * scale * size
            );
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
        await wordcloud.sleep(1000);
        // another refresh to show the word-cloud
        wordcloud.s.refresh();

        wordcloud.addNodeEvent();
    },

    addButtonClickEvent: function () {
        let feedbackBtn = document.getElementById('feedback_btn');
        feedbackBtn.onclick = this.feedbackClicked;

        let closeFeedBackBtn = document.getElementById('close_feedback_btn');
        closeFeedBackBtn.onclick = this.closeFeedbackClicked;
    },

    feedbackClicked: function () {
        var toggle_survey_elements = document.getElementsByClassName('toggle_survey');
        for (element of toggle_survey_elements) {
            element.classList.remove('survey_close');
            element.classList.add('survey_open');
        }

        if (window.innerWidth <= 1024) {
            window.scrollTo(0, document.body.scrollHeight);
        }
    },

    // addEventHandlers: function(){
    //     document.getElementById("container").addEventListener("mousewheel DOMMouseScroll", wordcloud.mouseWheel);
    //     wordcloud.s.bind('coordinatesUpdated', wordcloud.coordinateUpdatedEventHandler);
    // },

    // mouseWheel: function(){
    //     console.log(wordcloud.s.camera);
    // },

    // coordinateUpdatedEventHandler: function(event) {
    //     console.log(event);
    // },

    addNodeEvent: function () {
        wordcloud.s.bind('clickNode', wordcloud.clickNodeEventHandler);
        let close_fullsize_image_button = document.getElementById('close-fullsize-image-button');
        close_fullsize_image_button.onclick = wordcloud.closeFullSizeImageButtonClicked;
    },

    getImageUrl: function (node) {
        var image_url = node.data.node.image.url;
        return image_url.replace('thumbnails', 'fullsize');
    },

    setFullsizeImageForReview: function (image_url, element_id) {
        var fullsize_image = document.getElementById(element_id);
        fullsize_image.setAttribute('src', image_url);
    },

    clickNodeEventHandler: function (node) {
        var image_url = wordcloud.getImageUrl(node);

        switch (wordcloud.reviewStatus) {
            case 1:
                // image 1 showed
                wordcloud.setFullsizeImageForReview(image_url, 'selected-wordcloud-2');
                wordcloud.reviewStatus = 2;
                break;
            default:
                // nothing showed
                // OR
                // both images showed
                wordcloud.setFullsizeImageForReview(image_url, 'selected-wordcloud');
                wordcloud.reviewStatus = 1;
                break;
        }

        let wordcloud_fullsize = document.getElementById('wordcloud-fullsize');
        wordcloud_fullsize.setAttribute('class', 'show');
    },

    closeFullSizeImageButtonClicked: function () {
        let wordcloud_fullsize = document.getElementById('wordcloud-fullsize');
        wordcloud_fullsize.setAttribute('class', 'hide');
    },

    closeFeedbackClicked: function () {
        var toggle_survey_elements = document.getElementsByClassName('toggle_survey');
        for (element of toggle_survey_elements) {
            element.classList.add('survey_close');
            element.classList.remove('survey_open');
        }
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
                zoomMin: 0.1
            }
        });

        sigma.parsers.json(
            wordcloud.data,
            wordcloud.s,
            async function () {
                // wordcloud.s.bind('coordinatesUpdated', wordcloud.coordinateUpdatedEventHandler);
                wordcloud.s.refresh();
                await wordcloud.config();
            }
        );

        wordcloud.addButtonClickEvent();
        // wordcloud.addEventHandlers();
    }
}

wordcloud.init();