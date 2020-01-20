import torch
import torch.nn as nn
import torch.nn.functional as F

class BaseTransformer(nn.Module):
    def __init__(self):
        '''
        脉冲-电流转换器的基类

        输入是脉冲（torch.bool），输出是电流（torch.float）
        '''
        super().__init__()

    def forward(self, in_spike):
        '''
        :param in_spike: 输入脉冲
        :return: 输出电流

        要求子类必须实现这个函数
        '''
        raise NotImplementedError

    def reset(self):
        '''
        :return: None

        重置所有的状态变量为初始值
        对于有状态的子类，必须实现这个函数
        '''
        pass

class SpikeCurrent(BaseTransformer):
    def __init__(self, amplitude=1):
        '''
        :param amplitude: 放大系数

        输入脉冲，输出与脉冲形状完全相同、离散的、大小为amplitude倍的电流
        '''
        super().__init__()
        self.amplitude = amplitude

    def forward(self, in_spike):
        '''
        :param in_spike: 输入脉冲
        :return: 输出电流

        简单地将输入脉冲转换为0/1的浮点数，然后乘以amplitude
        '''
        return in_spike.float() * self.amplitude

class ExpDecayCurrent(BaseTransformer):
    def __init__(self, tau, amplitude=1):
        '''
        :param tau: 衰减的时间常数，越小则衰减越快
        :param amplitude: 放大系数

        指数衰减的脉冲-电流转换器

        若当前时刻到达一个脉冲，则电流变为amplitude

        否则电流按时间常数为tau进行指数衰减
        '''
        super().__init__()
        self.tau = tau
        self.amplitude = amplitude
        self.i = 0

    def forward(self, in_spike):
        '''
        :param in_spike: 输入脉冲
        :return: 输出电流
        '''
        in_spike_float = in_spike.float()
        i_decay = -self.i / self.tau
        self.i += i_decay * (1 - in_spike_float) + self.amplitude * in_spike_float
        return self.i

    def reset(self):
        '''
        :return: None
        重置所有状态变量为初始值，对于ExpDecayCurrent而言，直接将电流设置为0即可
        '''
        self.i = 0




