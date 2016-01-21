angular.module('app.util', [])
.service('FlotServ', FlotServ)
.directive('myFlot', myFlot)
.directive('ngEnter', ngEnter)
.filter('formatSize', formatSize);

function formatSize() {
    return function(input, standard) {
        input = input;

        var size = parseFloat(input);
        if (standard) {
            standard = standard.toLowerCase();
        }
        if(size <= 1){
            return size.toFixed(3);
        }

        var n = 0,
        base = standard == 'si' ? 1000 : 1024,
        prefixes = ' KMGTPEZY';

        if (size >= base) {
            n = Math.floor( Math.log(size) / Math.log(base) );

            if (n >= prefixes.length) {
                return 'N/A';
            }

            size = ( size / Math.pow(base, n) ).toFixed(3) * 1 + '';
        }else{
            size = size.toFixed(3)
        }

        return size + prefixes[n] + ( n && standard == 'iec' ? 'i' : '' ) + '';
    };
}

function myFlot(FlotServ) {
    var link = function($scope, $element, $attrs) {
        // 这里的值是异步的, 刚开始是空的, 需要watch一下
        var flot;
        var loadingIcon = $('#loading-container');
        loadingIcon.show();
        var type = $attrs.type; // s: 小图模式, b: 大图模式
        var el;
        if (type === 's') {
            el = $element.find('.chart-container-multi');
        } else if (type === 'b') {
            el = $element.find('.chart-container-big');
        }
        el.html('<span class="loading">载入中</span>');
        var legendContainer = $element.find('.legend');
        var data;
        var dataBak;
        $scope.$watch('config', function(val) {
            if (val && val.length) {
                // 这里的 数据需要排序, 貌似angular把这里的顺序弄乱了
                data = FlotServ.sortData(val);
                dataBak = angular.copy(data);
                // console.log('1', JSON.stringify(data));
                // 如果这里面有sum的话, 设置 stack 为true
                // laiwei:暂时不用stack
                // var stack = _.some(data, function(d) {
                //     return d.label === 'sum';
                // });
                var stack = false;
                flot = $.plot(el, data, FlotServ.getConfig({legend: legendContainer, stack: stack}));
            }
            loadingIcon.hide();
            el.find('.loading').remove();
        });

        $element.parents().find('.reset-zoom').on('click', function(e) {
            flot.shutdown();
            loadingIcon.show();
            var data = angular.copy(dataBak); // copy一份, 重新渲染
            // console.log('2', JSON.stringify(data));
            // 如果这里面有sum的话, 设置 stack 为true
            // laiwei:暂时不用stack
            // var stack = _.some(data, function(d) {
            //     return d.label === 'sum';
            // });
            var stack = false;
            flot = $.plot(el, data, FlotServ.getConfig({legend: legendContainer, stack: stack}));
            loadingIcon.hide();
        });

        // watch新添加的数据
        $scope.$watch('newdata', function(val) {
            if (val && val.length) {
                val = FlotServ.sortData(val);
                // console.log('2', JSON.stringify(val));
                // 在这里把新的数据拼到旧数据里
                // 例: 旧的数据 [1,2,3], 新数据 [2,3,4] [1,2,3]等
                // console.log('2', data);
                for (var si in data) {
                    // 这里顺序又乱了... 为什么...
                    var series = data[si];
                    series = FlotServ.sortData([data[si]])[0];
                    // console.log('2.5', JSON.stringify(series));
                    var last = series.data[series.data.length-1][0];
                    // console.log('3', last);

                    for (var di in val) {
                        var label = val[di].label;
                        var d = val[di].data;
                        if (series.label === label) {
                            for (var idx in d) {
                                if (d[idx][0] > last) {
                                    data[si].data.push(d[idx]);
                                }
                            }
                        }
                    }
                }
                // console.log('3', data);
                flot.setData(data);
                flot.draw();
            }
        });



        el.on('plothover', function (event, pos, item) {
            // console.log('1111');
            if (item) {
                // console.log('2222');
                // var x = item.datapoint[0].toFixed(2),
                var x = moment(item.datapoint[0]).format('YYYY-MM-DD HH:mm:ss'),
                y = item.datapoint[1].toFixed(3);

                $('#tooltip').html(item.series.label + '<br>' + x + '<br>' + y)
                .css({top: item.pageY+5, left: item.pageX+5})
                .fadeIn(200);
                // console.log('3333');
            } else {
                $('#tooltip').hide();
            }
        });

        el.bind("plotselected", function (event, ranges) {
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



    };
    return {
        link: link,
        restrict: 'A',
        scope: {
            config: '=',
            newdata: '='
        }
    };
}

function ngEnter() {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });
                event.preventDefault();
            }
        });
    };
}

function FlotServ($http, $window, $q) {
    var self = this;

    // flot config
    self.getConfig = function(options) {
        return {
            stack: options.stack || false,
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
            lines: {
                show: true
            },
            points: {
                show: true,
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
                // tickDecimals: 0,
                // tickSize: 1
            },
            series: {
                shadowSize: 0   // Drawing is faster without shadows
            },
            yaxis: {
                // min: 0
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
            grid: {
                hoverable: true,
                clickable: true,
                borderWidth: 0.5,
                borderColor: "#EAEAEA"
            },
            selection: {
                mode: "x"
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
    };

    // send ajax
    self.getData = function(url, params) {
        return $http({method: 'GET', url: url, params: params});
    };

    // 首次请求的参数
    self.getParam = function() {
        return $window.obj;
    };

    // 后续请求的参数, 定时的那个
    self.getParam2 = function() {
        return $window.obj2;
    };

    // 数据url
    self.getUrls = function() {
        return $window.urls;
    };

    // 多图时, 每个图的id
    self.getIds = function() {
        return $window.ids;
    };

    self.getMultiDataById = function(param) {
        var ids = self.getIds();
        var reqs = _.map(ids, function(id) {
            var p = angular.copy(param);
            if (angular.isDate(p.start_s)) {
                p.start_s = +p.start_s/1000;
            }
            if (angular.isDate(p.end_s)) {
                p.end_s = +p.end_s/1000;
            }
            p.id = id;
            return $http({method: 'GET', url: '/chart/' + p.graph_type, params: p});
        });
        return $q.all(reqs);
    };

    // 数据请求
    self.getMultiData = function() {
       var urls = self.getUrls();
       var reqs = _.map(urls, function(u) {
           return $http({method: 'GET', url: u});
       });
       return $q.all(reqs);
    };


    // parse response data
    self.parseData = function(ret) {
        var data = [];
        var len = ret.series.length;
        for (var i = 0, l = len; i < l; i ++) {
            var v = ret.series[i];
            data.push({label: v.name, data: v.data, check: true});
            // if (v.name === 'sum') {
            //     data.push({label: v.name, data: v.data, check: true, lines: {fill: true}});
            // } else {
            //     data.push({label: v.name, data: v.data, check: true});
            // }
        }
        return data;
    };

    // get max, min, avg, sum
    self.summary = function(series) {
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
    };

    // sort data by timestamp
    self.sortData = function(data) {
        _.each(data, function(d) {
            d.data = d.data.sort(function(a, b) {
                return a[0] - b[0];
            });
        });
        return data;
    };
}
