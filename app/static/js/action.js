// window.class_data = [{
//     "courseName": "人工智能",
//     "courseID": "CS304",
//     "credit": 3,
//     "note": "课程系统完整地讲解当今整地讲解当今整地讲解当今整地讲解当今主流当今整地对xxx...",
//     "classes": [{
//         "teachers": "唐柯",
//         "classinfo": ["周二3-4节 荔园一栋101", "周五5-6节 荔园6栋403"],
//         "classnum": 101,
//         "period": [2, 2, 5, 3]
//     },
//         {
//             "teachers": "唐柯",
//             "classinfo": ["周二3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
//             "classnum": 101,
//             "period": [2, 2, 3, 3]
//         }
//     ]
// },
//     {
//         "courseName": "面向对象",
//         "courseID": "CS303",
//         "classes": [{
//             "teachers": "张誉群",
//             "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
//             "classnum": 101,
//             "period": [4, 2, 3, 3]
//         }]
//     }
// ];
window.class_data = [];
window.labels_title = {"Grade": "面向年级", "CourseType": "课程性质", "Departments": "院系", "day": "星期", "interval": "节次"};
window.labels = {
    "Grade": "大一 大二 大三 大四",
    "CourseType": "必修 选修",
    "Departments": "通识基础 数学系 物理系 化学系 生物系 计算机系 电子系 地空系 海洋系 材料系 环境系 机械系 生医工系 金融系 人文中心 社科中心 语言中心 艺术中心 体育中心",
    "day": "星期一 星期二 星期三 星期四 星期五 星期六 星期日",
    "interval": "1-2节 3-4节 5-6节 7-8节 9-10节 11节"
};

window.selectedCourse = [];

window.onload = function () {
    document.getElementById("commit_Edit").style.display = "none";
    document.getElementById("all_label").style.display = "none";
    var labels_obj = generate_labels();
    for (var label in labels_obj) {
        document.getElementById("all_label").appendChild(labels_obj[label]);
    }
    $.ajax({
        type: 'GET',
        url: "/allCourse",
        anysc: false,
        data: null,  //转化字符串
        contentType: 'application/json',
        dataType: 'json',
        success: function (rdata) { //成功的话，得到消息
            //rdata's type is json
            //returnClass(data);
            //alert(JSON.stringify(rdata));

            var max_length = 23;
            rdata = rdata["result"];
            for (var i in rdata) {
                if (rdata[i]['note'].length > max_length) {
                    rdata[i]['note_short'] = rdata[i]['note'].substr(0, max_length) + '...';
                } else {
                    rdata[i]['note_short'] = rdata[i]['note'];
                }

                // 任课老师
                var lecturer = '';
                if (rdata[i].hasOwnProperty("classes")) {
                    var allClass = rdata[i]['classes'];
                    for (var d in allClass) {
                        if (lecturer === '') {
                            lecturer = allClass[d]['teachers'];

                        } else {
                            if (lecturer === allClass[d]['teachers']) {
                                lecturer += '等';
                                break;
                            }
                        }
                    }
                    rdata[i]['lecturer'] = lecturer;
                }


            }

            window.class_data = rdata;
            $('#class_table').bootstrapTable('prepend', window.class_data);
            // refreshCourseTable(rdata["result"]);

        }
    });
    $.ajax({
        type: 'GET',
        url: "/getHistory",
        anysc: false,
        data: null,  //转化字符串
        contentType: 'application/json',
        dataType: 'json',
        success: function (rdata) {
            // window.selectedCourse = rdata['result'];
            insertCard(window.class_data, rdata['result']);
        }
    });
    loadCourseTable();


};

function loadCourseTable() {
    updateRcoin();
    var oCoin = document.getElementById('rcoin');
    var oDiv1 = document.getElementById('div1');
    var oBtn = document.getElementById('span');
    var begin = getStyle(oDiv1, 'left');
    begin = parseInt(begin.substr(0, begin.length - 2));
    oDiv1.onmouseover = function () {
        startMove(oDiv1, 'left', begin + oDiv1.offsetWidth);
    };
    oDiv1.onmouseout = function () {
        setTimeout("", 2000);
        startMove(oDiv1, 'left', begin);
    };
    var oUl_course = document.getElementById('courseList');
    var oBtn_insert = document.getElementById('insert');
    // oBtn_insert.onclick = "insertCard()";
}


