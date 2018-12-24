window.data = {};
window.rcoin = 10000;
// data = {
// 	CS304:{
// 		"coin": 50,
// 		"classnum": 2
// 	}
// }
// 

function insertCard(course, history) {
  var oUl_course = document.getElementById('courseList');
  // var testCourse = getInfo();
  for (var i = 0; i < course.length; i++) {
    var oLi = document.createElement('li');
    oLi.innerHTML = addCourse(course[i]);
    oUl_course.appendChild(oLi);
  }
  if (history){
    simulationClick(history);
    //course的结构是{courseid:{coin:123, classnum: 100}, ...}
  }
}

function addCourse(testCourse) {
	var res = "";
	var oCourse;
	var courseName = testCourse.courseName;
	var courseID = testCourse.courseID;
	var classes = testCourse.classes;
	res += "<div class=\"mycard\"><div class=\"card\"><div class=\"card-header\" onclick=removeLi(this)>";
	res += courseID + " " + courseName;
	res +=
		"</div><div class=\"card-body\"><div id=\"courses\" class=\"course-selector\"><ul style=\"list-style: none; margin-left:-43px; \">";
	for (var clz in classes) {
		oCourse = new Classes(courseName, classes[clz].teachers, classes[clz].classinfo, classes[clz]
			.period, testCourse.courseID, classes[clz].classnum);
		res += addClass(oCourse);
	}
	res +=
		"</ul></div></div><div class=\"card-footer\"><p class=\"replacer\"></p><input type=\"text\" class=\"mytxt\" id=\"coin\" placeholder=\"请输入选课币\"></div></div></div>";
	
		return res;
}

function addClass(oCourse) {
	var res = "";
	res += "<li><div class=\"class-selector\" data-period=" + oCourse.period + " data-coursename=\"" + oCourse.courseName +
		"\" data-courseid=\"" + oCourse.courseID + "\" data-classinfo=\"" + oCourse.classinfo + "\" data-classnum=\"" +
		oCourse.classnum + "\" data-teachers=\"" + oCourse.teachers + "\">";
	for (i in oCourse.classinfo){
		res += "<p>" + oCourse.classinfo[i] + "</p>";
	}
	res += "<p>任课教师：" + oCourse.teachers + "</p>";
	res +="<input class=\"btn mybtn-select\" type=\"button\" name=\"btn\" id=\"btn\" value=\"select\" onclick=fillTable(this) /></div></li>";

	return res;
}
	
function fillTable(obj) {
	oDiv = obj.parentElement;
	oUl = oDiv.parentElement.parentElement;
	aBtns = oUl.getElementsByClassName('btn mybtn-select-active');
	period = oDiv.dataset.period.split(',');
	name = oDiv.dataset.coursename;
	id = oDiv.dataset.courseid;
	info = oDiv.dataset.classinfo.split(',');
	teachers = oDiv.dataset.teachers;
	classnum = oDiv.dataset.classnum;
	oCard = oUl.parentElement.parentElement.parentElement;
	ot = document.getElementById("classtable");
	aIn = oCard.getElementsByClassName('mytxt');
	aReplacer = oCard.getElementsByClassName('replacer');
	coin = aIn[0].value;
	classinfo = '';
	for (i in info){
		classinfo += "<p>" + info[i] + "</p>";
	}
	if (coin == '') {
		alert("您还未分配选课币！")
		return;
	} else if (isNaN(coin) || coin < 0) {
		alert("请输入一个正整数!")
		return;
	} 

	if (obj.className == "btn mybtn-select-active") {
		clearThisClass(ot, period);
		obj.setAttribute("class","btn mybtn-select");
		window.rcoin += parseInt(window.data[id].coin);
		postData('DELETE', window.data[id]);
		console.log('delete'+JSON.stringify(window.data[id]));
		delete window.data[id];
		aIn[0].setAttribute('style', 'display:unset');
		aReplacer[0].setAttribute('style','none');
	} else {
		//判断课程冲突
		if (hasConflict(ot, name, period)) {
			return;
		}
		//判断选课币是否充足
		if(window.data[id]){
			var courseCoin = window.data[id].coin;
			if (coin - courseCoin > rcoin){
				alert("当前选课币不足！当前余额：" + rcoin)
			return;
			}
		}else{
			if (coin > rcoin) {
				alert("当前选课币不足！当前余额：" + rcoin)
				return;
			}
		}

		//清除该课程选中的班级信息
		clearCourse(ot, aBtns);

		//添加当前选中班级信息
		tempcolor = getRandomColor();
		for (var i = 0; i < period.length;) {
			var rown = parseInt(period[i + 1] - 1);
			var celln = parseInt(period[i]);
			if (rown >= 2) rown++;
			else if (rown >= 5) rown++;
			ot.rows[rown].cells[celln].innerHTML = "<p>" + name + "</p>" + "<p>" + teachers + "</p>" + classinfo;
			ot.rows[rown].cells[celln].setAttribute("style",tempcolor);
			i += 2;
		}
		obj.setAttribute("class","btn mybtn-select-active")

		console.log(window.data)
		window.data[id] = {
			"coin": coin,
			"classnum": classnum
		}
		
		window.rcoin -= parseInt(coin);
		postData('ADD', window.data[id]);
		console.log('post '+JSON.stringify(window.data[id]));
		
		// 选中课程禁止修改选课币
		aIn[0].setAttribute('style', 'display:none')
		aReplacer[0].innerHTML = "已设定选课币："+coin;
		aReplacer[0].setAttribute('style','display:unset');
	}
	updateRcoin();
}

