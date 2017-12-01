// - business function -
function query_user() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/portal/hostgroup?q=' + query + '&mine=' + mine;
}

function create_hostgroup() {
    var name = $.trim($("#grp_name").val());
    $.post('/portal/group/create', {'grp_name': name}, function (json) {
        handle_quietly(json, function () {
            window.location.reload();
        });
    }, "json");
}

function delete_hostgroup(group_id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/portal/group/delete/' + group_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        });
    }, function () {
        return false;
    });
}

function edit_hostgroup(group_id, grp_name) {
    layer.prompt({title: 'input new name:', val: grp_name, length: 255}, function (val, index, elem) {
        $.post('/portal/group/update/' + group_id, {'new_name': val}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        }, "json");
    })
}

function rename_hostgroup() {
    var old_str = $.trim($('#old_str').val());
    var new_str = $.trim($('#new_str').val());
    $.post('/portal/group/rename', {'old_str': old_str, 'new_str': new_str}, function (json) {
        handle_quietly(json, function () {
            window.location.href = '/?q=' + new_str;
        });
    }, "json");
}

function bind_plugin(group_id) {
    var plugin_idr = $.trim($("#plugin_dir").val());
    $.post('/portal/plugin/bind', {'group_id': group_id, 'plugin_dir': plugin_idr}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json");
}

function unbind_plugin(plugin_id) {
    my_confirm('确定要解除绑定？', ['确定', '取消'], function () {
        $.getJSON('/portal/plugin/delete/' + plugin_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        });
    }, function () {
        return false;
    });
}

function query_host() {
    var xbox = $("#xbox").val();
    var group_id = $("#group_id").val();
    var query = $.trim($("#query").val());
    var limit = $("#limit").val();
    var maintaining = document.getElementById('maintaining').checked ? 1 : 0;
    window.location.href = '/portal/group/' + group_id + '/hosts?q=' + query + '&maintaining=' + maintaining + '&limit=' + limit + '&xbox=' + xbox;
}

function select_all() {
    var v = document.getElementById('chk').checked;
    $.each($("#hosts input[type=checkbox]"), function (i, n) {
        n.checked = v;
    });
}

function remove_hosts() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    var group_id = $("#group_id").val();
    $.post("/portal/host/remove", {'host_ids': ids.join(","), 'grp_id': group_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json");
}

function maintain() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    var begin = $.trim($("#begin").val());
    var end = $.trim($("#end").val());

    if (begin.length == 0 || end.length == 0) {
        err_message_quietly('begin time and end time are necessary');
        return false;
    }

    var b = moment(begin, "YYYY-MM-DD HH:mm").unix();
    var e = moment(end, "YYYY-MM-DD HH:mm").unix();

    $.post('/portal/host/maintain', {'begin': b, 'end': e, 'host_ids': ids.join(',')}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json");
}

function no_maintain() {
    var ids = [];
    jQuery.each($("#hosts input[type=checkbox]"), function (i, n) {
        if (n.checked) {
            ids.push($(n).attr("hid"));
        }
    });
    if (ids.length == 0) {
        err_message_quietly('no hosts selected');
        return;
    }

    $.post('/portal/host/reset', {'host_ids': ids.join(',')}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json");
}

function batch_add_host() {
    var hosts = $.trim($("#hosts").val());
    if (hosts.length == 0) {
        err_message_quietly('请填写机器列表，一行一个');
        return false;
    }

    $.post('/portal/host/add', {'group_id': $("#group_id").val(), 'hosts': hosts}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            $("#message").html(json.data);
        }
    }, "json");
}

function host_unbind_group(host_id, group_id) {
    $.getJSON('/portal/host/unbind', {'host_id': host_id, 'group_id': group_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    })
}

function query_expression() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/portal/expression?q=' + query + '&mine=' + mine;
}

function delete_expression(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/portal/expression/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function update_expression() {
    var callback_url = $.trim($("#callback_url").val());
    var need_callback = callback_url.length > 0 ? 1 : 0;
    $.post(
        '/portal/expression/update',
        {
            'expression': $.trim($("#expression").val()),
            'func': $.trim($("#func").val()),
            'op': $("#op").val(),
            'right_value': $.trim($("#right_value").val()),
            'uic': $.trim($("#uic").val()),
            'max_step': $.trim($("#max_step").val()),
            'priority': $.trim($("#priority").val()),
            'note': $.trim($("#note").val()),
            'url': callback_url,
            'callback': need_callback,
            'before_callback_sms': document.getElementById("before_callback_sms").checked ? 1 : 0,
            'before_callback_mail': document.getElementById("before_callback_mail").checked ? 1 : 0,
            'after_callback_sms': document.getElementById("after_callback_sms").checked ? 1 : 0,
            'after_callback_mail': document.getElementById("after_callback_mail").checked ? 1 : 0,
            'expression_id': $("#expression_id").val()
        },
        function (json) {
            handle_quietly(json);
        }, "json");
}

function pause_expression(id) {
    var pause = '1';
    if ($('#i-' + id).attr('class').indexOf('play') > 0) {
        // current: pause
        pause = '0'
    }
    $.getJSON("/portal/expression/pause", {'id': id, 'pause': pause}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            if (pause == '1') {
                $('#i-' + id).attr('class', 'glyphicon glyphicon-play orange')
            } else {
                $('#i-' + id).attr('class', 'glyphicon glyphicon-pause orange')
            }
        }
    });
}

