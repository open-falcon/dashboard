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
		'password' : $("#password").val()
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
