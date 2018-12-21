function Classes(courseName, teachers, classtime, classroom, period) {
	/**
	 * teachers, classtime, classroom 都是string，用于调取直接在插入的div上显示
	 * 格式示例：人工智能", "周二3-4/周五5-6", "荔园1栋101/荔园6栋403", "唐柯/赵耀
	 * period是一个二维数组，是将class time转换成一个可读取的数字用的数组[[2,3][5,3]]代表周二第三大节和周五第三大节
	 * coins默认为0；
	 */
	this.courseName = courseName;
	this.teachers = teachers;
	this.classtime = classtime;
	this.classroom = classroom;
	this.period = period;
	this.coins = 0;
}

function getInfo() {
	var testCourse = {
		"courseName": "人工智能",
		"classes": [{
				"teachers": "tk / zy",
				"classtime": "1 2 / 3 4",
				"classroom": "ly1d101 / ly6d403",
				"period": [1,2]
			},
			{
				"teachers": "tk / zy",
				"classtime": "2 3 / 5 4",
				"classroom": "ly1d101 / ly6d403",
				"period": [2,3, 5,4]
			},
			{
				"teachers": "tk / zy",
				"classtime": "3 3 / 4 3",
				"classroom": "ly1d101 / ly6d403",
				"period": [3,3,4,3]
			}
		]
	}

	return testCourse;
}
