function err_message_quietly(msg, f) {
	$.layer({
		title : false,
		closeBtn : false,
		time : 2,
		dialog : {
			msg : msg
		},
		end : f
	});
}

function ok_message_quietly(msg, f) {
	$.layer({
		title : false,
		closeBtn : false,
		time : 1,
		dialog : {
			msg : msg,
			type : 1
		},
		end : f
	});
}

function my_confirm(msg, btns, yes_func, no_func) {
	$.layer({
		shade : [ 0 ],
		area : [ 'auto', 'auto' ],
		dialog : {
			msg : msg,
			btns : 2,
			type : 4,
			btn : btns,
			yes : yes_func,
			no : no_func
		}
	});
}

// - business function -

function login() {
	var raw = $('#ldap').prop('checked');
	if (raw) {
		useLdap = '1'
	} else {
		useLdap = '0'
	}
	$.post('/auth/login', {
		'name' : $('#name').val(),
		'password' : $("#password").val(),
        'ldap' : useLdap
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly('sign in successfully', function() {
				var redirect_url = '/user/profile';
				if (json.data.length > 0) {
					redirect_url = json.data;
				}
				location.href = redirect_url;
			});
		}
	}, "json");
}

function update_profile() {
	$.post('/user/profile', {
		'cnname' : $("#cnname").val(),
		'email' : $("#email").val(),
		'phone' : $("#phone").val(),
		'im' : $("#im").val(),
		'qq' : $("#qq").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly("更新成功：）");
		}
	}, "json");
}

function change_password() {
	$.post('/user/chpwd', {
		'old_password' : $("#old_password").val(),
		'new_password' : $("#new_password").val(),
		'repeat_password' : $("#repeat_password").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly("密码修改成功：）");
		}
	}, "json");
}

function register() {
	$.post('/auth/register', {
		'name' : $('#name').val(),
		'cnname' : $('#cnname').val(),
		'email' : $('#email').val(),
		'password' : $("#password").val(),
		'repeat_password' : $("#repeat_password").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly('sign up successfully', function() {
				location.href = '/auth/login';
			});
		}
	}, "json");
}

function query_user() {
	var query = $("#query").val();
	location.href = "/user/list?query=" + query;
}

function query_team() {
	var query = $("#query").val();
	location.href = "/team/list?query=" + query;
}

function create_user() {
	$.post('/user/create', {
		'name' : $("#name").val(),
		'cnname' : $("#cnname").val(),
		'email' : $("#email").val(),
		'phone' : $("#phone").val(),
		'im' : $("#im").val(),
		'qq' : $("#qq").val(),
		'password' : $("#password").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly("create user successfully");
		}
	}, "json");
}

function edit_user(id) {
	$.post('/admin/user/'+id+'/edit', {
        'id': id,
		'cnname' : $("#cnname").val(),
		'email' : $("#email").val(),
		'phone' : $("#phone").val(),
		'im' : $("#im").val(),
		'qq' : $("#qq").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly("更新成功：）");
		}
	}, "json");
}

function reset_password(id) {
	$.post('/admin/user/'+id+'/chpwd', {
		'password' : $("#password").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly("密码重置成功：）");
		}
	}, "json");
}

function create_team() {
	$.post('/team/create', {
		'name' : $("#name").val(),
		'resume' : $("#resume").val(),
		'users' : $("#users").val()
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly('create team successfully');
		}
	}, "json");
}

function edit_team(tid) {
	$.post('/team/'+tid+'/edit', {
		'resume' : $("#resume").val(),
		'users' : $("#users").val(),
		'id': tid
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
		} else {
			ok_message_quietly('edit team successfully');
		}
	}, "json");
}

function delete_user(uid) {
	my_confirm("真的要删除么？通常只有离职的时候才需要删除", [ '确定', '取消' ], function() {
		$.post('/admin/user/'+uid+'/delete', {
		}, function(json) {
			if (json.msg.length > 0) {
				err_message_quietly(json.msg);
			} else {
				ok_message_quietly('delete user successfully', function() {
					location.reload();
				});
			}
		}, "json");
	}, function() {
	});
}

function delete_team(id) {
	my_confirm("真的真的要删除么？", [ '确定', '取消' ], function() {
		$.post('/team/'+id+'/delete', {}, function(json) {
			if (json.msg.length > 0) {
				err_message_quietly(json.msg);
			} else {
				ok_message_quietly('delete team successfully', function() {
					location.reload();
				});
			}
		}, "json");
	}, function() {
	});
}

function set_role(uid, obj) {
	var role = obj.checked ? '1' : '0';
	$.post('/admin/user/'+uid+'/role', {
		'role' : role
	}, function(json) {
		if (json.msg.length > 0) {
			err_message_quietly(json.msg);
			location.reload();
		} else {
			if (role == '1') {
				ok_message_quietly('成功设置为管理员：）');
			} else if (role == '0') {
				ok_message_quietly('成功取消管理员权限：）');
			}
		}
	}, "json");
}

