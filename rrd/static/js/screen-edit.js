$(function() {
    var config = {
        URLGet: '/graph/multi_edit?sid=',
        URLPost: '/graph/multi_edit'
    };

    // 点击
    $('.icon-muledit').on('click', function(e) {

        // 收集数据
        var $c = $('.chart-container');
        var charts = [];
        var sid = window.sid;
        $.getJSON(config.URLGet + sid, function(ret) {
            if (ret.ok) {
                charts = ret.data;
                var $area = $('#editModal').find('.edit-area');
                $area.html(_.template($('#tpl-edit').html(), {charts: charts}));
                $('#editModal').modal('show');
            } else {
                alert('出错了, msg: ' + ret.msg);
            }
        });
    });

    // save
    $('body').on('click', '.editModalYes', function(e) {
        // 收集数据
        var data = [];
        var $c = $('#editModal').find('.form-horizontal');
        _.each($c, function(i) {
            var obj = {};
            obj.id = $(i).find('.id').text();
            obj.endpoints = $(i).find('.endpoints').val().split('\n');
            obj.counters = $(i).find('.counters').val().split('\n');
            data.push(obj);
        });
        $.ajax({
            type: 'POST',
            url: config.URLPost,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: 'json',
            success: function(ret) {
                if (ret.ok) {
                    window.location.reload();
                } else {
                    alert('出错了, msg: ' + ret.msg);
                }
            }
        });
    });

});
