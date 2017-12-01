$(function() {


    // screen搜索
    $('#searchinput').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        // console.log($(e.target));
    });
    $('#searchinput').on('keyup', debouncer(function(e) {
        var $el = $(e.target);
        var val = $el.val();
        // console.log('1', val);
        var screenEls = $el.parent().parent().nextAll();
        _.each(screenEls, function(e) {
            var text = $(e).find('small').text();
            // console.log('2', text);
            var re = new RegExp(val, 'i');
            // if (text.indexOf(val) !== -1) {
            if (re.test(text)) {
                $(e).show();
            } else {
                $(e).hide();
            }
        });
        // console.log('0', '------');
        // console.log('1', val);
    }, 300));

    function debouncer(func, timeout) {
        var timeoutID;
        timeout = timeout || 300;
        return function () {
            var scope = this , args = arguments;
            clearTimeout( timeoutID );
            timeoutID = setTimeout( function () {
                func.apply( scope , Array.prototype.slice.call( args ) );
            }, timeout);
        };
    }

    // 画图
    active();
    window.active = active;
    window.getData = getData;

    function getData(area, url) {
        $.getJSON(url, function(ret) {
            var data = parseData(ret);
            var title = ret.title;

            var $el = $(area).find('.chart-area');
            var $t = $(area).find('.chart-title');
            var $l = $(area).find('.legend');

            var href = $.query.load(window.location.href);
            var showLegend = href.get('legend');

            //if (showLegend && showLegend === 'off') {
            //    $l.hide();
            //}
            $.plot($el, data, getConfig({legend: $l}));
            $t.html(title);

            $el.on('plothover', function (event, pos, item) {
                // console.log('1111');
                if (item) {
                    // console.log('2222');
                    // var x = item.datapoint[0].toFixed(2),
                    var x = moment(item.datapoint[0]).format('YYYY-MM-DD HH:mm:ss'),
                    y = item.datapoint[1].toFixed(2);

                    $('#tooltip').html(item.series.label + '<br>' + x + '<br>' + y)
                    .css({top: item.pageY+5, left: item.pageX+5})
                    .fadeIn(200);
                    // console.log('3333');
                } else {
                    $('#tooltip').hide();
                }
            });

        });
    }

    function active() {
        var $containers = $('.chart-container');
        var href = $.query.load(window.location.href);
        var showLegend = href.get('legend') || "off";
        window.cacheData = {}; // 数据缓存
        window.cachePlot = {}; // plot缓存

        _.each($containers, function(c, i) {
            var url = $(c).data('u');
            var $el = $(c).find('.chart-area');
            var $t = $(c).find('.chart-title');
            var $l = $(c).find('.legend');
            $.getJSON(url, function(ret) {
                var data = parseData(ret);
                var title = ret.title;
                window.cacheData[i] = $.extend(true, [], data);

                if (showLegend && showLegend === 'off') {
                    $l.hide();
                }
                cachePlot[i] = {};
                var flot = $.plot($el, data, getConfig({legend: $l}));
                cachePlot[i].plot = flot;
                cachePlot[i].$el = $el;
                cachePlot[i].$l = $l;
                $t.html(title);

                $el.on('plothover', function (event, pos, item) {
                    // console.log('1111');
                    if (item) {
                        // console.log('2222');
                        // var x = item.datapoint[0].toFixed(2),
                        var x = moment(item.datapoint[0]).format('YYYY-MM-DD HH:mm:ss'),
                        y = formatSizeOrigin(item.datapoint[1], "si", 3)

                        $('#tooltip').html(item.series.label + '<br>' + x + '<br>' + y)
                        .css({top: item.pageY+5, left: item.pageX+5})
                        .fadeIn(200);
                        // console.log('3333');
                    } else {
                        $('#tooltip').hide();
                    }
                });

                $el.bind("plotselected", function (event, ranges) {
                    // $("#selection").text(ranges.xaxis.from.toFixed(1) + " to " + ranges.xaxis.to.toFixed(1));
                    $.each(flot.getXAxes(), function(_, axis) {
                        var opts = axis.options;
                        opts.min = ranges.xaxis.from;
                        opts.max = ranges.xaxis.to;
                    });
                    flot.setupGrid();
                    flot.draw();
                    flot.clearSelection();
                });

            });
        });
    }

    // reset zoom
    // TODO: 切换求和的时候reset zoom 有问题
    $('body').on('click', '.reset-zoom', function(e) {
        var $el = $(e.target);
        var index = $el.data('index');
        var data = $.extend(true, [], window.cacheData[index]);
        window.cachePlot[index].plot.shutdown();
        $.plot(cachePlot[index].$el, data, getConfig({legend: cachePlot[index].$l}));
    });


    // sort data
    function sortData(data) {
        _.each(data, function(d) {
            d.data = d.data.sort(function(a, b) {
                return a[0] - b[0];
            });
        });
        return data;
    }

    // summary series
    function summary(series) {
        var d = series.data;

        // 去掉值中的null
        d = _.filter(d, function(i) {
            return i[1] !== null;
        });

        // 这里的数据结构是 [timestamp, value]
        var last = d[d.length-1][1];
        var max = _.max(d, function(i) {return i[1]})[1];
        var min = _.min(d, function(i) {return i[1]})[1]
        var sum = sum = _.reduce(d, function(memo, i) {return memo + i[1]}, 0);
        var avg = (sum/d.length);
        var sorted = d.sort(function(a,b) {return a[1]-b[1]});
        var th95 = sorted[parseInt(d.length*0.95, 10)][1];
        var th99 = sorted[parseInt(d.length*0.99, 10)][1];

        return {
            last: last,
            max: max,
            min: min,
            sum: sum,
            avg: avg,
            th95: th95,
            th99: th99
        };
    }

    // parse return data
    function parseData(ret) {
        var data = [];
        var len = ret.series.length;
        for (var i = 0, l = len; i < l; i ++) {
            var v = ret.series[i];
            data.push({label: v.name, data: v.data, check: true});
        }
        return data;
    }

    // flot config
    function getConfig(options) {
        return {
            lines: {
                show: true
            },
            points: {
                show: true,
                radius: 0.2,
                lineWidth: 1,
                fill:true,
                fillColor: "rgba(215, 234, 252, 0.8)"
            },
            xaxis: {
                mode: 'time',
                timezone: 'browser',
                color: "#EAEAEA",
                font: {
                  size: 10,
                  weight: "bold",
                  color: "#ACABAB",
                  family: "sans-serif",
                  variant: "small-caps"
                }
                //tickDecimals: 0,
                //tickSize: 1
            },
            series: {
                shadowSize: 0   // Drawing is faster without shadows
            },
            // 使用深色色彩可选值, 避免因为绘图线条颜色太浅看不清楚
            colors:  [
                "#FF6A6A", "#00BFFF", "#A52A2A",
                "#CDCD00", "#008878", "#FF0000",
                "#00FF00", "#7B68EE", "#FF00FF",
                "#EEAEEE", "#00AEEE", "#AEEEEE",

                "#FFB90F", "#00B90F", "#00FFFF",
                "#DC143C", "#BFEFFF", "#AA7500",
                "#F0E68C", "#00E68C", "#AAE68C",
                "#EE9A49", "#009A49", "#AA9A49",

                "#FFA54F", "#00A54F", "#AAA54F",
                "#8B4789", "#004789", "#AA4789",
                "#00CDCD", "#00CDCD", "#AACDCD",
                "#EE8262", "#008262", "#AA8262",

                "#FF8C00", "#008C00", "#AA8C00",
                "#8B3626", "#003626", "#AA3626",
                "#00BFFF", "#00E8AA", "#AAE8AA",
                "#EE7621", "#007621", "#AA7621",
                ],
            yaxis: {
                // min: -1
                // max: 100
                color: "#EAEAEA",
                font: {
                  size: 10,
                  weight: "bold",
                  color: "#ACABAB",
                  family: "sans-serif",
                  variant: "small-caps"
                }
            },
            selection: {
                mode: "x"
            },
            grid: {
                hoverable: true,
                clickable: true,
                borderWidth: 0.5,
                borderColor: "#EAEAEA"
            },
            legend: {
                show: true,
                // position: 'nw',
                container: options.legend,
                labelFormatter: function(label, series) {
                    return label;
                    // return label + '<input type='checkbox' value='' + label + ''>';
                    // return null;
                }
            }
        }
    }
});
