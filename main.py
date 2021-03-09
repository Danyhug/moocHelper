# Version 1.0
# Created by Danyhug on 2020-12-30 14:55
# Coding by Danyhug on 2021-01-16 12:00

import requests
import time
import random
import json
import os
import base64
import re
from io import BytesIO
from PIL import Image

userName = 'mapengcheng'  # 用户名
passWord = 'Hh153669225'  # 密码

# 请求头
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) '
                         'Chrome/86.0.4240.75 Safari/537.36'}

# 默认路径
default = os.getcwd()


# 延迟执行
def sleep(t1, t2):
    sleepTime = random.randint(t1, t2)
    print('随机延迟:', sleepTime, '秒')
    time.sleep(sleepTime)


# 保存文件
def saveFile(fileName, answerType, answerText, courseOpenId, courseName, workExamId):
    # 将答案文本进行加密 utf8编码再base64编码 de
    answerText = base64.b64encode(answerText.encode())
    # 判断答案类型进入不同目录 0 作业 1 测验 2 考试
    # 进入答案目录
    if answerType == 0:
        # 作业答案
        os.chdir('answerFile/' + courseOpenId + '/work')
    elif answerType == 1:
        # 测验答案
        os.chdir('answerFile/' + courseOpenId + '/test')
    else:
        # 考试答案
        os.chdir('answerFile/' + courseOpenId + '/exam')
    # 写入二进制数据
    fo = open(fileName + '.hpc', 'wb')
    fo.write(answerText)
    fo.close()
    # 更改dhg文件
    # 返回到课程目录
    os.chdir('..')
    fo = open(courseName + '.dhg', 'r')  # 打开课程文件
    try:
        data = json.loads(fo.read())  # 获得里面的内容
    # 里面可能为空
    except json.decoder.JSONDecodeError:
        data = dict()
    fo.close()  # 关闭
    data[fileName] = workExamId  # 添加新字典
    fo = open(courseName + '.dhg', 'w')
    fo.write(json.dumps(data))  # 将新字典写入
    fo.close()  # 关闭

    # 回到课程路径
    print('courseOpenId', courseOpenId)
    os.chdir(default)
    return '>>> 保存成功'


# 清空目录
def clearDir():
    def c(filePath):
        os.chdir(filePath)
        # 获取当前目录文件
        for file in os.listdir(os.getcwd()):
            os.remove(file)
        print('已删除', filePath, '目录下所有文件')
        os.chdir(default)
    c('answerFile/work')
    c('answerFile/test')
    c('answerFile/exam')


