#!/usr/local/bin/python3.6

'''
编写目的：
	学校机房的devc++只识别gb2312的文件，所以在弄过去的时候，要转码。
输入：

'''
import os
import chardet

# 检索这个文件夹下 的后缀相符的文件。
# 返回 他们的绝对路径
def All_Files(dirName,postfix=['.txt','.cpp','.c','.h']):
	Files = []
	Dirs = []
	if not(os.path.exists(dirName)):
		print("\n ##!! the dir is not exists! !!##")
		print(" \t",dirName)
		return Files

	for x in os.walk(dirName):
		absdir = os.path.abspath(x[0])
		Files += [ os.path.join(absdir,i) for i in x[2] if(i[0]!='.' and (os.path.splitext(i)[1] in postfix) )  ]

	return Files
#检查:
#for i in All_Files("/Users/luo-banqi/Desktop/cprogram"):
#	print(i)


# 把一个文件转换成其他格式，要用比特的方式读入，然后写的时候也要用b，
# 不用b的话，在read的时候就会按照utf-8解码，就会抛出错误。
#TurnGDB(filename,'utf-8')
def TurnGDB(filename,tocode='gb2312'):
	# 如果 传入参数filenamae的文件存在，就执行
 
	try:
		f = open(filename,'rb')
		s = f.read()
		f.close()
		#分析 这个f文件的编码方式。
		enc=chardet.detect(s)
		codeType=enc['encoding']
		#然后 按照这个编码方式来解码。再用tocode的编码方式编码。
		s = s.decode(codeType)
		s = s.encode(tocode)
		#最后，把编号的东西给写入文件。
		f = open(filename,'wb')
		f.write(s)
		f.close()
		print(' turn file form:(', codeType, ') to (',tocode,') successful,')
		print(' 	filename: ',os.path.split(filename)[1])
		return True
	except:
		f.close()
		print('\n ##!! turning file while error happened !!## ')
		print(' 	',filename)
		return False	 
#检查：
#TurnGDB("/Users/luo-banqi/testfile/hel.txt","utf-8")


# 复制文件。
def CopyFile(fromfile,tofile):
	#如果文件路径相同，就出错。
	if(fromfile == tofile):
		print(' ##!! CopyFile: fromfile == tofile, so break. !!## ')
		return False

	#改文件名，一直到tofile是不存在的。
	name,post = os.path.splitext(tofile)
	while(os.path.exists(name+post)):
		name+='2'
	tofile = name+post

	try:
		ff = open(fromfile,'rb')
		tt = open(tofile,'wb')
		while True:
			buff = ff.read(1024)
			if( not buff ):
				break;
			tt.write(buff)
		ff.close()
		tt.close()
		#print(' copy file successful. ')
		return True
	except:
		ff.close()
		tt.close()
		print(' ##!! copying file while error raise! !!## ')
		print(' 	from file:',os.path.split(fromfile)[1],'to file: ',os.path.split(tofile)[1])
		return False
#检查:
#file = "/Users/luo-banqi/testfile/hel.txt"
#file2 = "/Users/luo-banqi/Desktop/hel.txt"
#CopyFile(file,file2)



# 拷贝整个文件夹。返回：拷贝的文件下有几个文件，几个文件夹。
# fromDir 是要拷贝的， ToDir是拷贝到的地方，ToDir是要不存在的，copy_invisible: 是不是要拷贝隐藏文件。
def CopyDir(fromDir,ToDir,copy_invisible=False):
	file_num = 0
	dir_num = 0
	if (os.path.exists(fromDir)) and fromDir!=ToDir and (not os.path.exists(ToDir)):
		os.mkdir(ToDir)
		#print( 'making a dir: ',ToDir,)
		#遍历这个文件夹里面的每一个项。判断每个项的类别。
		#拷贝文件，创建文件夹
		for file in os.listdir(fromDir):
			if file[0]=='.' and not copy_invisible:
				continue
			source = os.path.join(fromDir,file)
			target = os.path.join(ToDir,file)
			if os.path.isfile(source):
				if(CopyFile(source,target)):
					file_num+=1
			if os.path.isdir(source):
				ans = CopyDir(source,target)
				file_num += ans[0]
				dir_num  = dir_num+ans[1]+1
	else:
		print('\n ##!! copy dir fail! !!## ')
		print(' \tfromdir:',fromDir)
		print(' \ttodir:  ',ToDir)
		
	return file_num,dir_num

#dd = '/Users/luo-banqi/testfile'
#d2 = '/Users/luo-banqi/Desktop/testfile2'
#print(CopyDir(dd,d2,True))

dirname = input('\n 输入要 转换的 (文件\文件夹) 的路径，不要有转义反斜杠。\n')
ccdir = dirname + '-copy'
CopyDir(dirname,ccdir,True)
for file in All_Files(ccdir):
	TurnGDB(file)

