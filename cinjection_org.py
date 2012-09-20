#! /usr/bin/python
#-*-coding:gbk-*-
import os
import sys
import re

reload(sys)
sys.setdefaultencoding("gbk")


class CInjection:
	
	def __init__(self):
		self.log_file = '/export/home/www/data/edit_template/1.log'

	def CheckIn(self, files):
		if not re.search("\.php$", files):
			return False
		unsafe_var = []
		f = file(files, 'r')
		ff = file(self.log_file, 'a+')
		line_list = f.readlines()
		for row in range(0, len(line_list)):
			if re.search("\.php$", files) and re.search("\$[a-zA-Z0-9_]{1,}\s*=(?:\s|checkdata\()*\s*\$_(POST|GET|REQUEST|COOKIE)", line_list[row], re.I) and not re.search("int|intval", line_list[row]):
				tmp = re.search("(\$[a-zA-Z0-9_]{1,})\s*=(?:\s|checkdata\()*\s*\$_(POST|GET|REQUEST)", line_list[row], re.I)
				try:
					if tmp:
						hi = tmp.group(1)
						unsafe_var.append(str(hi))
				except:
					pass
			elif re.search("\.php$", files) and re.search("select.*?(?<!')\"\s*\.\s*(\$\w+)\.\s*\"", line_list[row], re.I):
				sql_tmp = re.search("select.*?(?<!')\"\s*\.\s*(\$\w+)\.\s*\"", line_list[row], re.I)
				try:
					sql_var = sql_tmp.group(1)
					if sql_var in unsafe_var:
						ff.write(files + "---line " + str(row + 1) + "：" +line_list[row] + "\r\n")
				except:
					pass
			elif re.search("\.php$", files) and re.search("select.*?(?<!')\s*\{\s*(\$\w+)\s*\}", line_list[row], re.I):
				sql_tmp = re.search("select.*?(?<!')\s*\{\s*(\$\w+)\s*\}", line_list[row], re.I)
				try:
					sql_var = sql_tmp.group(1)
					if sql_var in unsafe_var:
						ff.write(files + "---line " + str(row + 1) + "：" +line_list[row] + "\r\n")
				except:
					pass
			else:
				#print line_list[row]
				pass
		f.close()
		ff.close()
		return True
	
	def getFile(self, path):
		for root, dirs, files in os.walk(path):
			for filepath in files:
				self.CheckIn(os.path.join(root, filepath))
				print 'I am doing ' + os.path.join(root, filepath) + '\r\n'



check = CInjection()
check.getFile("/export/home/www/data/edit_template")

print "done.\r\n"
