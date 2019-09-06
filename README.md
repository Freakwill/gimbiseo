# gimbiseo
🤖Man-machine conversation system base on owlready2. It is inspirited by a Korean TV Play.

基于 owlready2 的问答系统。灵感来自韩剧《金秘书你为何这样》
![](https://github.com/Freakwill/gimbiseo/blob/master/gimbiseo.jpg)

## Requirements
- OwlReady2
- pyparsing
- jieba (Optional)

# Usage
just run `owlgimbiseo.py`

## Attention (only for Chinese)
系统处于测试阶段，没有启用分词。若启用分词，则不必注意这些
- 个体名词必须加上引号
- 动词前面加上v:, 量词加q:, 形容词在作定语的时候加a:(其余情况不加)
- 词语之间用空格隔开

# Test
run `test.py`
 
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

# Video
[交互模式演示视频(旧版)](https://www.bilibili.com/video/av56821908)
[交互模式演示视频](https://www.bilibili.com/video/av66578713)

# Examples
(English is deprecated currently)
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
- [ ] 实现复合概念
- [ ] GUI设计
- [ ] 与机器学习方法结合