function removeLi(obj) {
	oDiv = obj.parentElement.parentElement;
	oLi = oDiv.parentElement;
	oUl = oLi.parentElement;
	ot = document.getElementById("classtable");
	id = oDiv.getElementsByClassName('class-selector')[0].dataset.courseid;
	aBtns = oDiv.getElementsByClassName('btn mybtn-select-active');
	//移除课程的时候课表更新！！！！！！！！！！
	clearCourse(ot, aBtns);

	// 这里应该要退还所有的coin```````````````````````
	if (window.data[id]) {
		// window.rcoin += parseInt(window.data[id].coin)
		postData('DELETE', window.data[id]);
		console.log('delete'+JSON.stringify(window.data[id]));
		delete window.data[id];
	}
	oDiv.innerHTML = '';
	startMove(oDiv, 'height', 0);
	setTimeout("oUl.removeChild(oLi);", 2000);
	updateRcoin();

}

function clearCourse(ot, aBtns) {
	for (var i = 0; i < aBtns.length; i++) {
		var tempperiod = aBtns[i].parentElement.dataset.period.split(',');
		aBtns[i].setAttribute("class","btn mybtn-select")

		for (var i = 0; i < tempperiod.length;) {
			var rown = parseInt(tempperiod[i + 1] - 1);
			var celln = parseInt(tempperiod[i]);
			if (rown >= 2) rown++;
			else if (rown >= 5) rown++;
			ot.rows[rown].cells[celln].innerHTML = "";
			ot.rows[rown].cells[celln].setAttribute("style","background-color:none");
			i += 2;

		}
		window.rcoin += parseInt(window.data[id].coin);
		postData('ADD', window.data[id]);
		updateRcoin();
		console.log('post '+JSON.stringify(window.data[id]));
	}
}

function clearThisClass(ot, period) {
	for (var i = 0; i < period.length;) {
		var rown = parseInt(period[i + 1] - 1);
		var celln = parseInt(period[i]);
		if (rown >= 2) rown++;
		else if (rown >= 5) rown++;
		ot.rows[rown].cells[celln].innerHTML = "";
		ot.rows[rown].cells[celln].setAttribute("style","background-color:none");
		i += 2;
	}
}

function hasConflict(ot, name, period) {
	for (var i = 0; i < period.length;) {
		var rown = parseInt(period[i + 1] - 1);
		var celln = parseInt(period[i]);
		if (rown >= 2) rown++;
		else if (rown >= 5) rown++;
		if (ot.rows[rown].cells[celln].innerHTML != "" ) {
			temp = ot.rows[rown].cells[celln].firstElementChild.innerHTML;
			if(name != temp){
				alert("与课程 " + temp + " 冲突，请修改班级！")
				return true;
			}
		}
		i += 2;
	}
	return false;
}

function updateRcoin(){
	var oDiv = document.getElementById("show-coin");
	oDiv.innerHTML = "余币量：" + window.rcoin;
}

function getRandomColor(){
	colorset = ["#e1e3ff", "#f1e1ff", "#f8e1ff", "#ffe1e1","#e1fffe", "#e1ffe2", "#feffe1","#fff4e1", "#fee1ff"];
	a = Math.floor(colorset.length*Math.random());
	return "border: 1px solid #e0e0e0; background-color:"+colorset[a];
}
function simulationClick(course){
  oList = document.getElementById('courseList');
  aCards = document.getElementsByClassName('card');
  for (var i = 0; i < aCards.length; i++) {
    tempid = aCards[i].firstElementChild.innerHTML.split(' ')[0];
    tempcoin = course[tempid].coin;
    tempclassnum = course[tempid].classnum;
    tempinput = aCards[i].getElementsByClassName('mytxt')[0];
    tempinput.value = tempcoin;
    aClasses = aCards[i].getElementsByClassName('class-selector');
    for (var j = 0; j < aClasses.length; j++){
      if(aClasses[j].data.classnum == tempclassnum){
        var clickEvent=new MouseEvent('click',{
          altKey:true // 模拟alt键按下
        });
        aClasses[j].getElementById('btn').dispatchEvent(clickEvent); // 派发
      }
    }
  }
}
function postData(_type, _data){
	$.ajax({
		type: "POST",
		url: "/class"+_type,
		anysc: false,
		data: JSON.stringify(_data),
		contentType: 'application/json; charset=UTF-8',
		dataType:'json',
		seccess: function(data){
			
		}
	});
}