from scipy.io import loadmat
import pandas as pd

def CRWU_readdata(fau_pos,fau_type,size,load,clock='0',file_pos='D:\\OneDrive\\毕业设计\\CRWU\\'):
    #读取CRWU实验数据
    #fau_pos:故障位置，可选参数'FE','DE12K','DE48K'
    #fau_type:故障类型，可选参数'B','IR','OR'
    #size:故障大小，可选参数'07','14','21','28'
    #load:负载，可选参数'0','1','2','3'
    #clock:当fau_type为'OR'时，可选参数'6','12','3'
    #file_pos:文件路径，默认为'D:\\OneDrive\\毕业设计\\CRWU\\'
    #返回值：RPM:转速，DE:驱动端数据，FE:风扇端数据，BA:基座数据

    file=''
    if fau_pos not in ('FE','DE12K','DE48K'):#判断故障位置参数是否正确
        raise ValueError('fau_pos参数错误')
    else:
        if fau_pos=='FE':
            file+='12k Fan End Bearing Fault Data'
        elif fau_pos=='DE12K':
            file+='12k Drive End Bearing Fault Data'
        elif fau_pos=='DE48K':
            file+='48k Drive End Bearing Fault Data'

    if fau_type not in ('B','IR','OR'):#判断故障类型参数是否正确
        raise ValueError('fau_type参数错误')
    else:
        if fau_type=='B':
            file+='\\Ball'
        elif fau_type=='IR':
            file+='\\Inner Race'
        elif fau_type=='OR':
            if clock not in ('6','12','3'):
                raise ValueError('clock参数错误')
            else:
                file+='\\Outer Race'

    if size not in ('07','14','21','28'):#判断故障大小参数是否正确
        raise ValueError('size参数错误')
    else:
        file+='\\00'+size

    if load not in ('0','1','2','3'):#判断负载参数是否正确
        raise ValueError('load参数错误')
    
    file_name=fau_type+'0'+size
    if fau_type=='OR':
        file_name+=('@'+clock)
    file_name+='_'+load+'.mat'#生成mat文件名
    
    file=file_pos+file+('\\'+file_name)#生成文件路径
    try:
        data=loadmat(file)#由于某些参数下没有实验数据，故使用try读取文件
    except FileNotFoundError:
        raise FileNotFoundError('不存在该参数下实验数据文件')
    
    keys=data.keys()
    RPM=[s for s in keys if 'RPM' in s][0]
    DE=[s for s in keys if 'DE' in s][0]
    FE=[s for s in keys if 'FE' in s][0]
    BA=[s for s in keys if 'BA' in s]

    RPM=data[RPM][0][0]#读取转速
    DE=data[DE].flatten()#读取驱动端数据
    FE=data[FE].flatten()#读取风扇端数据
    if len(BA)!=0:
        BA=data[BA[0]].flatten()#读取基座数据
    print(f'该实验转速参数:{RPM}rpm\n驱动端DE数据长度:{len(DE)}\n风扇端FE数据长度:{len(FE)}\n基座BA数据长度:{len(BA)}')
    return RPM,DE,FE,BA