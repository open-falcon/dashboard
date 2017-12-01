function err_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 2,
        dialog: {
            msg: msg
        },
        end: f
    });
}

function ok_message_quietly(msg, f) {
    $.layer({
        title: false,
        closeBtn: false,
        time: 1,
        dialog: {
            msg: msg,
            type: 1
        },
        end: f
    });
}

function my_confirm(msg, btns, yes_func, no_func) {
    $.layer({
        shade: [ 0 ],
        area: [ 'auto', 'auto' ],
        dialog: {
            msg: msg,
            btns: 2,
            type: 4,
            btn: btns,
            yes: yes_func,
            no: no_func
        }
    });
}

function handle_quietly(json, f) {
    if (json.msg.length > 0) {
        err_message_quietly(json.msg);
    } else {
        ok_message_quietly("successfully:-)", f);
    }
}