$(document).ready(function () {

    $('#class_table').bootstrapTable({
        data: window.class_data,
        editable: true,//开启编辑模式
        clickToSelect: true,
        cache: false,
        // showToggle:true, //显示切换按钮来切换表/卡片视图。
        // showPaginationSwitch:true, //显示分页切换按钮
        pagination: true,
        classes: 'table-no-bordered',
        pageList: [25],
        pageSize: 15,
        pageNumber: 1,
        uniqueId: 'index', //将index列设为唯一索引
        striped: true,

        // search: true,
        height: 655,
        // showRefresh: true,
        minimumCountColumns: 2,
        smartDisplay: true,
        onClickRow: function (row, $element) {
            var courseModal = $('#myModal');
            courseModal.modal('show');
            $('#myModal h2')[0].innerHTML = row['courseName'] + '(' + row['courseID'] + ')' + '--课程信息';
            var currentCourse;
            var flag = false;

            for (i in window.selectedCourse) {
                if (window.selectedCourse[i]['courseID'] === row['courseID']) {
                    flag = true;
                    break;
                }

            }
            var obj = $('#myModal button')[1];
            if (!flag) {
                obj.innerHTML = "选择课程";
                obj.value = "unselected";
                obj.setAttribute("class", 'w3-btn c5');
            } else {
                obj.innerHTML = "取消选择";
                obj.value = "selected";
                obj.setAttribute("class", 'w3-btn w3-red');
            }


            for (var i in window.class_data) {
                if (window.class_data[i]["courseID"] === row['courseID']) {
                    currentCourse = window.class_data[i];
                    break;
                }

            }
            $('#myModal h5')[0].innerHTML = currentCourse['note'];
            $('#myModal button')[1].id = i;

            // 课程卡片
            var classBox = $('#classBox');
            classBox.empty();
            var colorSet = ['w3-light-green', 'w3-lime', 'w3-khaki'];
            var classes = currentCourse['classes'];

            for (var c in classes) {
                var classCard = document.createElement('div');
                var classType = 'w3-hover-shadow w3-center ';
                classType += colorSet[classBox.children.length % 3];
                classCard.setAttribute('class', classType);
                var class_id = parseInt(c) + 1;
                var class_head = class_id + '班  ' + classes[c]['teachers'];
                // fixme 课程分行显示
                var class_time = classes[c]['classinfo'];
                classCard.innerHTML = class_head + class_time;
                classBox.append(classCard)
            }


            /*
                    <div class="w3-khaki w3-hover-shadow w3-center center">
                            <p> 一班:<br/>
                        周一 1-2节
                        一教101 王老师<br/>
                        周二 1-2节
                        一教101 王老师</p>
                        </div>
                        <div class="w3-light-green w3-hover-shadow w3-center">
                            <p> 一班:<br/>
                        周一 1-2节
                        一教101 王老师<br/>
                        周二 1-2节
                        一教101 王老师</p>
                        </div>
            */


        },
        columns: [{
            field: 'courseID',
            title: '课程编号',
            class: "col-md-1"
        }, {
            field: 'courseName',
            title: '课程名称',
            class: "col-md-3"
        }, {
            field: 'credit',
            title: '学分',
            class: "col-md-1 text-center"
        }, {
            field: 'lecturer',
            title: '任课教师',
            class: "col-md-1"
        }, {
            field: 'note_short',
            title: '课程简介',
            class: "col-md-6"
        },
        ],

    });
});


function refreshCourseTable(rdata) {
    $('#class_table').bootstrapTable('removeAll');
    var returnCourse = [];
    for (var i in rdata) {
        for (var c in window.class_data) {
            if (rdata[i]['courseID'] === window.class_data[c]['courseID']) {
                returnCourse.push(window.class_data[c]);
                break;
            }
        }
    }
    $('#class_table').bootstrapTable('prepend', returnCourse);
}

