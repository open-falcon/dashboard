
angular.module('app', ['app.util','angular-multi-check'])
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller('BigCtrl', BigCtrl)

function BigCtrl(FlotServ, $scope, $interval, $timeout, $filter) {
    var vm = this;

    var urlH = '/chart/h';
    var defaultParam = FlotServ.getParam();
    var graph_type = defaultParam.graph_type;

    if (graph_type === 'k') {
        urlH = '/chart/k';
    } else if (graph_type === 'a') {
        urlH = '/chart/a';
    }

    vm.chart = {}; // 前端的图, 对应后端的返回
    vm.config = []; // 绘图的数据, 会变化
    vm.data = []; // 缓存的绘图数据, 不会改变
    vm.param = angular.copy(defaultParam);


    vm.all = true; // 是否全选
    vm.reverse = false; // 是否反选

    vm.checkAll = checkAll;
    vm.checkReverse = checkReverse;
    vm.checkSearch = checkSearch;
    vm.reset = reset;
    vm.checkFilter = checkFilter;


    // watch
    $scope.$watch('vm.param', function(newVal, oldVal) {
        if (!angular.equals(newVal, oldVal)) {
            active(newVal);
        }
    }, true);


    active(vm.param);

    // interval

    $interval(function() {
        var rand = Math.round(Math.random() * 1000 * 120); // 0s ~ 120s
        $timeout(function() {
            var p = FlotServ.getParam2();
            p['-'] = Math.random();
            FlotServ.getData(urlH, p).success(function(ret) {
                var d = FlotServ.parseData(ret);
                if (d.length > 0) {
                    vm.newdata = FlotServ.parseData(ret);
                }
                // vm.chart = ret;
                // TODO 这里也要重新计算?
                // vm.summary = FlotServ.summary(ret.series[0]);
            });
        }, rand);
    }, 60000);


    // reset
    function reset() {
        vm.param = angular.copy(defaultParam);
    }

    // active
    function active(param) {
        FlotServ.getData(urlH, param).success(function(ret) {
            vm.config = FlotServ.parseData(ret);
            vm.data = FlotServ.parseData(ret);
            vm.chart = ret;
            vm.summary = FlotServ.summary(ret.series[0]);
        });
    }

    function checkFilter() {
        _.each(vm.data, function(d) {
            d.check = false;
        });

        var query = vm.query;
        var checks = $filter('filter')(vm.data, {label:query});
        angular.forEach(checks, function(i) {
            i.check = true;
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
    }


    // 反选
    function checkReverse () {
        if (vm.reverse) {
            vm.all = false;
            _.each(vm.data, function(d) {
                d.check = !d.check;
            });
        }
    }

    // 刷新
    function checkSearch() {
        var data2 = [];
        _.each(vm.data, function(d) {
            if (d.check) {
                data2.push(d);
            }
        });
        vm.config = data2;
    }


}
