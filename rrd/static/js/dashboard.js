function fn_list_endpoints()
{
    var qs = $.trim($("input[name='endpoint_search']").val());
    var tags = $.trim($("input[name='tag_search']").val());
    var limit = $("#endpoint-limit").val();
    var page = $("#endpoint-page").val();

    $(".loading").show();
    $.getJSON("/api/endpoints", {q: qs, tags: tags, limit:limit, page:page, _r:Math.random()}, function(ret){
                $(".loading").hide();
                if (!ret.ok) {
                    err_message_quietly(ret.msg);
                    return;
                }

                // display_endpoints
                var tbody_hosts = $("#tbody-endpoints");
                tbody_hosts.html("");
                for (var hidx in ret.data) {
                    var h = ret.data[hidx].endpoint;
                    var eid = ret.data[hidx].id;
                    var line_html = '<tr>'
                    + '<td><input type="checkbox" class="input shiftCheckbox" data-eid="'+ eid +'"  data-fullname="'+ h +'"></input></td>'
                    + '<td>' + h + '</td>'
                    + '</tr>';
                    tbody_hosts.append($(line_html));
                    tbody_hosts.find('.shiftCheckbox').shiftcheckbox();
                }
                fn_check_all_hosts();
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function fn_list_counters(){
    var qs = $.trim($("#counter-search").val());
    var eids = new Array();
    $("#tbody-endpoints input:checked").each(function(i, o){
        var eid = $(o).attr("data-eid");
        eids.push(eid);
    });
    if (eids.length === 0){
        err_message_quietly("先选定一些endpoints");
        return false;
    }

    var limit = $("#counter-limit").val();
    var page = $("#counter-page").val();
    $(".loading").show();
    $.ajax({
        method: "POST",
        url: "/api/counters",
        dataType: "json",
        data: {"eids": JSON.stringify(eids), "q": qs, "limit": limit, "page":page, "_r": Math.random()},
        success:function(ret){
            $(".loading").hide();
            if(ret.ok){
                var items = ret.data;
                // display counters
                var tbody_items = $("#tbody-counters");
                tbody_items.html("");

                for (var i in items) {
                    var c = items[i];
                    var display_counter_type = "计数器";
                    if(c[1] == "GAUGE") {
                        display_counter_type = "原始值";
                    }
                    var line_html = '<tr>'
                    + '<td><input type="checkbox" class="input shiftCheckbox" data-fullkey="'+c[0]+'"></input></td>'
                    + '<td><a href="javascript:void(0);" onclick="fn_show_chart(\'' + c[0] + '\')" >' + c[0] + '</a></td>'
                    + '<td>'+ display_counter_type +'</td>'
                    + '<td>'+ c[2] +'s</td>'
                    + '</tr>'
                    tbody_items.append($(line_html));
                    tbody_items.find('.shiftCheckbox').shiftcheckbox();
                }
            }else{
                err_message_quietly("搜索失败：" + ret.msg);
                return false;
            }
        }
    });
}

function fn_delete_counters(){
    var checked_hosts = new Array();
    $("#tbody-endpoints input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var hostfullname = $(o).attr("data-fullname");
            checked_hosts.push(hostfullname);
        }
    });
    if(checked_hosts.length === 0){
        err_message_quietly("先选endpoint：）");
        return false;
    }

    var checked_items = new Array();
    $("#tbody-counters input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var key_ = $(o).attr("data-fullkey");
            checked_items.push(key_);
        }
    });
    if (checked_items.length === 0){
        err_message_quietly("请选择counter");
        return false;
    }
    if(checked_items.length > 10) {
        err_message_quietly("每次删除不能超过10个，免得你后悔:");
        return false;
    }


	my_confirm("真的要删除么？这会删除MySQL中对应的内容，也会清除磁盘上对应的数据文件", [ '确定', '取消' ], function() {
        $.ajax({
            url: "/api/counters",
            dataType: "json",
            method: "DELETE",
            data: {"endpoints": checked_hosts, "counters": checked_items, "_r": Math.random()},
            success: function(ret) {
                if (ret.ok) {
                    ok_message_quietly(ret.data);
                }else {
                    err_message_quietly("请求出错了");
                }
            },
            error: function(){
                err_message_quietly("请求出错了");
            }
        });

	}, function() {
	});

    return false;
}

function fn_delete_endpoints(){
    var checked_hosts = new Array();
    $("#tbody-endpoints input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var hostfullname = $(o).attr("data-fullname");
            checked_hosts.push(hostfullname);
        }
    });
    if(checked_hosts.length === 0){
        err_message_quietly("先选endpoint：）");
        return false;
    }

    if(checked_hosts.length > 2) {
        err_message_quietly("每次删除不能超过2个，免得你后悔:");
        return false;
    }

	my_confirm("真的要删除么？这会删除MySQL中对应的内容，也会清除磁盘上对应的数据文件", [ '确定', '取消' ], function() {
        $.ajax({
            url: "/api/endpoints",
            dataType: "json",
            method: "DELETE",
            data: {"endpoints": checked_hosts, "_r": Math.random()},
            success: function(ret) {
                if (ret.ok) {
                    ok_message_quietly(ret.data);
                }else {
                    err_message_quietly("请求出错了");
                }
            },
            error: function(){
                err_message_quietly("请求出错了");
            }
        });
	}, function() {
	});

    return false;
}


