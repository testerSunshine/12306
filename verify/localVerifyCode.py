# coding: utf-8
import TickerConfig

if TickerConfig.AUTO_CODE_TYPE == 2:
    import base64
    import os
    import cv2
    import numpy as np
    from keras import models, backend
    import tensorflow as tf
    from verify import pretreatment
    from verify.mlearn_for_image import preprocess_input

    graph = tf.get_default_graph()

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


TEXT_MODEL = ""
IMG_MODEL = ""


def get_text(img, offset=0):
    text = pretreatment.get_text(img, offset)
    text = cv2.cvtColor(text, cv2.COLOR_BGR2GRAY)
    text = text / 255.0
    h, w = text.shape
    text.shape = (1, h, w, 1)
    return text


def base64_to_image(base64_code):
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.fromstring(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)

    return img


class Verify:
    def __init__(self):
        self.textModel = ""
        self.imgModel = ""
        self.loadImgModel()
        self.loadTextModel()

    def loadTextModel(self):
        if not self.textModel:
            self.textModel = models.load_model(PATH('../model.v2.0.h5'))
        else:
            print("无需加载模型model.v2.0.h5")

    def loadImgModel(self):
        if not self.imgModel:
            self.imgModel = models.load_model(PATH('../12306.image.model.h5'))

    def verify(self, fn):
        verify_titles = ['打字机', '调色板', '跑步机', '毛线', '老虎', '安全帽', '沙包', '盘子', '本子', '药片', '双面胶', '龙舟', '红酒', '拖把', '卷尺',
                         '海苔', '红豆', '黑板', '热水袋', '烛台', '钟表', '路灯', '沙拉', '海报', '公交卡', '樱桃', '创可贴', '牌坊', '苍蝇拍', '高压锅',
                         '电线', '网球拍', '海鸥', '风铃', '订书机', '冰箱', '话梅', '排风机', '锅铲', '绿豆', '航母', '电子秤', '红枣', '金字塔', '鞭炮',
                         '菠萝', '开瓶器', '电饭煲', '仪表盘', '棉棒', '篮球', '狮子', '蚂蚁', '蜡烛', '茶盅', '印章', '茶几', '啤酒', '档案袋', '挂钟', '刺绣',
                         '铃铛', '护腕', '手掌印', '锦旗', '文具盒', '辣椒酱', '耳塞', '中国结', '蜥蜴', '剪纸', '漏斗', '锣', '蒸笼', '珊瑚', '雨靴', '薯条',
                         '蜜蜂', '日历', '口哨']
        # 读取并预处理验证码
        img = base64_to_image(fn)
        text = get_text(img)
        imgs = np.array(list(pretreatment._get_imgs(img)))
        imgs = preprocess_input(imgs)
        text_list = []
        # 识别文字
        self.loadTextModel()
        global graph
        with graph.as_default():
            label = self.textModel.predict(text)
        label = label.argmax()
        text = verify_titles[label]
        text_list.append(text)
        # 获取下一个词
        # 根据第一个词的长度来定位第二个词的位置
        if len(text) == 1:
            offset = 27
        elif len(text) == 2:
            offset = 47
        else:
            offset = 60
        text = get_text(img, offset=offset)
        if text.mean() < 0.95:
            with graph.as_default():
                label = self.textModel.predict(text)
            label = label.argmax()
            text = verify_titles[label]
            text_list.append(text)
        print("题目为{}".format(text_list))
        # 加载图片分类器
        self.loadImgModel()
        with graph.as_default():
            labels = self.imgModel.predict(imgs)
        labels = labels.argmax(axis=1)
        results = []
        for pos, label in enumerate(labels):
            l = verify_titles[label]
            print(pos + 1, l)
            if l in text_list:
                results.append(str(pos + 1))
        return results


if __name__ == '__main__':
    pass
    # verify("verify-img1.jpeg")