function make_select2_for_uic_group(selector) {
    $(selector).select2({
        placeholder: "input uic team name",
        allowClear: true,
        multiple: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.name;
        },
        ajax: {
            url: "/api/uic/group",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 20
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var data = [];
            $($(element).val().split(",")).each(function () {
                data.push({id: this, name: this});
            });
            callback(data);
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
}

function query_template() {
    var query = $.trim($("#query").val());
    var mine = document.getElementById('mine').checked ? 1 : 0;
    window.location.href = '/portal/template?q=' + query + '&mine=' + mine;
}

function delete_template(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/portal/template/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function create_template() {
    var tpl_name = $.trim($("#tpl_name").val());
    $.post('/portal/template/create', {'name': tpl_name}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            location.href = '/portal/template/update/' + json.id;
        }
    }, "json");
}

function make_select2_for_template(selector) {
    $(selector).select2({
        placeholder: "input template name",
        allowClear: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.id;
        },
        ajax: {
            url: "/api/template/query",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 10
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var tpl_id = $(element).val();
            $.getJSON("/api/template/" + tpl_id, function (json) {
                callback(json.data);
            });
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
}

function make_select2_for_metric(selector) {
    $(selector).select2({
        placeholder: "input metric",
        allowClear: true,
        quietMillis: 100,
        minimumInputLength: 2,
        id: function (obj) {
            return obj.name;
        },
        ajax: {
            url: "/api/metric/query",
            dataType: 'json',
            data: function (term, page) {
                return {
                    query: term,
                    limit: 10
                };
            },
            results: function (json, page) {
                return {results: json.data};
            }
        },

        initSelection: function (element, callback) {
            var val = $(element).val();
            callback({id: val, name: val});
        },

        formatResult: function (obj) {
            return obj.name
        },
        formatSelection: function (obj) {
            return obj.name
        }
    });
}

function update_template() {
    var tpl_id = $('#tpl_id').val();
    var name = $.trim($("#name").val());
    var parent_id = $("#parent_id").val();
    $.post('/portal/template/rename/' + tpl_id, {'name': name, 'parent_id': parent_id}, function (json) {
        handle_quietly(json);
    }, "json");
}

function save_action_for_tpl(tpl_id) {
    var callback_url = $.trim($("#callback_url").val());
    var need_callback = callback_url.length > 0 ? 1 : 0;
    $.post(
            '/portal/template/action/update/' + tpl_id,
        {
            'uic': $.trim($("#uic").val()),
            'url': callback_url,
            'callback': need_callback,
            'before_callback_sms': document.getElementById("before_callback_sms").checked ? 1 : 0,
            'before_callback_mail': document.getElementById("before_callback_mail").checked ? 1 : 0,
            'after_callback_sms': document.getElementById("after_callback_sms").checked ? 1 : 0,
            'after_callback_mail': document.getElementById("after_callback_mail").checked ? 1 : 0
        },
        function (json) {
            handle_quietly(json);
        }, "json");
}

function goto_strategy_add_div() {
    $("#add_div").show('fast');
    $("#current_sid").val('');
    location.href = "#add";
}

function save_strategy() {
    var sid = $("#current_sid").val();
    $.post('/portal/strategy/update', {
        'sid': sid,
        'metric': $.trim($("#metric").val()),
        'tags': $.trim($("#tags").val()),
        'max_step': $.trim($("#max_step").val()),
        'priority': $.trim($("#priority").val()),
        'note': $.trim($("#note").val()),
        'func': $.trim($("#func").val()),
        'op': $.trim($("#op").val()),
        'right_value': $.trim($("#right_value").val()),
        'run_begin': $.trim($("#run_begin").val()),
        'run_end': $.trim($("#run_end").val()),
        'tpl_id': $.trim($("#tpl_id").val())
    }, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json")
}

function clone_strategy(sid) {
    $("#current_sid").val('');
    fill_fields(sid);
}

function modify_strategy(sid) {
    $("#current_sid").val(sid);
    fill_fields(sid);
}

function fill_fields(sid) {
    $("#add_div").show('fast');
    location.href = "#add";
    $.getJSON('/portal/strategy/' + sid, {}, function (json) {
        $("#metric").val(json.data.metric);
        $("#tags").val(json.data.tags);
        $("#max_step").val(json.data.max_step);
        $("#priority").val(json.data.priority);
        $("#note").val(json.data.note);
        $("#func").val(json.data.func);
        $("#op").val(json.data.op);
        $("#right_value").val(json.data.right_value);
        $("#run_begin").val(json.data.run_begin);
        $("#run_end").val(json.data.run_end);
        make_select2_for_metric("#metric");
    });
}

function delete_strategy(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.getJSON('/portal/strategy/delete/' + id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function tpl_unbind_group(tpl_id, grp_id) {
    my_confirm('确定要解除绑定关系？', ['确定', '取消'], function () {
        $.getJSON('/portal/template/unbind/group', {'tpl_id': tpl_id, 'grp_id': grp_id}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function fork_template(tpl_id) {
    $.getJSON('/portal/template/fork/' + tpl_id, {}, function (json) {
        if (json.msg.length > 0) {
            err_message_quietly(json.msg);
        } else {
            location.href = '/portal/template/update/' + json.id;
        }
    });
}

function bind_template(grp_id) {
    var tpl_id = $.trim($("#tpl_id").val());
    $.getJSON('/portal/group/bind/template', {'grp_id': grp_id, 'tpl_id': tpl_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        })
    });
}

function node_unbind_tpl(grp_name, tpl_id) {
    my_confirm('确定要解除绑定关系？', ['确定', '取消'], function () {
        $.getJSON('/portal/template/unbind/node', {'tpl_id': tpl_id, 'grp_name': grp_name}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        })
    }, function () {
        return false;
    });
}

function node_bind_tpl() {
    var node = $.trim($("#node").val());
    var tpl_id = $("#tpl_id").val();
    $.post('/portal/template/bind/node', {'node': node, 'tpl_id': tpl_id}, function (json) {
        handle_quietly(json, function () {
            location.reload();
        });
    }, "json");
}

function create_cluster_monitor_metric(grp_id) {
    $.post('/portal/group/' + grp_id + '/cluster/creator', {
        'numerator': $("#numerator").val(),
        'denominator': $("#denominator").val(),
        'endpoint': $("#endpoint").val(),
        'metric': $("#metric").val(),
        'tags': $("#tags").val(),
        'step': $("#step").val()
    }, function (json) {
        handle_quietly(json, function () {
            location.href = "/portal/group/" + grp_id + "/cluster";
        });
    }, "json")
}

function update_cluster_monitor_metric(cluster_id, grp_id) {
    $.post('/portal/cluster/edit/' + cluster_id, {
        'numerator': $("#numerator").val(),
        'denominator': $("#denominator").val(),
        'endpoint': $("#endpoint").val(),
        'metric': $("#metric").val(),
        'tags': $("#tags").val(),
        'step': $("#step").val(),
        'grp_id': grp_id
    }, function (json) {
        handle_quietly(json);
    }, "json");
}

function delete_cluster_monitor_item(cluster_id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/portal/cluster/delete/' + cluster_id, {}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            })
        }, "json");
    }, function () {
        return false;
    });
}

// - alarm-dash business function -
function alarm_case_all_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked="checked";
    }
}
function alarm_case_event_all_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked="checked";
    }
}