function filter_endpoint()
{
    var filter_text = $("#endpoint-filter").val().toLowerCase();
    var targets = $("#tbody-endpoints tr");
    if(!filter_text){
        targets.each(function(i, obj){
            $(obj).show();
        });
    }else{
        var filter_pattern = new RegExp(filter_text, "i");

        targets.each(function(i, obj){
            var checkbox = $($(obj).find("input[type='checkbox']")[0]);
            var name = checkbox.attr("data-fullname");
            if(filter_pattern.exec(name) == null){
                $(obj).hide();
            }else{
                $(obj).show();
            }
            if($(obj).is(":visible")){
                checkbox.prop("checked", true);
            }else{
                checkbox.prop("checked", false);
            }
        });
    }
};

function filter_counter()
{
    var filter_text = $("#counter-filter").val().toLowerCase();
    var targets = $("#tbody-counters tr");
    if(!filter_text){
        targets.each(function(i, obj){
            $(obj).show();
        });
    }else{
        var filter_pattern = new RegExp(filter_text, "i");
        targets.each(function(i, obj){
            var checkbox = $($(obj).find("input[type='checkbox']")[0]);
            var name = checkbox.attr("data-fullkey");
            if(filter_pattern.exec(name) == null){
                $(obj).hide();
            }else{
                $(obj).show();
            }
            if($(obj).is(":visible")){
                checkbox.prop("checked", true);
            }else{
                checkbox.prop("checked", false);
            }
        });
    }
};

function fn_show_chart(counter)
{
    var checked_hosts = new Array();
    $("#tbody-endpoints input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var hostfullname = $(o).attr("data-fullname");
            checked_hosts.push(hostfullname);
        }
    });
    if(checked_hosts.length === 0){
        err_message_quietly("先选endpoint：）");
        return false;
    }

    checked_items = new Array();
    checked_items.push(counter);
    var w = window.open();
    $.ajax({
        url: "/chart",
        dataType: "json",
        method: "POST",
        data: {"endpoints": checked_hosts, "counters": checked_items, "graph_type": "h", "_r": Math.random()},
        success: function(ret) {
            if (ret.ok) {
                setTimeout(function(){w.location='/chart/big?id='+ret.id;}, 0);
            } else {
                err_message_quietly("请求出错了");
            }
        },
        error: function(){
            err_message_quietly("请求出错了");
        }
    });
    return false;
}

function fn_show_all(graph_type)
{
    var checked_hosts = new Array();
    $("#tbody-endpoints input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var hostfullname = $(o).attr("data-fullname");
            checked_hosts.push(hostfullname);
        }
    });
    if(checked_hosts.length === 0){
        err_message_quietly("先选endpoint：）");
        return false;
    }

    var checked_items = new Array();
    $("#tbody-counters input:checked").each(function(i, o){
        if($(o).is(":visible")){
            var key_ = $(o).attr("data-fullkey");
            checked_items.push(key_);
        }
    });
    if (checked_items.length === 0){
        err_message_quietly("请选择counter");
        return false;
    }

    var w = window.open();
    $.ajax({
        url: "/chart",
        dataType: "json",
        method: "POST",
        data: {"endpoints": checked_hosts, "counters": checked_items, "graph_type": graph_type, "_r": Math.random()},
        success: function(ret) {
            if (ret.ok) {
                setTimeout(function(){w.location="/charts?id="+ret.id+"&graph_type="+graph_type;}, 0);
            }else {
                err_message_quietly("请求出错了");
            }
        },
        error: function(){
            err_message_quietly("请求出错了");
        }
    });
    return false;
}

function fn_check_all_items()
{
    var box = $("#check_all_counters");
    if(box.prop("checked")){
        $("#tbody-counters").find("input:checkbox").each(function(i, o){
            $(o).prop("checked", true);
        });
    }else{
        $("#tbody-counters").find("input:checkbox").each(function(i, o){
            $(o).prop("checked", false);
        });
    }
}

function fn_check_all_hosts()
{
    var box = $("#check_all_endpoints");
    if(box.prop("checked")){
        $("#tbody-endpoints").find("input:checkbox").each(function(i, o){
            $(o).prop("checked", true);
        });
    }else{
        $("#tbody-endpoints").find("input:checkbox").each(function(i, o){
            $(o).prop("checked", false);
        });
    }
}

function fn_filter_group()
{
    var filter_text = $("#group-filter").val().toLowerCase();
    var group_objs = $(".group");
    if(!filter_text){
        group_objs.each(function(i, obj){
            $(obj).show();
        });
    }else if (filter_text.length <= 2) {
    }else{
        group_objs.each(function(i, obj){
            var groupname = $($(obj).children("a")[0]).attr("data-gname");
            if(groupname.toLowerCase().indexOf(filter_text) === -1){
                $(obj).hide();
            }else{
                $(obj).show();
            }
        });
        fn_collapse_in_groups();
    }
};

function fn_collapse_in_groups()
{
    $(".accordion-body").each(function(i, obj){
        if(!$(obj).hasClass("in")){
            $(obj).collapse("show");
        }
    });
};