class Mooc:
    # ******URL******
    # 首页
    URL = 'https://mooc.icve.com.cn'
    # 登录
    URL_LOGIN = 'https://mooc.icve.com.cn/portal/LoginMooc/loginSystem'
    # 登录验证码
    URL_LOGIN_VERIFY = 'https://mooc.icve.com.cn/portal/LoginMooc/getVerifyCode'
    # 获取课程列表
    URL_LIST_LESSON = 'https://mooc.icve.com.cn/portal/Course/getMyCourse'
    # 获取正在进行的课程
    URL_LIST_LESSON_ING = 'https://mooc.icve.com.cn/portal/Course/getMyCourse?isFinished=0&page=1&pageSize=999'
    # 获取作业列表
    URL_LIST_WORK = 'https://mooc.icve.com.cn/study/workExam/getWorkExamList'
    # 获取作业信息
    URL_LIST_WORK_INFO = 'https://mooc.icve.com.cn/study/workExam/getWorkExamData'
    # 测验界面
    URL_PAGE = 'https://mooc.icve.com.cn/study/workExam/workExamPreview'
    # 提交答案
    URL_POST_ANSWER = 'https://mooc.icve.com.cn/study/workExam/onlineHomeworkAnswer'
    # 提交答案(填空)
    URL_POST_ANSWER2 = 'https://mooc.icve.com.cn/study/workExam/onlineHomeworkCheckSpace'
    # 让服务器保存答案
    URL_POST_ANSWER_SAVE = 'https://mooc.icve.com.cn/study/workExam/workExamSave'
    # 让服务器保存考试答案
    URL_POST_EXAM_SAVE = 'https://mooc.icve.com.cn/study/workExam/onlineExamSave'
    # 获取测验细节
    URL_GET_EXAM_DETAIL = 'https://mooc.icve.com.cn/study/workExam/detail'
    # 获取答案
    URL_GET_ANSWER = 'https://mooc.icve.com.cn/study/workExam/history'

    # 获取用户信息
    URL_USER_INFO = 'https://mooc.icve.com.cn/portal/LoginMooc/getUserInfo'

    def __init__(self):
        # clearDir()
        self.modelNum = 0  # 模块的数值 作业为0，测验为1，考试为2
        self.answerSave = 'y'  # 是否保存答案 保存为y 不保存为n
        self.funcSwitch = 1  # 功能选择 1获取答案 2答题

        self.session = requests.session()  # 会话状态保持
        self.loginStatus = self.login()  # 登录状态
        self.userid = self.getUserInfo()  # 用户ID
        self.course = ''
        self.question = ''
        self.allQuestion = ''

    def main(self):
        self.start()

    def login(self):
        # userName = input('请输入账号：')
        # passWord = input('请输入密码：')
        codeContent = self.session.get(
            f'{self.URL_LOGIN_VERIFY}?ts={round(time.time() * 1000)}',
            headers=headers).content
        byteIoObj = BytesIO()
        byteIoObj.write(codeContent)
        Image.open(byteIoObj).show()
        verifyCode = input('请输入验证码：')
        data = {
            'userName': userName,
            'password': passWord,
            'verifycode': verifyCode
        }
        res = self.session.post(Mooc.URL_LOGIN, data=data, headers=headers).json()
        if res['code'] == 1:
            return True
        else:
            print(res['msg'])
            return False

    def getUserInfo(self):
        res = self.session.get(Mooc.URL_USER_INFO, headers=headers).json()
        try:
            print('-' * 30)
            print('\t\t欢迎您:', res['displayName'])
            print('-' * 30)
        except:
            print(res['msg'])
            exit(-1)
        return res['id']

    # 获取课程列表
    def getCourseList(self):
        print('\n******进行中的课程列表******')
        print('-' * 30)
        res = self.session.get(
            self.URL_LIST_LESSON_ING,
            headers=headers
        ).json()
        i = 1
        print('序号\t\t课程名')
        for lesson in res['list']:
            print(f'{i:^3}\t\t{lesson["courseName"]}')
            i = i + 1
        inp = int(input('输入序号选择你要完成的课程：'))
        return res['list'][inp - 1]

    # 获取作业信息
    def getWorkExamList(self):
        noSuccessQuestion = list()
        print('-' * 30)
        print('已选择课程：《', self.course['courseName'], '》')

        print('请输入你要使用的功能')
        self.funcSwitch = input('~~1.获取答案 ~~2.开始答题:')
        if self.funcSwitch == '1':
            self.answerSave = (input('是否将答案保存到本地？(y/n):')).lower()
            if self.answerSave == 'y':
                self.answerSave = True
                print('~~~当前选择：保存答案~~~')
            else:
                self.answerSave = False
                print('~~~当前选择：不保存答案~~~')

        print('请输入不需要完成的模块\n1:作业 2:测验 6.全部完成 默认不完成考试')
        try:
            inp = int(input('请输入:'))-1
        except ValueError:
            inp = 2

        for self.modelNum in range(0, 3, 1):
            # print('循环执行')
            if inp == self.modelNum:
                continue
            if self.modelNum == 0:
                print('******当前模块：作业******')
            elif self.modelNum == 1:
                print('******当前模块：测验******')
            elif self.modelNum == 2:
                print('******当前模块：考试******')
            # 作业为0，测验为1，考试为2
            data = {
                'pageSize': 5000,
                'page': 1,
                'workExamType': self.modelNum,
                'courseOpenId': self.course['courseOpenId']
            }
            res = self.session.post(
                self.URL_LIST_WORK,
                data=data,
                headers=headers
            ).json()
            # print(res)
            print(f'序号\t\t{"得分":<5}\t\t{"状态":<6}\t\t测验名')
            i = 1
            # State分为0 1 2 getScore为得分
            # 0 未做
            # 1 批阅
            # 2 已做
            for homework in res['list']:
                def state(s):
                    if s == 0:
                        return '未  做'
                    elif s == 1:
                        return '待批阅'
                    else:
                        return '已  做'

                print(f'{i:^3}\t\t'
                      f'{homework["getScore"]:<5}\t\t'
                      f'{state(homework["State"])}\t\t'
                      f'{homework["Title"]:<}')
                i = i + 1
                # print(homework)

            # print(res['list'])
            # while True:
            #     inp = input('请选择功能(1.获取答案 2.开始做题)：')
            #     if inp == '1':
            #         print('******当前功能：获取答案******')
            #         print('请注意：本功能需要使用当前账号将所选课程全部做一次，然后获取到答案\n'
            #               '在一般课程中不影响，但是在答题次数为限制的课程中，可能会因为超过答题\n'
            #               '次数而无法继续答题\n'
            #               '*一般的最终考试限制为一次，确定要使用此功能吗？')
            #         inp = input('输入1确定，输入其他重新选择:')
            #         if inp == '1':
            #             if input('这是最后一次机会，确定您要使用当前账号将所选课程全部做一次吗？输入1确定:') == '1':
            #                 pass
            #             print('您现在可以重新选择')
            #             continue
            #         else:
            #             print('您现在可以重新选择')
            #             continue
            #     elif inp == '2':
            #         print('******当前功能：开始做题******')
            #     else:
            #         print('输入有误，检查后重新输入')
            #         break

            if self.funcSwitch == '2':
                # 将所有的题存起来
                allQuestion = list()

                def saveQuestion():
                    for index in range(len(res['list'])):
                        allQuestion.append(res['list'][index])
                    # print('未完成的作业有：', noSuccessQuestion)
                saveQuestion()
                # 全部的题
                self.allQuestion = allQuestion  # 测验列表
                self.useLocalAnswer()
                return

            # 将所有未做的题单独存起来
            def saveQuestion():
                for index in range(len(res['list'])):
                    # 未做添加到列表中
                    if res['list'][index]['State'] == 0:
                        noSuccessQuestion.append(res['list'][index])
                # print('未完成的作业有：', noSuccessQuestion)
            saveQuestion()
            self.question = noSuccessQuestion  # 未完成的测验列表
            self.getExamPreview(answer='')
            # 清空未完成的题
            noSuccessQuestion.clear()

    # 提交答案
    def sendQuestion(self, questionId, questionType, uniqueId, answerJson, answer='', online=1):
        if questionType == 4 or questionType == 6:
            online = 0
        data = {
            'questionId': questionId,
            'workExamType': self.modelNum,
            'questionType': questionType,
            'uniqueId': uniqueId,
            'answer': answer,
            'online': online
        }
        # print(data)
        # 如果是填空
        if questionType == 4 or questionType == 5:
            print(answerJson)
            data['answerJson'] = json.dumps(answerJson)
            # print('8888888889填空答案', data['answerJson'], '333')
            # print(questionType, '44444', data)
            # print(json.dumps([{"SortOrder":0,"Content":"sswd2"}]))
            print('sendQuestion data', data)
            print('xxx',self.session.post(
                self.URL_POST_ANSWER2,
                data=data,
                headers=headers
            ).text)
            return

        self.session.post(
            self.URL_POST_ANSWER,
            data=data,
            headers=headers
        )

    # 获取答案
    def getAnswer(self, courseOpenId, workExamId, studentWorkId, workExamType, title):
        data = {
            'courseOpenId': courseOpenId,
            'workExamId': workExamId,
            'studentWorkId': studentWorkId,
            'workExamType': workExamType
        }
        res = self.session.post(
            self.URL_GET_ANSWER,
            data=data,
            headers=headers
        ).json()
        # print('答案json')
        # print(json.loads(res['workExamData'])['questions'])
        # 保存答案
        print(saveFile(
            fileName=title,
            answerType=self.modelNum,
            answerText=res['workExamData'],
            courseOpenId=self.course['courseOpenId'],
            courseName=self.course['courseName'],
            workExamId=res['homework']['Id']
        ))

    # 使用本地答案答题
    def useLocalAnswer(self):
        print('进入useLocalAnswer')
        # 获取本地答案
        # 打开目录
        os.chdir(default + '/answerFile/' + self.course['courseOpenId'])
        # 加载本地json配置文件
        fo = open(self.course['courseName'] + '.dhg', 'r')
        try:
            data = json.loads(fo.read())
            print('无错误')
        except json.decoder.JSONDecodeError:
            data = dict()
            print('有错误', json.decoder.JSONDecodeError)
        print('读取', data)
        for modelNum in range(0, 1, 1):
            if self.modelNum == 0:
                os.chdir('work')
            elif self.modelNum == 1:
                os.chdir('test')
            elif self.modelNum == 2:
                os.chdir('exam')
            print('在这我是正常的', os.getcwd())
            pre = re.compile('>(.*?)<')
            # 遍历目录下的文件
            for file in os.listdir(os.getcwd()):
                print('7777777', file)
                # 遍历配置文件键值
                haveAns = False  # 默认没有答案
                tempQuestion = list()  # 需要做的题
                for conf in data:
                    # print('conf ', conf, ' file ', file)
                    if file == conf+'.hpc':
                        # 本地答案有并且配置文件也有相关数据
                        haveAns = True
                        # 遍历所有课程
                        for index in range(len(self.allQuestion)):
                            # 如果配置文件有本课程
                            if self.allQuestion[index]['Id'] == data[conf]:
                                # 将此文件添加到临时课程
                                tempQuestion.append(self.allQuestion[index])
                                break
                        break
                # 没有答案直接退出本次循环
                if not haveAns:
                    print('没有', file, '答案,填过此测验')
                    continue
                print(file)
                self.question = tempQuestion
                print('useLocal的self.question', self.question)
                # 只读方式打开
                fileContent = open(file, 'r').read()
                # base64 解码 再 utf8解码
                fileContent = base64.b64decode(fileContent).decode()
                jsonContent = json.loads(fileContent)
                # print(jsonContent.keys())
                # questionType 2 客观 1 单选
                # print(jsonContent['questions'][2]['questionType'])
                answer = dict()
                for questionList in jsonContent['questions']:
                    time.sleep(.5)

                    # 判断是否有多个答案 目前用来处理填空题
                    def haveAnswers():
                        answersList = list()
                        print('00000000000', '进入haveAnswers')
                        print(questionList['answerList']), len(questionList['answerList'])
                        # 有多个答案
                        if len(questionList['answerList']) > 1:
                            for answerListItem in questionList['answerList']:
                                print('有多个答案')
                                answersList.append({
                                    'SortOrder': answerListItem['SortOrder'],
                                    'Content': answerListItem['Content']
                                })
                            print(answersList)
                            return answersList
                        return ''.join(pre.findall(questionList['Answer']))

                    # 单选
                    if questionList['questionType'] == 1:
                        abcd = 0
                        abcdOption = list()
                        for answerList in questionList['answerList']:
                            # A B C D
                            if abcd < 4:
                                abcdOption.append(answerList['IsAnswer'])
                            abcd = abcd + 1
                        print('单选答案', abcdOption.index('true'))
                        answer[questionList['questionId']] = abcdOption.index('true')
                    # 多选
                    elif questionList['questionType'] == 2:
                        print('多选答案', questionList['Answer'])
                        answer[questionList['questionId']] = questionList['Answer']
                    # 判断
                    elif questionList['questionType'] == 3:
                        print('判断答案', questionList['Answer'])
                        answer[questionList['questionId']] = questionList['Answer']
                    # 填空
                    elif questionList['questionType'] == 4 or questionList['questionType'] == 5:
                        print('填空答案', ''.join(pre.findall(questionList['Answer'])))
                        # answer[questionList['questionId']] = ''.join(pre.findall(questionList['Answer']))
                        answer[questionList['questionId']] = haveAnswers()
                    # 客观
                    elif questionList['questionType'] == 6:
                        print('客观答案', ''.join(pre.findall(questionList['Answer'])))
                        answer[questionList['questionId']] = ''.join(pre.findall(questionList['Answer']))
                    else:
                        print('未知类型', ''.join(pre.findall(questionList['Answer'])))
                        answer[questionList['questionId']] = ''.join(pre.findall(questionList['Answer']))
                    # html读内容的bug 使用这个临时修补一下
                    if answer[questionList['questionId']] == '':
                        answer[questionList['questionId']] = questionList['Answer']
                        print('修正答案', questionList['Answer'])
                    print('answer', answer)
                self.getExamPreview(answer=answer)
            os.chdir('..')

    # 获取测验有关信息
    def getExamPreview(self, answer):
        # 做作业
        if self.funcSwitch == '2':
            pass
        print('进入getExamPreview', answer)
        print('self.question', self.question)
        # 遍历所有未完成的作业信息
        for index in range(len(self.question)):
            data = {
                'courseOpenId': self.course['courseOpenId'],  # 课程ID
                'workExamId': self.question[index]['Id'],  # 测验ID
                'agreeHomeWork': 'agree',
                'workExamType': self.modelNum  # 测验类型
            }
            # 获取到测验界面当前信息
            res = self.session.post(
                self.URL_PAGE,
                data=data,
                headers=headers
            ).json()
            print('----', res)
            # 默认情况
            if res['workExamData'] != '':
                # 所有题的信息
                questionInfo = json.loads(res['workExamData'])
                # 将所有题依次提交一次
                for i in range(len(questionInfo['questions'])):
                    # print(res['paperData'])
                    # print(res['paperData']['questions'])
                    def answerContent():
                        if self.funcSwitch == '1':
                            return ''
                        # 如果当前列表长度大于1 有可能为多个答案
                        print('Giao', answer)
                        print(answer[questionInfo['questions'][i]['questionId']])
                        # answer为字典 题ID:答案
                        # 判断是否为列表 是列表则有多个答案
                        print('6666666666是否为列表', isinstance(answer[questionInfo['questions'][i]['questionId']], list))
                        print('列表', answer[questionInfo['questions'][i]['questionId']])
                        if isinstance(answer[questionInfo['questions'][i]['questionId']], list):
                            tempAnswer = ''
                            for v in answer[questionInfo['questions'][i]['questionId']]:
                                print('vvv', v)
                                tempAnswer = tempAnswer + ' ' + v['Content']
                            return tempAnswer
                        return answer[questionInfo['questions'][i]['questionId']]
                    print('调用sendQuestion')
                    self.sendQuestion(
                        # questionId=res['paperData']['questions'][index]['questionId'],
                        # questionType=res['paperData']['questions'][index]['questionType'],
                        questionId=questionInfo['questions'][i]['questionId'],
                        questionType=questionInfo['questions'][i]['questionType'],
                        uniqueId=res['uniqueId'],
                        answer='test',
                        answerJson=answerContent()
                        # answerJson=[{
                        #     'SortOrder': 0,
                        #     'Content': answerContent()
                        # }]
                    )
            # 第二种情况
            else:
                # 将所有题依次提交一次
                for i in range(len(res['paperData']['questions'])):
                    # print(res['paperData'])
                    # print(res['paperData']['questions'])
                    def answerContent():
                        if self.funcSwitch == '1':
                            return ''
                        return answer[res['paperData']['questions'][i]['questionId']]
                    self.sendQuestion(
                        questionId=res['paperData']['questions'][i]['questionId'],
                        questionType=res['paperData']['questions'][i]['questionType'],
                        uniqueId=res['uniqueId'],
                        answer=answerContent()
                    )
            # 此时所有题已经做完，向服务器发送保存请求
            # 保存
            if self.modelNum != 2:
                data = {
                    'uniqueId': res['uniqueId'],
                    'workExamId': self.question[index]['Id'],
                    'workExamType': self.modelNum,
                    'courseOpenId': self.course['courseOpenId'],
                    'paperStructUnique': '',
                    'useTime': random.randint(100, 520)
                }
            # 考试模块
            elif self.modelNum == 2:
                data = {
                    'examStudentId': '',
                    'uniqueId': res['uniqueId'],
                    'examId': self.question[index]['Id'],
                    'useTime': random.randint(100, 520),
                    'courseOpenId': self.course['courseOpenId'],
                    'workExamType': self.modelNum,
                }
            else:
                print('程序出错，请联系作者')

            # 发送请求
            if self.modelNum != 2:
                self.session.post(
                    self.URL_POST_ANSWER_SAVE,
                    data=data,
                    headers=headers
                )
            else:
                self.session.post(
                    self.URL_POST_EXAM_SAVE,
                    data=data,
                    headers=headers
                )
            # 作业名
            title = res['homework']['Title']
            print('>>', title, '已提交答案')
            time.sleep(1)
            # 如果是答题模块 直接退出
            if self.funcSwitch == '2':
                print('******当前模块任务完成******')
                break
            # 获取studentWorkId来获得答案
            data = {
                'courseOpenId': self.course['courseOpenId'],
                'workExamId': self.question[index]['Id'],
                'workExamType': self.modelNum
            }
            res = self.session.post(
                self.URL_GET_EXAM_DETAIL,
                data=data,
                headers=headers
            ).json()
            self.getAnswer(
                courseOpenId=self.course['courseOpenId'],
                workExamId=res['list'][0]['WorkExamId'],
                studentWorkId=res['list'][0]['Id'],
                workExamType=self.modelNum,
                title=title
            )
            print('细节：', res)
            print(res['list'])
            sleep(5, 10)
        print('******当前模块任务完成******')

    def start(self):
        while True:
            os.chdir('answerFile')
            self.course = self.getCourseList()  # 选中的课程信息字典
            print('课程名', self.course['courseOpenId'])

            try:
                os.mkdir(self.course['courseOpenId'])
                os.mkdir(self.course['courseOpenId'] + '/work')
                os.mkdir(self.course['courseOpenId'] + '/test')
                os.mkdir(self.course['courseOpenId'] + '/exam')
                print('新建目录：', self.course['courseOpenId'], '属于课程->', self.course['courseName'])
            except FileExistsError:
                print('检测到目录存在：', self.course['courseOpenId'], '不进行创建')
            # 进入课程目录
            os.chdir(self.course['courseOpenId'])
            open(self.course['courseName'] + '.dhg', 'a').close()

            # 回到默认路径
            os.chdir(default)

            self.getWorkExamList()
            print('******课程《', self.course['courseName'], '》已完成')
            # 回到默认路径
            os.chdir(default)
            print('课程字典：', self.course)
            print('测验列表：', self.question)


if __name__ == '__main__':
    print('** ' * 13)
    print('- - - 智慧职教 MOOCHelper 内测V1.0.0 - - -')
    print('- - -         By Danyhug           - - -')
    print('=====内部使用                 请勿外传=====')
    print('** ' * 13)
    Mooc().main()
    pass
