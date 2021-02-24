import requests,json
import unittest
import random

# 添加新用户接口
url = 'https://bizmate-poc.sinosun.com:17443/bizmate/user/v1/addInfo'

# 获取token
url2 = 'https://bizmate-poc.sinosun.com:17443/auth/realms/UCCB-pro/verification_codes/test'
Token = requests.get(url2)
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    "Authorization": "Bearer " + Token.text
}

# 新建企业接口
url3 = 'https://bizmate-poc.sinosun.com:17443/bizmate/user/v1/addOrganization'

# 企业添加人员接口
url4 = 'https://bizmate-poc.sinosun.com:17443/bizmate/user/v1/addOrganizationUser'

# 预置考勤组
url5 = 'https://bizmate-poc.sinosun.com:17443/bizmate/attendance/v1/setAttendanceGroup'

# 考勤打卡
url6 = 'https://bizmate-poc.sinosun.com:17443/bizmate/attendance/v1/clock'



# 随机生成手机号码
class PhoneNOGenerator():
    def phoneNORandomGenerator(self):
        prelist=["130","131","132","133","134","135","136","137","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
pg = PhoneNOGenerator()


class TestRegister(unittest.TestCase):
    # 注测接口测试用例类
    def test_register_succsess(self):
        # 注测成功case
        data1 = {
            "mobile": pg.phoneNORandomGenerator()    # 手机号调用随机生成值
        }
        r1 = requests.post(url, data1)
        print(r1.text)
        # 断言
        # expected = {
        #     "result": {
        #         "bizMateId": "8619999367876@uccb-pro"
        #  },
        #     "resultMessage": "执行成功",
        #     "resultCode": 0
        # }
        result1 = r1.json()['resultCode']  # 把测试数据传到被测代码
        self.assertEqual(0, result1)  # 断言一致即通过

        return r1.json()['result']['bizMateId']

        # r1对象实例化，使用该人员新创建企业时，调用r1中result中的bizMateId
        # def __init__(self, r1):
        #     self.r1 = r1

    def test_register_isnull(self):
        # 手机号参数为空case
        data2 = {
            "mobile": ""
        }
        r2 = requests.post(url, data2)
        print(r2.text)
        # excepted = {
        #     "result": null,
        #     "resultMessage": "电话号码或者用户名 密码为空",
        #     "resultCode": 80116002
        # }
        result2 = r2.json()['resultCode']
        self.assertEqual(80116002, result2)

    def test_register_overlap(self):
        # 用户手机号重复case
        data3 = {
            "mobile": "13886321625"
        }
        r3 = requests.post(url, data3)
        print(r3.text)
        # excepted = {
        #     "result": {
        #         "bizMateId": "8619999363200@uccb-pro"
        #     },
        #     "resultMessage": "用户信息已存在",
        #     "resultCode": 80116301
        # }
        result3 = r3.json()['resultCode']
        self.assertEqual(80116301, result3)

# 获取bizMateId
bizMateId = TestRegister().test_register_succsess()

class TestAddOrganization(unittest.TestCase):
    # 新建企业成功case
    def test_addOrganization_success(self):
        data = {
            "orgName": "测试企业"+pg.phoneNORandomGenerator(), # 随机生成企业名称
            "bizMateId": bizMateId,  # 使用随机新增用户生成的bizMateId
            "industryType": "INTERNET_ELECTRONICS",
            "employeesCount": "SIX"
        }

        r4 = requests.post(url3, data=json.dumps(data), headers=headers)
        print(r4.text)
        result4 = r4.json()['resultCode']
        self.assertEqual(0, result4)

        return r4.json()['result']['orgId']



    # 企业名为空case
    def test_orgName_null(self):
        data = {
        "orgName": "",
        "bizMateId": bizMateId,
        "industryType": "INTERNET_ELECTRONICS",
        "employeesCount": "SIX"
        }


        r5 = requests.post(url3, data=json.dumps(data), headers=headers)
        print(r5.text)
        result5 = r5.json()['resultCode']
        self.assertEqual(80116002, result5)

    # 企业名称重复case
    def test_orgName_overlap(self):
        data = {
            "orgName": "测试企业00001",
            "bizMateId": bizMateId,
            "industryType": "INTERNET_ELECTRONICS",
            "employeesCount": "SIX"
        }


        r6 = requests.post(url3, data=json.dumps(data), headers=headers)
        print(r6.text)
        result6 = r6.json()['resultCode']
        self.assertEqual(80116101, result6)

    # 企业创建者为空case
    def test_bizMateId_null(self):
        data = {
            "orgName": "测试企业00001",
            "bizMateId": "",
            "industryType": "INTERNET_ELECTRONICS",
            "employeesCount": "SIX"
        }

        r7 = requests.post(url3, data=json.dumps(data), headers=headers)
        print(r7.text)
        result7 = r7.json()['resultCode']
        self.assertEqual(80116002, result7)

    # 企业名不能包含“/”case
    def test_orgName_wrong(self):
        data = {
            "orgName": "/",
            "bizMateId": bizMateId,
            "industryType": "INTERNET_ELECTRONICS",
            "employeesCount": "SIX"
        }

        r8 = requests.post(url3, data=json.dumps(data), headers=headers)
        print(r8.text)
        result8 = r8.json()['resultCode']
        self.assertEqual(80116002, result8)

# 获取orgId
orgId = TestAddOrganization().test_addOrganization_success()

class TestAddOrgUser(unittest.TestCase):
    # 企业添加人员成功case
    def test_addOrgUser_susscess(self):
        data = {
            "bizMateId": bizMateId,
            "orgId": orgId,
            "targetBizMateId": "8619999367889@uccb-pro",
            "name": "lichenglong"
        }

        r9 = requests.post(url4, data=json.dumps(data), headers=headers)
        print(r9.text)
        result9 = r9.json()['resultCode']
        self.assertEqual(0, result9)


    # 企业创建者ID为空case
    def test_bizMateId_null(self):
        data = {
            "bizMateId": "",
            "orgId": orgId,
            "targetBizMateId": "8619999367889@uccb-pro",
            "name": "lichenglong"
        }

        r10 = requests.post(url4, data=json.dumps(data), headers=headers)
        print(r10.text)
        result10 = r10.json()['resultCode']
        self.assertEqual(80116002, result10)

    # 企业ID为空case
    def test_orgId_null(self):
        data = {
            "bizMateId": bizMateId,
            "orgId": "",
            "targetBizMateId": "8619999367889@uccb-pro",
            "name": "lichenglong"
        }

        r11 = requests.post(url4, data=json.dumps(data), headers=headers)
        print(r11.text)
        result11 = r11.json()['resultCode']
        self.assertEqual(80116002, result11)

    # 新增用户ID为空case
        def test_targetBizMateId_null(self):
            data = {
                "bizMateId": bizMateId,
                "orgId": orgId,
                "targetBizMateId": "",
                "name": "lichenglong"
            }

            r12 = requests.post(url4, data=json.dumps(data), headers=headers)
            print(r12.text)
            result12 = r12.json()['resultCode']
            self.assertEqual(80116302, result12)

    # 企业已存在case
    def test_targetBizMateId_overlap(self):
        data = {
            "bizMateId": bizMateId,
            "orgId": "77386395-2b2b-4a9a-9743-338a6e81a8b5",
            "targetBizMateId": "8619999367889@uccb-pro",
            "name": "李成龙"
        }

        r13 = requests.post(url4, data=json.dumps(data), headers=headers)
        print(r13.text)
        result13 = r13.json()['resultCode']
        self.assertEqual(80116104, result13)



class ClockTest(unittest.TestCase):
    # 预制考勤组数据case
    def test_clock_data(self):
        data = {
          "userId": bizMateId,
          "companyId": orgId,
          "attenGroupInfo": {
            "groupId": 1,
            "groupName": "全参数新建考勤组",
            "attenMode": {
              "wifiList": [
                {
                  "macAddr": "b0:f9:63:87:f9:f0",
                  "wifiName": "sinosun-mobile"
                }
              ],
              "monetList": [
                {
                  "longitude": 114028123,
                  "latitude": 22536189,
                  "regionName": "深圳市福田区车公庙泰然大厦C座",
                  "radius": 1000
                }
              ],
              "faceRecongizeFlag": 2
            },
            "classType": 1,
            "classInfoList": [
              {
                "workStartTime": 1592870400,
                "workEndTime": 1592902800,
                "workdays":["Mon","Tue","Wed","Thu","Fri"],
                "flexibleWork": {
                  "permitLateTime": 10
                }
              }
            ],
            "isPushReminder": True,
            "supplyClockMaxTimes": 3,
            "isFlexibleWork": False
          }
        }

        r14 = requests.post(url5,json.dumps(data), headers=headers)
        print(r14.text)
        result14 = r14.json()['resultCode']
        self.assertEqual(0, result14)

    # GPS考勤打卡成功case
    def test_gps_success(self):
        data = {
          "userId": bizMateId,
          "companyId": orgId,
          "gpsInfo": {
            "longitude": 114028123,
            "latitude": 22536189,
            "regionName": "深圳市福田区车公庙泰然大厦C座"
          }
        }

        r15 = requests.post(url6,json.dumps(data), headers=headers)
        print(r15.text)
        result15 = r15.json()['resultCode']
        self.assertEqual(0, result15)


    # WIFI考勤打卡成功case
    def test_wifi_success(self):
        data = {
          "userId": bizMateId,
          "companyId": orgId,
          "gpsInfo": {
              "macAddr": "b0:f9:63:87:f9:f0",
              "wifiName": "sinosun-mobile"
          }
        }

        r16 = requests.post(url6,json.dumps(data), headers=headers)
        print(r16.text)
        result16 = r16.json()['resultCode']
        self.assertEqual(0, result16)

# 如果直接运行这个文件，需要执行unittest中的main函数执行测试用例
if __name__ == '__main__':
    unittest.main()