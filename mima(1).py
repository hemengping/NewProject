import os
import time
import cv2

import numpy as np

## im：原图
## dir_name:模板目录
def get_number_keyboard_location(im, dir_name):

    templates = {}
    nimpath = dir_name

    for i in range(0,11):
        templates[i] = os.path.join(nimpath,"{}.png".format(i))
        print(templates[i])

    #读图片
    img_rgb = cv2.imread(im)
    #彩色图片转灰度图片
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #把图片二值化
    ret,thresh1=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    #寻找轮廓
    threshCnts, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = threshCnts
    locs = []
    # 遍历轮廓
    for (i, c) in enumerate(cnts):
        # 计算矩形
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # 选择合适的区域，根据实际任务来，这里的基本都是四个数字一组
        if ar > 0.2 and ar < 1 and w>10 and h>10:
            locs.append((x, y, w, h))

    # 将符合的轮廓从左到右排序
    locs = sorted(locs, key=lambda x: x[0])

    locs_x =[]
    locs_y =[]
    locs_result = []
    for rect in locs:
        for teNum,tepath in templates.items():
            ##读取模板图像
            template = cv2.imread(tepath)
            if template is not None:
                h, w = template.shape[:-1]
                #将模板图像与Roi图像的大小调整到一样
                pic = cv2.resize(img_rgb[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]], (w + 1, h + 1),
                                 interpolation=cv2.INTER_LINEAR)
                #模板匹配算法
                res = cv2.matchTemplate(pic, template, cv2.TM_CCOEFF_NORMED)
            #用阈值过滤结果
            threshold =.60
            loc = np.where(res >= threshold)
            if np.size(loc) > 0:
                #cv2.circle(img_rgb, (int(rect[0]+rect[2]/2), int(rect[1]+rect[3]/2)), 5, (0, 0, 255), 1)
            #画矩形框
                locs_result.append((int(rect[0]+rect[2]/2),int(rect[1]+rect[3]/2)))
                locs_x.append(int(rect[0]+rect[2]/2))
                locs_y.append(int(rect[1]+rect[3]/2))
                cv2.rectangle(img_rgb, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 2)
                break
    #显示结果
    cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
    img_rgb = cv2.resize(img_rgb,(512,1024))
#    cv2.imshow('input_image', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return locs_result

if __name__ == "__main__":
    #返回参数1：键盘坐标
    #返回参数2：每个键的坐标
    locs_result = get_number_keyboard_location('img/shuzi.jpg','img')
    print(locs_result)