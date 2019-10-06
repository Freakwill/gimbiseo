#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict

test1 = OrderedDict({
    '"八公" 是 狗':'',  
    '狗 是一种 动物':'',
    '动物 是一种 事物':'我知道了',
    '"八公" 是 狗 吗？':'是',
    '狗 是一种 什么？':'动物',
    '狗 v:喜欢 骨头':'',
    '狗狗 我好喜欢':'能再说一遍吗？',
    '骨头 是一种 事物':'我知道了',
    '狗 v:喜欢 骨头':'不要重复',
    '狗 v:喜欢 骨头 吗？':'是',
    '"八公" v:喜欢 骨头 吗？':'是',
    '骨头 v:喜欢 骨头 吗？':'不是',
    '狗 v:喜欢 什么 ？':'骨头',
    })

test11 = OrderedDict({
    '"八公" 是 狗；狗 是一种 动物':'',
    '动物 是一种 事物':'我知道了',
    '"八公" 是 狗 吗？':'是',
    '狗 是一种 什么？':'动物',
    '狗 v:喜欢 骨头':'',
    '狗狗 我好喜欢':'能再说一遍吗？',
    '骨头 是一种 事物':'我知道了',
    '狗 v:喜欢 骨头':'不要重复',
    '狗 v:喜欢 骨头 吗？':'是',
    '"八公" v:喜欢 骨头 吗？':'是',
    '骨头 v:喜欢 骨头 吗？':'不是',
    '狗 v:喜欢 什么 ？':'骨头',
    })

test2 = OrderedDict({
    '"八公" 是 狗':'',
    '"八公" 是 a:忠诚的 狗':'',
    '忠诚的 是一种 性质':'',
    '狗 是一种 动物':'',
    '动物 是一种 事物':'我知道了',
    '"八公" 是 狗 吗？':'是',
    '狗 是一种 什么 ？':'动物',
    '狗 v:爱吃 骨头':'',
    '狗狗 我好爱吃':'能再说一遍吗？',
    '骨头 是一种 事物':'我知道了',
    '狗 v:爱吃 骨头':'不要重复',
    '狗 v:爱吃 骨头 吗？':'是',
    '"八公" v:爱吃 骨头 吗？':'是',
    '"八公" 是 v:爱吃 骨头 的 a:忠诚的 狗 吗？':'是',
    '骨头 v:爱吃 骨头 吗？':'不是',
    '狗 v:爱吃 什么 ？':'骨头',
    '"八公" 是 什么样的 狗？':'',
    '"八公" v:喜欢 "教授"':'我知道了',
    '"教授" 是 人':'',
    '人 是一种 事物':'',
    '"八公" v:喜欢 谁？':'教授'
    })

test3 = OrderedDict({
    '"地球" 是 行星':'',
    '行星 是一种 天体':'',
    '天体 是一种 事物':'我知道了',
    '"地球" v:围绕 "太阳"':'',
    '"地球" 是 a:蓝色的':'我知道了',
    '蓝色的 是一种 性质':'',
    '"金星" 是 行星':'',
    '"金星" 是 a:红色的':'',
    '红色的 是一种 性质':'',
    '"地球" 是 蓝色的':'我知道了',
    '"太阳" 是 恒星':'我知道了',
    '行星 只 v:围绕 恒星':'',
    '恒星 是一种 天体':'我知道了',
    '"太阳" 是 恒星 吗？':'是',
    '卫星 v:围绕 行星':'',
    '卫星 是一种 天体':'我知道了',
    '"月球" 是 卫星': '我知道了',
    '"月球" 只 v:围绕 "地球"':'我知道了',
    '"月球" v:围绕 "地球" 吗？':'是',
    '"月球" v:围绕 "金星" 吗？':'不是',
    '"月球" 是 v:围绕 "地球" 的 卫星 吗？':'是',
    '哪个 卫星 是 v:围绕 "地球" 的 卫星？':'月球',
    '"地球" 是 a:蓝色的 行星 吗？':'',
    '哪个 天体 是 a:蓝色的 行星？':'地球',
    '哪个 天体 是 a:红色的 行星？':'金星',
    '"地球" 是 什么 天体？':'',
    '"月球" v:围绕 哪个 天体？':'地球',
    })


test4 = OrderedDict({
    '"地球" 是 行星':'',
    '行星 是一种 天体':'',
    '恒星 也是一种 天体':'',
    '天体 是一种 事物':'我知道了',
    '"地球" v:围绕 "太阳"':'',
    '"太阳" 是 恒星': '',
    '"地球" 是 a:蓝色的 天体':'我知道了',
    '蓝色的 是一种 性质':'',
    '"地球" 是 a:蓝色的 行星 吗？':'是',
    '哪个 天体 是 a:蓝色的 行星？':'地球',
    '哪个 天体 v:围绕 "太阳"？':'地球',
    '"毗邻星" 是 恒星':'',
    '"地球" v:围绕 "毗邻星" 吗？':''
    })

