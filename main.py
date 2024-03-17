#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Author  : Hatanezumi
@Contact : Hatanezumi@chunshengserver.cn
'''
import os
import ctypes
import psutil
import win32api
import win32process

class MemoryProcess():
    def __init__(self, name:str) -> None:
        PROCESS_ALL_ACCESS = (0x000F0000|0x00100000|0xFFF)#最高权限
        pids = psutil.pids()
        while True:
            try:
                pid = [pid for pid in pids if psutil.Process(pid).name() == name]
            except psutil.NoSuchProcess as err:
                continue
            except:
                raise
            else:
                break
        self.pid = pid[0] if len(pid) > 0 else -1
        if pid == -1:
            raise FileNotFoundError('未找到游戏进程')
        self.process = win32api.OpenProcess(PROCESS_ALL_ACCESS,False,self.pid)
        self.md = ctypes.windll.LoadLibrary(os.path.join('C:','Windows','System32','kernel32.dll'))
    def close(self):
        '''
        关闭进程
        '''
        win32api.CloseHandle(self.process)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
    def __get_data(self, type:str, value:int|float=None) -> ctypes.c_long | ctypes.c_short | ctypes.c_longlong | ctypes.c_float | ctypes.c_double:
        '''
        type:类型
        返回对应类型的ctype类
        '''
        if type == 'long':
            data = ctypes.c_long() if value is None else ctypes.c_long(value)
        elif type == 'short':
            data = ctypes.c_short() if value is None else ctypes.c_short(value)
        elif type == 'longlong':
            data = ctypes.c_longlong() if value is None else ctypes.c_longlong(value)
        elif type == 'float':
            data = ctypes.c_float() if value is None else ctypes.c_float(value)
        elif type == 'double':
            data = ctypes.c_double() if value is None else ctypes.c_double(value)
        else:
            raise ValueError(f'type:{type}')
        return data
    def get_memory(self, addr:str, type:str='long') -> int:
        '''
        addr:地址
        读取内存地址
        '''
        data = self.__get_data(type)
        self.md.ReadProcessMemory(int(self.process),int(addr,16),ctypes.byref(data),ctypes.sizeof(data),None)
        return data.value
    def write_memory(self, addr:str,vaule:int, type:str='long') -> int:
        '''
        addr:地址
        data:要写入的值
        写入内存数据
        返回0则代表失败
        '''
        data = self.__get_data(type,vaule)
        res = self.md.WriteProcessMemory(int(self.process),int(addr,16),ctypes.byref(data),ctypes.sizeof(data),None)
        return res
    def get_module_handle(self) -> str:
        '''
        返回程序基址
        '''
        module_handles = win32process.EnumProcessModules(self.process)
        module_handle = module_handles[0] # 0就是基址
        return hex(module_handle)
    def get_point(self, addr:str,vx:str) -> str:
        '''
        addr:地址
        vx:偏移
        返回计算后的偏移地址
        '''
        return hex(self.get_memory(addr) + int(vx,16))

with MemoryProcess('Raising succubus.exe') as game:
    EXPADDR = game.get_point(game.get_point(game.get_point(game.get_point(hex(int(game.get_module_handle(),16) + int('0x00509D7C',16)),'0x2C'),'0x10'),'0x468'),'0x20')
    MONEYADDR = game.get_point(game.get_point(game.get_point(game.get_point(hex(int(game.get_module_handle(),16) + int('0x00509D7C',16)),'0x2C'),'0x10'),'0x1B0'),'0x1C0')
    SEXADDR = game.get_point(game.get_point(game.get_point(hex(int(game.get_module_handle(),16) + int('0x00727EF0',16)),'0x30'),'0x1B0'),'0x200')
    RENADDR = game.get_point(game.get_point(game.get_point(game.get_point(game.get_point(hex(int(game.get_module_handle(),16) + int('0x004EF02C',16)),'0x8'),'0'),'0x18'),'0xA4'),'0x5B0')
    HUIADDR = game.get_point(game.get_point(game.get_point(game.get_point(hex(int(game.get_module_handle(),16) + int('0x00509D7C',16)),'0x2C'),'0x10'),'0x21C'),'0x50')
    os.system('title サキュバスの育成方法 5项修改器 v1.0.0')
    while True:
        os.system('cls')
        print('=' * 50 + '\nサキュバスの育成方法 5项修改器 v1.0.0\n作者:田鼠Hatanezumi\n' + '=' * 50)
        print('-' * 50 + '\n当前数值:')
        print('EXP:',int(game.get_memory(EXPADDR, 'double')))
        print('钱:',int(game.get_memory(MONEYADDR, 'double')))
        print('性技:',int(game.get_memory(SEXADDR, 'double')))
        print('忍耐力:',int(game.get_memory(RENADDR, 'double')))
        print('恢复力:',int(game.get_memory(HUIADDR, 'double')))
        print('-' * 50)
        choose = input('请选择要修改的项目:\n1.EXP\n2.钱\n3.性技\n4.忍耐力\n5.恢复力\n0.退出\n')
        if choose == '1':
            value = int(input('请输入要修改的数值:'))
            if value < 0:
                print('输入必须大于0!')
                os.system('pause')
                continue
            print('修改失败' if game.write_memory(EXPADDR, value, 'double') == 0 else '修改成功')
        elif choose == '2':
            value = int(input('请输入要修改的数值:'))
            if value < 0:
                print('输入必须大于0!')
                os.system('pause')
                continue
            print('修改失败' if game.write_memory(MONEYADDR, value, 'double') == 0 else '修改成功')
        elif choose == '3':
            value = int(input('请输入要修改的数值:'))
            if value < 0:
                print('输入必须大于0!')
                os.system('pause')
                continue
            print('修改失败' if game.write_memory(SEXADDR, value, 'double') == 0 else '修改成功')     
        elif choose == '4':
            value = int(input('请输入要修改的数值:'))
            if value < 0:
                print('输入必须大于0!')
                os.system('pause')
                continue
            print('修改失败' if game.write_memory(RENADDR, value, 'double') == 0 else '修改成功') 
        elif choose == '5':
            value = int(input('请输入要修改的数值:'))
            if value < 0:
                print('输入必须大于0!')
                os.system('pause')
                continue
            print('修改失败' if game.write_memory(HUIADDR, value, 'double') == 0 else '修改成功') 
        elif choose == '0':
            break
        else:
            continue
        os.system('pause')