function alarm_case_reverse_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            boxes[i].checked=""
        } else {
            boxes[i].checked="checked";
        }
    }
}
function alarm_case_event_reverse_select() {
    var boxes = $("input[type=checkbox]");
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            boxes[i].checked=""
        } else {
            boxes[i].checked="checked";
        }
    }
}

function alarm_case_batch_rm() {
    var boxes = $("input[type=checkbox]");
    var ids = []
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            ids.push($(boxes[i]).attr("alarm"))
        }
    }

    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/portal/alarm-dash/case/delete', {"ids": ids.join(',')}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        }, "json");
    }, function () {
        return false;
    });
}

function alarm_case_rm(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/portal/alarm-dash/case/delete', {"ids": id}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        }, "json");
    }, function () {
        return false;
    });
}

function alarm_case_event_rm(id) {
    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/portal/alarm-dash/case/event/delete', {"ids": id}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        }, "json");
    }, function () {
        return false;
    });
}
function alarm_case_event_batch_rm() {
    var boxes = $("input[type=checkbox]");
    var ids = []
    for (var i = 0; i < boxes.length; i++) {
        if (boxes[i].checked) {
            ids.push($(boxes[i]).attr("alarm"))
        }
    }

    my_confirm('确定要删除？？？', ['确定', '取消'], function () {
        $.post('/portal/alarm-dash/case/event/delete', {"ids": ids.join(',')}, function (json) {
            handle_quietly(json, function () {
                location.reload();
            });
        }, "json");
    }, function () {
        return false;
    });
}