test5 = OrderedDict({
    '玫瑰 是一种 植物':'',
    '植物 是一种 生物':'',
    '生物 是一种 事物':'',
    '玫瑰 是一种 植物 吗？':'',
    '玫瑰 v:象征 爱情':'',
    '爱情 是一种 事物':'',
    '玫瑰 v:象征 什么？':'',
    '什么 生物 是一种 v:象征 爱情 的 植物？':'',
})

test6 = OrderedDict({
    '生物 是一种 a:有生命的 事物':'',
    '有生命的 是一种 性质':'',
    '动物 是一种 a:能动的 生物':'',
    '能动的 是一种 性质':'',
    '植物 是一种 a:不能动的 生物':'',
    '不能动的 是一种 性质':'',
    '不能动的 不 是一种 a:能动的 事物':'',
    '地点 是一种 事物':'',
    '"水中" 是 地点':'',
    '水生的 定义为 v:栖息在 "水中" 的 性质':'',
    '水草 是一种 a:水生的 植物':'',
    '水草 不 是一种 a:能动的 生物 吗？':'',
    '水草 是一种 a:不能动的 生物 吗？':'',
    '草鱼 是一种 鱼':'',
    '鱼 是一种 a:水生的 生物':'',
    '草鱼 q:只 v:吃 水草':'',
    '水草 是一种 植物':'',
    '草食的 定义为 q:只 v:吃 植物 的 生物':'',
    '草鱼 是一种 a:草食的 生物 吗？':'是',
    '鲨鱼 是一种 a:肉食的 鱼':'',
    '肉食的 定义为 q:只 v:吃 动物 的 生物':'',
    '鲨鱼 v:吃 鱼':'',
    '鲨鱼 v:吃 水草 吗？':'不是',
    '什么 生物 v:栖息在 "水中"？':'',
    '鸟 是一种 a:会飞的 动物':'',
    '会飞的 是一种 a:能动的 性质':'',
    '鸟 是一种 a:会飞的 生物 吗？':'是',
    '企鹅 是一种 鸟':'',
    '企鹅 是一种 a:会飞的 生物 吗？':'是',
    '企鹅 v:栖息在 "南极"':'',
    '"南极" 是 地点':'',
    '企鹅 是一种 什么 动物？':'',
    '"QQ" 是 企鹅':'',
    '"QQ" 是 什么？':'',
    '"QQ" v:栖息在 哪个 地点？':'',
    '"QQ" 是 会飞的 吗？':'',
    '海狗 q:只 v:吃 企鹅':'',
    '海狗 是一种 动物':'',
    '海狗 是一种 a:肉食的 动物 吗？':'',
})


testx = OrderedDict({
    '"八公"是狗':'',  
    '狗是一种动物':'',
    '动物是一种事物':'我知道了',
    '八公是狗吗？':'是',
    '狗是一种什么？':'动物',
    '狗喜欢骨头':'',
    '狗狗我好喜欢':'能再说一遍吗？',
    '骨头是一种事物':'我知道了',
    '狗喜欢骨头':'不要重复',
    '狗喜欢骨头吗？':'是',
    '八公喜欢骨头吗？':'是',
    '骨头喜欢骨头吗？':'不是',
    '狗喜欢什么？':'骨头',
    })

testy = OrderedDict({
    '生物是一种[a有生命的]事物':'',
    '有生命的是一种性质':'',
    '动物是一种[a能动的]生物':'',
    '能动的是一种性质':'',
    '植物是一种[a不能动的]生物':'',
    '不能动的是一种性质':'',
    '不能动的[不]是一种能动的事物':'',
    '地点是一种事物':'',
    '"水中"是地点':'',
    '[a水生的]定义为[v栖息在]"水中"的性质':'',
    '水草是一种水生的植物':'',
    '水草[不]是一种能动的生物吗？':'',
    '水草是一种不能动的生物吗？':'是',
    '草鱼是一种鱼':'',
    '鱼是一种水生的生物':'',
    '草鱼只吃水草':'',
    '水草是一种植物':'',
    '[a草食的]定义为只吃植物的生物':'',
    '草鱼是一种草食的生物吗？':'是',
    '鲨鱼是一种[a肉食的]鱼':'',
    '肉食的定义为只吃动物的生物':'',
    '鲨鱼吃鱼':'',
    '鲨鱼吃水草吗？':'不是',
    '什么生物栖息在水中？':'',
    '鸟是一种[a会飞的]动物':'',
    '会飞的是一种能动的性质':'',
    '鸟是一种会飞的生物吗？':'是',
    '企鹅是一种鸟':'',
    '企鹅是一种会飞的生物吗？':'是',
    '企鹅栖息在"南极"':'',
    '南极是地点':'',
    '企鹅是一种什么动物？':'',
    '"QQ"是企鹅':'',
    'QQ是什么？':'',
    'QQ栖息在哪个地点？':'',
    'QQ是会飞的吗？':'',
    '海狗只吃企鹅':'',
    '海狗是一种动物':'',
    '海狗是一种肉食的动物吗？':'',
})



