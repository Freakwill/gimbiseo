# gimbiseo
🤖Man-machine conversation system base on owlready2. It is inspirited by a Korean TV Play (*what's up with Gim seceretary*). When I initiated the development of the system, I was watching the TV recommended by many people. And I wanted to make a "digit secretary" to reduce the brain labor. Hence I just called it gimbiseo (Gim Secretary).

Thank the author of OwlReady who helped me realizing the dream of human-machine dialogue system.

基于 owlready2 的问答系统。灵感来自韩剧《金秘书你为何这样》。因为在开始开发这个系统的时候，我正在看这个部很多人安利的韩剧。而我最初是想做一个“数字秘书”，可以减轻我的脑力劳动。于是干脆就把这个项目叫 gimbiseo“金秘书”。

旧版的[“数字秘书”](https://github.com/Freakwill/assistant)完全没有逻辑推理能力，只能记录每次的问答对，以及简单的查询-输出。特别感谢[OwlReady](https://owlready2.readthedocs.io/en/latest/)的作者使我人机对话的梦想成真。

![](https://github.com/Freakwill/gimbiseo/blob/master/gimbiseo.jpg)

## Requirements
- OwlReady2
- pyparsing
- jieba

# Usage
just run `owlgimbiseo.py`
or run `ui.py` with UI

## Attention (only for Chinese)
不启用分词（目前不再推荐）
- 个体名词必须加上引号
- 动词前面加上v:, 量词加q:, 形容词在作定语的时候加a:(其余情况不加)
- 词语之间用空格隔开

启用分词（默认）
- 个体名词必须加上引号（英文）
- `[v动词], [a形容词]`
- `[不]`(目前必须始终强制追加[])

一般只需使用一次（在第一次出现时使用），如果保证能够识别词性，可以不加。

句法:
```
   句子 -> 名词+动词+复合名词    # 地球围绕太阳，地球是蓝色的行星，月球围绕蓝色的围绕太阳的天体
   复合名词 -> 形容词 + 形容词 + ... + 名词  # 蓝色的行星，围绕太阳的行星，红色的围绕太阳的天体
   形容词 -> ..的 | 动宾短语+的  # 蓝色的，围绕太阳的
   名词 -> 个体 | 类   # 太阳，行星
``` 

错误句法:
我爱我的祖国。# “我的”不能作为形容词 


*注意* 疑问句的问号是中文的。

详见[帮助文档](https://github.com/Freakwill/gimbiseo/blob/master/helpdoc.md)

# Usage/Test/Demo
```python
# basic usage
from owlgimbiseo import *
d = Dialogue()
memory = ChineseMemory()
d(memory)

# test/demo
from qadict import *
q_as = testy
d.demo(testy, memory) # d.test(testy, memory)
```
 
## Demo

    -- "八公" 是 狗
    -- 狗是什么?
    -- "八公" 是 a:忠诚的 狗
    -- 忠诚的是什么?
    -- 忠诚的 是一种 性质
    -- 我知道了
    -- 狗 是一种 动物
    -- 动物是什么?
    -- 动物 是一种 事物
    -- 我知道了
    -- "八公" 是 狗 吗？
    -- 让我想一想...是
    -- 狗 是一种 什么 ？
    -- 让我想一想...动物
    -- 狗 v:爱吃 骨头
    -- 骨头是什么?
    -- 狗狗 我好爱吃
    -- 能再说一遍吗？
    -- 骨头 是一种 事物
    -- 我知道了
    -- 狗 v:爱吃 骨头 吗？
    -- 让我想一想...是
    -- "八公" v:爱吃 骨头 吗？
    -- 让我想一想...是
    -- "八公" 是 v:爱吃 骨头 的 a:忠诚的 狗 吗？
    -- 让我想一想...是
    -- 骨头 v:爱吃 骨头 吗？
    -- 让我想一想...不是
    -- 狗 v:爱吃 什么 ？
    -- 让我想一想...骨头
    -- "八公" 是 什么样的 狗？
    -- 让我想一想...忠诚的
    -- "八公" v:喜欢 "教授"
    -- 教授是什么?
    -- "教授" 是 人
    -- 人是什么?
    -- 人 是一种 事物
    -- 我知道了
    -- "八公" v:喜欢 谁？
    -- 让我想一想...教授

## Word cutting
Applying the technology of word cutting

    Users:  "八公"是狗
    AI:  狗是什么?
    Users:  狗是一种动物
    AI:  动物是什么?
    Users:  动物是一种事物
    AI: 我知道了
    Users:  八公是狗吗？
    AI: 让我想一想...是
    Users:  狗是一种什么？
    AI: 让我想一想...动物
    Users:  狗喜欢骨头
    AI:  骨头是什么?
    Users:  狗狗我好喜欢
    AI: 能再说一遍吗？
    Users:  骨头是一种事物
    AI: 我知道了
    Users:  狗喜欢骨头吗？
    AI: 让我想一想...是
    Users:  八公喜欢骨头吗？
    AI: 让我想一想...是
    Users:  骨头喜欢骨头吗？
    AI: 让我想一想...不是
    Users:  狗喜欢什么？
    AI: 让我想一想...骨头

# Video
[交互模式演示视频](https://www.bilibili.com/video/av66578713)

[交互模式演示视频(分词)](https://www.bilibili.com/video/av69086776)
[交互模式演示视频(分词改进)](https://www.bilibili.com/video/av70597500)
[GUI演示视频](https://www.bilibili.com/video/av70597500?p=2)
# Examples
(English is not supported currently)
```
-- Who dose Alice love?
I am thinking...
-- What is Alice?
-- Alice is a Thing.
-- I get.
-- Bob is a Thing.
-- I get.
-- Alice love Bob.
-- I get.
-- Who dose Alice love?
I am thinking...
-- Bob
-- love is a sort of SymmetricProperty.
-- I get.
-- Who dose Bob love?
-- Alice.
--
```

```
-- lily is a Thing.
-- I get.
-- Flower is a sort of Thing.
-- I get.
-- lily is a Flower.
-- I get.
-- Person is a sort of Thing.
-- I get.
-- lily is a Person.
-- I get.
-- Is lily a Person?
I am thinking...
-- Yes
```

# TODO
- [x] 实现复合概念
- [x] 实现分词
- [x] GUI设计
- [ ] 与机器学习方法结合
