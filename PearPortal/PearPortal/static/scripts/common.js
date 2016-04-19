
	var common = {
		getCookie: function(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
				    var cookie = jQuery.trim(cookies[i]);
				    // Does this cookie string begin with the name we want?
				    if (cookie.substring(0, name.length + 1) == (name + '=')) {
				        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				        break;
				    }
				}
			}
			return cookieValue;
		},

		csrfSafeMethod: function(method){
			// these HTTP methods do not require CSRF protection
	    	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		},

		decodeQueryString: function(queryString) {
        	var parts = queryString.split("&");
        	var output = {};
        	parts.forEach(function(x) {
            	var splitIndex = x.indexOf("=");
            	if (splitIndex < 0)
                	return;
            	var key = decodeURIComponent(x.substr(0, splitIndex));
            	var value = decodeURIComponent(x.substr(splitIndex + 1));
            	output[key] = value;
        	});
        	return output;
    	}

	};