function search_class() {
    var data = $('#searchContent').val(); //string

    if (data) {
        $.ajax({
            type: 'GET',
            url: "/searchCourse",
            anysc: false,
            data: data,  //转化字符串
            contentType: 'application/json',
            dataType: 'json',
            success: function (rdata) { //成功的话，得到消息
                //rdata's type is json
                //returnClass(data);
                //alert(JSON.stringify(rdata));
                refreshCourseTable(rdata["result"]);

            }
        });
    } else {
        $('#class_table').bootstrapTable('removeAll');
        $('#class_table').bootstrapTable('prepend', window.class_data);

    }


    // var rdata = [{
    //     "courseName": "面向对象",
    //     "courseID": "CS303",
    //     "classes": [{
    //         "teachers": "张誉群",
    //         "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
    //         "classnum": 101,
    //         "period": [4, 2, 3, 3]
    //     }]
    // }];


}

function pull_course() {
    window.class_data = [{
        "courseName": "面向对象",
        "courseID": "CS303",
        "classes": [{
            "teachers": "张誉群",
            "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
            "classnum": 101,
            "period": [4, 2, 3, 3]
        }]
    }];

}

function showFullLabel() {
    document.getElementById("label").classList.replace("col-md-1", "col-md-8");
    document.getElementById("Edit").style.display = "none";
    document.getElementById("commit_Edit").style.display = "inline";
    document.getElementById("all_label").style.display = "inline";
    document.getElementById("selected_label").classList.replace("col-md-12", "col-md-2");

}

function searchByLabel() {
    var datal = {"Grade": [], "Departments": [], "CourseType": [], "interval": [], "day": []}; //dictionary

    $("#selected_label button").each(function () {
        var label = this.innerHTML;

        for (var key in window.labels) {
            var temp = window.labels[key];
            var has = temp.indexOf(label) > -1;
            if (has) {
                // alert(key+" "+label);
                datal[key].push(label);
                break;
            }

        }


    });
    var count = 0;
    for (var key in datal) {
        if (datal[key].length === 0) {
            delete datal[key];
        } else {
            count++;
        }
    }

    if (count > 0) {
        $.ajax({
            type: 'GET',
            url: "/searchLabel",
            anysc: false,
            data: datal,  //转化字符串
            contentType: 'application/json',
            dataType: 'json',
            success: function (rdata) { //成功的话，得到消息
                //rdata's type is json
                //returnClass(data);
                refreshCourseTable(rdata['result']);
            }
        });
    } else {
        $('#class_table').bootstrapTable('removeAll');
        $('#class_table').bootstrapTable('prepend', window.class_data);

    }


    // var rdata = [{
    //     "courseName": "人工智能",
    //     "courseID": "CS303",
    //     "lecturer": "唐珂",
    //     "classes": [{
    //         "teachers": "唐珂",
    //         "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
    //         "classnum": 101,
    //         "period": [4, 2, 3, 3]
    //     }]
    // }, {
    //     "courseName": "人工智能",
    //     "courseID": "CS303",
    //     "classes": [{
    //         "teachers": "唐珂",
    //         "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
    //         "classnum": 101,
    //         "period": [4, 2, 3, 3]
    //     }]
    // }, {
    //     "courseName": "人工智能",
    //     "courseID": "CS303",
    //     "classes": [{
    //         "teachers": "唐珂",
    //         "classinfo": ["周四3-4节 荔园一栋101", "周三5-6节 荔园6栋403"],
    //         "classnum": 101,
    //         "period": [4, 2, 3, 3]
    //     }]
    // }];
    // refreshCourseTable(rdata);

}

function showSelectedLabel() {
    document.getElementById("label").classList.replace("col-md-8", "col-md-1");
    document.getElementById("commit_Edit").style.display = "none";
    document.getElementById("Edit").style.display = "inline";
    document.getElementById("all_label").style.display = "none";
    document.getElementById("selected_label").classList.replace("col-md-2", "col-md-12");

    searchByLabel();
}

