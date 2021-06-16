var links = [];
var xpath = "changed_xpath"
$x(xpath).forEach(function(data) {
        links.push(data.href);
});
console.log(links);
