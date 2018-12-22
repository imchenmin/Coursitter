//Simple search: single condition:
var data = "tb"; //string
$.ajax({
                type: 'GET',
                url: "/searchCourse",
                anysc: false,
                data: JSON.stringify(data),  //转化字符串
                contentType: 'application/json',
                dataType:'json',
                success: function (rdata) { //成功的话，得到消息
                    //rdata's type is json
                    //returnClass(data);
                }
    });

//Label search: multiple condition:
var datal = {"Grade":[], "Departments":[], "CourseType":[], "interval":[], "day":[]}; //dictionary
$.ajax({
                type: 'GET',
                url: "/searchLabel",
                anysc: false,
                data: JSON.stringify(datal),  //转化字符串
                contentType: 'application/json',
                dataType:'json',
                success: function (rdata) { //成功的话，得到消息
                    //rdata's type is json
                    //returnClass(data);
                }
    });

//others need to use POST
// first need to add these codes at the head of .js
// using jQuery
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');

            function csrfSafeMethod(method) {
                // 这些HTTP方法不要求CSRF包含
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
//and then use .ajax
$.ajax({
                type: 'POST',
                url: "/url",//todo confirm .
                // "/addClass"
                anysc: false,
                data: JSON.stringify(data),  //转化字符串
                contentType: 'application/json',
                dataType:'json',
                success: function (rdata) { //成功的话，得到消息
                    //true
                    //false, string: why
                    //rdata's type is json
                    //returnClass(data);
                }
    });