function generate_labels() {


    var labels_obj = [];
    for (var i in window.labels) {
        var l_obj = document.createElement('div');
        l_obj.classList.add("label_set");
        l_obj.classList.add("col-md-6");
        var ls = window.labels[i].split(" ");
        var title_obj = document.createElement("h4");
        title_obj.innerHTML = window.labels_title[i];
        title_obj.classList.add("label_title");
        l_obj.appendChild(title_obj);
        for (var j in ls) {
            // <button id="Edit" type="button" class="btn btn-primary " onclick="showFullLabel()">编辑</button>

            var label_name = ls[j];

            var single_label = document.createElement("button");

            single_label.setAttribute("onclick", "select_label(this)");


            single_label.setAttribute("class", "w3-btn w3-white w3-border w3-border col-md-3");
            // single_label.classList.add("btn");
            single_label.setAttribute("style", "padding:5px;text-align: center;");
            single_label.setAttribute("title", "unselected");
            single_label.setAttribute("id", label_name);
            single_label.innerHTML = label_name;
            l_obj.appendChild(single_label);

        }


        labels_obj.push(l_obj);

    }

    return labels_obj;
}

function copy(obj) {
    var newobj = {};
    for (var attr in obj) {
        newobj[attr] = obj[attr];
    }
    return newobj;
}

function select_label(obj) {
    // 标签数量最大值
    if (obj.title === "unselected") {
        if (document.getElementById('selected_label').children.length <= 16) {
            // obj.classList.replace("btn-info", "btn-success");
            obj.setAttribute("class", "w3-btn w3-indigo w3-border col-md-3 ");

            obj.setAttribute("title", "selected");
            var show_it = obj.cloneNode(true);
            show_it.innerHTML = obj.innerHTML;
            show_it.setAttribute("id", "show_" + obj.id);
            show_it.setAttribute("title", obj.id + "show_only");
            // show_it.classList.replace("col-md-3", "col-md-12");

            show_it.setAttribute("class", "w3-btn w3-indigo w3-border col-md-12 ");
            document.getElementById("selected_label").appendChild(show_it);
        } else {
            alert('标签数量最大为15！');
        }

    } else if (obj.title === "selected") {

        // obj.classList.replace("btn-success", "btn-info");
        obj.setAttribute("class", "w3-btn w3-white w3-border w3-border col-md-3");

        obj.setAttribute("title", "unselected");
        var shown = document.getElementById("show_" + obj.id);
        document.getElementById("selected_label").removeChild(shown);

    }
    else {
        var cname = obj.id;
        var true_name = cname.substring(5);
        obj.parentElement.removeChild(obj);
        obj = document.getElementById(true_name);
        // obj.classList.replace("btn-success", "btn-info");
        obj.setAttribute("class", "w3-btn w3-white w3-border w3-border col-md-3");
        obj.setAttribute("title", "unselected");
        searchByLabel();

    }
}



function deleteMainStageCourse(courseID) {
    for (var i in window.selectedCourse) {
        if (window.selectedCourse[i]['courseID'] === courseID) {
            window.selectedCourse.splice(i, 1);
            break;
        }
    }
}

// }
function selectCourse(obj) {
    // alert(obj.id);
    var course = window.class_data[parseInt(obj.id)];
    var courseID = course["courseID"];
    var verified;
    var msg;
    if (obj.value === 'selected') {
        obj.innerHTML = "选择课程";
        obj.value = "unselected";
        obj.setAttribute("class", 'w3-btn c5');

        //TODO 课程表删除已选课程的方法
        deleteById(courseID);
    } else {
        $.ajax({
            type: 'GET',
            url: "/checkClass",
            anysc: false,
            data: courseID,  //转化字符串
            contentType: 'application/json',
            dataType: 'json',
            success: function (rdata) { //成功的话，得到消息
                //rdata's type is json
                //returnClass(data);
                verified = rdata[0] === 1;
                msg = rdata[1];


                if (verified) {
                    obj.innerHTML = "取消选择";
                    obj.value = "selected";
                    obj.setAttribute("class", 'w3-btn w3-red');
                    window.selectedCourse.push({'courseID': courseID});
                    insertCard([course]);


                } else {
                    alert(msg)
                }
            }
        });
    }

}

//搜索框回车监听
function enterSubmit(obj) {
    //当enter 键按下后，需要执行的事件
    var button = document.getElementById('search');
    if (obj.keyCode == 13) {
        button.click();
        obj.returnValue = false;
    }
}

//登出方法
function logout() {
    $.ajax({
        type: 'GET',
        url: "/searchLabel",
        anysc: false,
        data: datal,  //转化字符串
        contentType: 'application/json',
        dataType: 'json',
        success: function (rdata) { //成功的话，得到消息
            //rdata's type is json
            //returnClass(data);
        }
    });
}
