function Classes(courseName, teachers, classinfo, period, id, num) {
	/**
	 * teachers, classtime, classroom 都是string，用于调取直接在插入的div上显示
	 * 格式示例：人工智能", "周二3-4/周五5-6", "荔园1栋101/荔园6栋403", "唐柯/赵耀
	 * period是一个二维数组，是将class time转换成一个可读取的数字用的数组[[2,3][5,3]]代表周二第三大节和周五第三大节
	 * coins默认为0；
	 */
	this.courseName = courseName;
	this.teachers = teachers;
	this.classinfo = classinfo;
	this.period = period;
	this.courseID = id;
	this.classnum = num;
	this.coins = 0;
}

//log 取消classtime和classroom，换成classinfo
function getInfo() {
	var testCourse = [{
			"courseName": "人工智能",
			"courseID": "CS304",
			"classes": [{
					"teachers": "唐柯",
					"classinfo": ["周二3-4节 荔园一栋101","周五5-6节 荔园6栋403"],
					"classnum": 101,
					"period": [2, 2, 5, 3]
				},
				{
					"teachers": "唐柯",
					"classinfo": ["周二3-4节 荔园一栋101","周三5-6节 荔园6栋403"],
					"classnum": 101,
					"period": [2, 2, 3, 3]
				}
			]
		},
		{
			"courseName": "面向对象",
			"courseID": "CS303",
			"classes": [{
				"teachers": "张誉群",
					"classinfo": ["周四3-4节 荔园一栋101","周三5-6节 荔园6栋403"],
					"classnum": 101,
					"period": [4, 2, 3, 3]
			}]
		}
	]

	return testCourse;
}
