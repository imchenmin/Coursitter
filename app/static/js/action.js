var class_data=[{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
},{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
},{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
},{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
},{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
},{
    "class_id": "1",
    "class_name": "2",
    "credit": "3",
    "lecture": "4",
    "capacity": "5",
    "current_number": "6"
}];
window.onload = function () {
    document.getElementById("commit_Edit").style.display = "none";
    document.getElementById("all_label").style.display = "none";
    var labels_obj = generate_labels();
    for (var label in labels_obj) {
        document.getElementById("all_label").appendChild(labels_obj[label]);
    }

};



$(document).ready(function () {
    var class_data=[{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    },{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    },{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    },{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    },{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    },{
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    }];
    $('#class_table').bootstrapTable({
        data:class_data,
            editable:true,//开启编辑模式
            clickToSelect: true,
            cache: false,
            // showToggle:true, //显示切换按钮来切换表/卡片视图。
            // showPaginationSwitch:true, //显示分页切换按钮
            pagination: true,
            classes:'table-no-bordered',
            pageList: [25],
            pageSize:15,
            pageNumber:1,
            uniqueId: 'index', //将index列设为唯一索引
            striped: true,
            // search: true,
            height:650,
            // showRefresh: true,
            minimumCountColumns: 2,
            smartDisplay:true,
        onClickRow:function (row,$element) {
            // alert(row.html);
            $('#myModal').modal('show');
            // $('.info').removeClass('info');//移除class
            // $($element).addClass('info');//添加class
            // $('.course_card').css("display", "inline-block");
        },
        columns: [{
            field: 'class_id',
            title: '课程编号'
        }, {
            field: 'class_name',
            title: '课程名称'
        }, {
            field: 'credit',
            title: '学分'
        }, {
            field: 'lecturer',
            title: '任课教师'
        }, {
            field: 'capacity',
            title: '课程容量'
        }, {
            field: 'current_number',
            title: '已选人数'
        },
        ],

    });
});


function search_class() {
    var data = {
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "lecturer":"ZLDNB",
        "capacity": "5",
        "current_number": "6"
    };
    $('#class_table').bootstrapTable('prepend', class_data);

}

function showFullLabel() {
    document.getElementById("label").classList.replace("col-md-1", "col-md-8");
    document.getElementById("Edit").style.display = "none";
    document.getElementById("commit_Edit").style.display = "inline";
    document.getElementById("all_label").style.display = "inline";
    document.getElementById("selected_label").classList.replace("col-md-12", "col-md-2");

    var data = {
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    };
    $('#class_table').bootstrapTable('prepend', data);


}

function showSelectedLabel() {
    document.getElementById("label").classList.replace("col-md-8", "col-md-1");
    document.getElementById("commit_Edit").style.display = "none";
    document.getElementById("Edit").style.display = "inline";
    document.getElementById("all_label").style.display = "none";
    document.getElementById("selected_label").classList.replace("col-md-2", "col-md-12");

}

function generate_labels() {
    var labels_title = {"grade": "面向年级", "character": "课程性质", "department": "开课院系", "week": "星期", "time": "节次"};
    var labels = {
        "grade": "大一 大二 大三 大四",
        "character": "必修 选修",
        "department": "通识基础部 数学系 物理系 化学系 生物系 计算机系 电子系 地空系 海洋系 材料系 环境系 机械系 生医工系 金融系 人文中心 社科中心 语言中心 艺术中心 体育中心",
        "week": "星期一 星期二 星期三 星期四 星期五 星期六 星期日",
        "time": "1-2节 3-4节 5-6节 7-8节 9-10节 11节"
    };

    var labels_obj = [];
    for (var i in labels) {
        var l_obj = document.createElement('div');
        l_obj.classList.add("label_set");
        l_obj.classList.add("col-md-6");
        var ls = labels[i].split(" ");
        var title_obj = document.createElement("h4");
        title_obj.innerHTML = labels_title[i];
        title_obj.classList.add("label_title");
        l_obj.appendChild(title_obj);
        for (var j in ls) {
            // <button id="Edit" type="button" class="btn btn-primary " onclick="showFullLabel()">编辑</button>

            var label_name = ls[j];

            var single_label = document.createElement("button");
            // single_label.id = label_name;
            single_label.classList.add("btn");
            single_label.classList.add("btn-info");
            single_label.classList.add("col-md-3");
            // single_label.classList.add("label_button");
            single_label.setAttribute("onclick", "select_label(this)");
            single_label.setAttribute("title", "unselected");
            single_label.setAttribute("id", label_name);
            single_label.innerHTML = label_name;
            l_obj.appendChild(single_label);

            // single_label.classList.add("col-md-3");
        }


        labels_obj.push(l_obj);
        // var br = document.createElement("br");
        // labels_obj.push(br);
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
    if (obj.title === "unselected") {
        obj.classList.replace("btn-info", "btn-success");
        obj.setAttribute("title", "selected");
        var show_it = obj.cloneNode(true);
        show_it.innerHTML = obj.innerHTML;
        show_it.setAttribute("id", "show_" + obj.id);
        show_it.setAttribute("title", obj.id + "show_only");
        show_it.classList.replace("col-md-3", "col-md-12");
        document.getElementById("selected_label").appendChild(show_it);

    } else if (obj.title === "selected") {

        obj.classList.replace("btn-success", "btn-info");
        obj.setAttribute("title", "unselected");
        var shown = document.getElementById("show_" + obj.id);
        document.getElementById("selected_label").removeChild(shown);
    }
    else {
        var cname = obj.id;
        var true_name = cname.substring(5);
        document.getElementById("selected_label").removeChild(obj);
        obj = document.getElementById(true_name);
        obj.classList.replace("btn-success", "btn-info");
        obj.setAttribute("title", "unselected");
    }

}

function add_class_row() {
    return {
        "class_id": "1",
        "class_name": "2",
        "credit": "3",
        "lecture": "4",
        "capacity": "5",
        "current_number": "6"
    };
}


function show_class_card(obj) {

    alert("AMD!yes!")
}