
angular.module('app', ['ui.bootstrap.datetimepicker', 'app.util'])
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller('MultiCtrl', MultiCtrl)

function MultiCtrl(FlotServ, $scope, $interval, $timeout) {
    var vm = this;

    // 全局的参数
    vm.defaultGlobalParam = {
        start: '',
        end: '',
        cf: 'AVERAGE', // MIN, MAX
        graph_type: 'h', // h Endpoint视角; k Counter视角
        sum: 'off' // off
    };
    vm.globalParam = angular.copy(vm.defaultGlobalParam);


    // var urlH = '/chart/h';
    // var urlK = '/chrt/k;
    var backendParam = FlotServ.getParam(); // 后端渲染出来的参数
    vm.globalParam.graph_type = backendParam.graph_type;

    vm.chart = {}; // 前端的图, 对应后端的返回
    vm.configs = []; // 绘图的数据, 多个
    vm.data = []; // 缓存的绘图数据, 不会改变
    // vm.param = angular.copy(defaultParam);


    vm.all = true; // 是否全选
    vm.reverse = false; // 是否反选

    vm.checkAll = checkAll;
    vm.checkReverse = checkReverse;
    vm.checkSearch = checkSearch;
    vm.reset = reset;
    vm.show = show;

    $scope.$watch('vm.globalParam.graph_type', function(newVal, oldVal) {
        if (newVal !== oldVal) {
            // change url
            var url = window.location.href;
            var newUrl;
            if (newVal === 'k') {
                newUrl = url.replace('graph_type=h', 'graph_type=k').replace('graph_type=a', 'graph_type=k');
            } else if (newVal === 'h') {
                newUrl = url.replace('graph_type=k', 'graph_type=h').replace('graph_type=a', 'graph_type=h');
            } else {
                newUrl = url.replace('graph_type=h', 'graph_type=a').replace('graph_type=k', 'graph_type=a');
            }
            window.location.href = newUrl;
        }
    });

    active(vm.globalParam);

    // reset 重置
    function reset() {
        vm.globalParam = angular.copy(vm.defaultGlobalParam);
    }

    // show 看图
    function show() {
        active(vm.globalParam);
    }

    // active
    function active(param) {
        // console.log(FlotServ.getUrls());
        var p = angular.copy(param);
        if (angular.isDate(p.start)) {
            p.start = +p.start/1000;
        }
        if (angular.isDate(p.end)) {
            p.end = +p.end/1000;
        }
        FlotServ.getMultiDataById(p).then(function(ret) {
            // [{data: {}}, {data: {}}, {data: {}}]
            // console.log(ret);
            var data;
            data = _.map(ret, function(i) {
                var o = {};
                o.config = FlotServ.parseData(i.data);
                o.title = i.data.title;
                return o;
            });
            // console.log(data);
            vm.configs = data;
        });
    }

    // 全选
    function checkAll() {
        if (vm.all) {
            _.each(vm.data, function(d) {
                d.check = true;
            });
        } else {
            _.each(vm.data, function(d) {
                d.check = false;
            });
        }
        // vm.config = vm.data;
    }


    // 反选
    function checkReverse () {
        if (vm.reverse) {
            vm.all = false;
            _.each(vm.data, function(d) {
                d.check = !d.check;
            });
        }
        // vm.config = vm.data;
    }

    // 确定
    function checkSearch() {
        var data2 = [];
        _.each(vm.data, function(d) {
            if (d.check) {
                data2.push(d);
            }
        });
        vm.config = data2;
        // vm.series = data2;
        // flot = $.plot(el, val, FlotServ.getConfig());
    }


}
