import winreg
import os
import re

def getInstalledAppsList():
    result = []
    sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall']
    for i in sub_key:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i)
        for j in range(winreg.QueryInfoKey(key)[0]):
            try:
                each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'{i}\\{winreg.EnumKey(key, j)}')
                DisplayName = winreg.QueryValueEx(each_key, 'DisplayName')[0]
                Version = winreg.QueryValueEx(each_key, 'DisplayVersion')[0]
                UninstallString = winreg.QueryValueEx(each_key, 'UninstallString')[0]
                info = {'name': DisplayName, 'version': Version, 'uninstallpath': UninstallString}
                result.append(info)
            except WindowsError:
                pass
        key.Close()
    sub_key = [r'Software\Microsoft\Windows\CurrentVersion\Uninstall']
    for i in sub_key:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, i)
        for j in range(winreg.QueryInfoKey(key)[0]):
            try:
                each_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f'{i}\\{winreg.EnumKey(key, j)}')
                DisplayName = winreg.QueryValueEx(each_key, 'DisplayName')[0]
                Version = winreg.QueryValueEx(each_key, 'DisplayVersion')[0]
                info = {'name': DisplayName, 'version': Version}
                result.append(info)
            except WindowsError:
                pass
        key.Close()
    return result

def getAppPath():
    result = []
    sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths']
    for i in sub_key:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i)
        for j in range(winreg.QueryInfoKey(key)[0]):
            try:
                each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'{i}\\{winreg.EnumKey(key, j)}')
                Path = winreg.QueryValueEx(each_key, 'Path')[0]
                result.append(Path)
            except WindowsError:
                pass
        key.Close()
    sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths']
    for i in sub_key:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, i)
        for j in range(winreg.QueryInfoKey(key)[0]):
            try:
                each_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f'{i}\\{winreg.EnumKey(key, j)}')
                Path = winreg.QueryValueEx(each_key, 'Path')[0]
                result.append(Path)
            except WindowsError:
                pass
        key.Close()
    return result

def pathProcess(str):
    processResult = str
    if(str[0] == "\""):
        reg = re.compile(r'"(.*?)"')
        result = re.findall(reg, str)
        if(result[0].endswith(".exe")):
            result[0] = os.path.dirname(result[0])
        processResult = result[0]
    if(processResult.endswith(".exe")):
        processResult = os.path.dirname(processResult)
    '''
    if (processResult.find("\\")):
        print(processResult)
        processResult = os.path.dirname(processResult[0:processResult.index(".exe") + 4])
    '''
    return processResult

def checkChromium(dir):
    try :
        for i in os.listdir(dir):
            if i == 'LICENSES.chromium.html':
                chromiumExist = True
                break
            else:
                chromiumExist = False
        if(chromiumExist == False):
            for i in os.listdir(dir):
                if i.startswith('chrom'):
                    chromiumExist = True
                    break
                else:
                    chromiumExist = False
    except:
        chromiumExist = False
        pass
    return chromiumExist

detectedDir = []
for i in getInstalledAppsList():
    try:
        dispName = i['name']
        pathString = i['uninstallpath']
    except KeyError:
        pass
    if(pathString.startswith('MsiExec.exe')):
        pass
    elif(pathString.startswith('%')):
        pass
    elif(pathString.startswith('\"C:\\WINDOWS\\SysWOW64\\RunDll32.EXE\"')):
        pass
    else:
        pathString = pathProcess(pathString)
        if(checkChromium(pathString)):
            detectedDir.append([dispName,pathString])
print('\033[33m喜报\n在您的计算机被这些软件强行安装了Chromium：\033[0m')
for i in detectedDir:
    print('\033[31m产品名称：\033[0m' + i[0] + '\n\033[31m位置：\033[0m' + i[1])
print('\033[92m总计：'+str(len(detectedDir))+'个\033[0m')
