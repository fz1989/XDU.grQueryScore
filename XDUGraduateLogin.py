import re
import urllib2
import urllib
import cookielib
def autoLogin(username, pwd):
	'''处理自动登录的脚本，返回的是学号和个人的课程编号'''
	cookie=cookielib.CookieJar()
	cj=urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cj)
	postdata = {'j_username':username,
				'j_password':pwd,
				}
	#登录的第一步
	req = urllib2.Request('http://210.27.12.1:90/student/index.jsp')
	operate = opener.open(req)
	#登录的第二步，填写用户名和密码
	req = urllib2.Request('http://210.27.12.1:90/j_security_check', urllib.urlencode(postdata))
	operate = opener.open(req)
	#登录成功，获取课程编号
	req = urllib2.Request('http://210.27.12.1:90/viewStudyPlanAction.do')
	list = []
	p = re.compile(r'\d{7}')
	operate = opener.open(req)
	for m in p.finditer(operate.read()):
		list.append(m.group())
	list = list[1:]
	
	#登录成功，获取学号
	req = urllib2.Request('http://210.27.12.1:90/student/main.jsp')
	operate = opener.open(req)
	p = re.compile(r'xdleess\d{8}sn\d{4}')
	content = operate.read()
	match = p.search(content)
	
	#登录成功，获取整体信息
	p = re.compile(r'\d+\.\d+')
	info = {};
	val = p.findall(content)
	info[u'全部额定学分'] = val[0];
	info[u'全部额定学分已完成'] = val[1];
	info[u'学位课额定学分'] = val[2];
	info[u'学位课额定学分已完成'] = val[3];
	info[u'学位课加权平均分'] = val[4];
	return list, match.group(),info
