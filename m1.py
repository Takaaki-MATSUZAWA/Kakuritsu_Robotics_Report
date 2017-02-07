
# coding: utf-8

# # 関数定義
# 
# 今回の課題で価値反復の計算を行うために以下の4つの関数を実装した。
# 課題を順にときながら実装し、最終的にすべての課題を溶けるよう関数を製作した。
# マップを2次元配列で表現するが、大きさが変わっても対応できるが例外処理などは実装していない。
# 
# ***
# `argMax(V, R, x, y,cost=1, miss=None)`<br>
# 
# 指定したマップの座標から最適方策を計算する関数
# 
# V    :価値を定義した配列<br>
# R    :ペナルティを定義した配列<br>
# x,y  :計算したいノードの座標<br>
# cost :移動にかかるコストの定義　初期値：1<br>
# miss :移動の際に間違って他のノードに入る確率　初期値：無効<br>
# 
# 戻り値：ノードの価値(int or float),方策を示す矢印(str)
# ***
# `showValueMap(V, header = None)`<br>
# 
# 与えられた配列をいい具合に表示する関数
# 
# V    :任意の2次元配列<br>
# header:ヘッダーに表示させたい任意の文字列　初期値:無効<br>
# 
# 戻り値：なし
# ***
# `checkConnivent(list1, list2, value)`<br>
# 
# 2つの2次元配列の各要素の差を調べすべてがvalueいかなら真を返す関数
# 
# list1   :任意の2次元配列<br>
# list2   :任意の2次元配列<br>
# value   :差の設定値<br>
# 
# 戻り値：bool
# ***
# `kachihanpuku(V, R, miss=None, connError = 1)`<br>
# 
# 価値反復の計算を行う関数
# 
# V    :価値を定義した配列<br>
# R    :ペナルティを定義した配列<br>
# miss :移動の際に間違って他のノードに入る確率　初期値：無効<br>
# connError:すべての要素がこの値以下になったら収束したとみなす<br>
# 
# 戻り値：ノードの価値(list),方策を示す矢印(list)
# 
# ***

# In[1]:

import copy

def argMax(V, R, x, y,cost=1, miss=None):
    xmax = len(V[0])-1
    ymax = len(V)-1
    Vster = []
    Varror = []
    correct = 1.0 
    
    #ノードゴールなら0とドットを返す
    if V[y][x]==0:
        return 0,"・"
    
    #ノードの上下左右に移動したときの価値とその方向を計算
    if x>0 and V[y][x-1] is not None:
        Vster.append(V[y][x-1] - cost - R[y][x-1]) 
        Varror.append("←")
        correct -= 0.1
    if x<xmax and V[y][x+1] is not None:
        Vster.append(V[y][x+1] - cost - R[y][x+1])
        Varror.append("→")
        correct -= 0.1
    if y>0 and V[y-1][x] is not None:
        Vster.append(V[y-1][x] - cost - R[y-1][x])
        Varror.append("↑")
        correct -= 0.1
    if y<ymax and V[y+1][x] is not None:
        Vster.append(V[y+1][x] - cost - R[y+1][x])
        Varror.append("↓")
        correct -= 0.1
    
    #ノードがなければNoneと空白を返す
    if V[y][x] is None:
        return None,"　"
    
    #最適方策を求める
    arror = Varror[Vster.index(max(Vster))]
    
    #ノードの価値を計算
    if miss is None:
        return max(Vster), arror
    else:
        maxValue = max(Vster)
        
        totalValue = (maxValue) * (correct + miss)
        Vster.remove(maxValue)
        
        for i in Vster:
            totalValue += i * miss
            
        Vster.append(maxValue)
        
        return totalValue, arror
    

def showValueMap(V, header = None):
    #ヘッダーがあれば表示
    if header is not None:
        print header
    
    #配列を分解して少数丸めたりunicode表示したり
    for x in V:
        if type(V[0][0])==float:
            print "[",
            for i in x:
                if i==None:
                    print str(i).rjust(7),
                    print ',',
                else :
                    print '{:7.2f}'.format(i),
                    print ',',
            print "]"
            
        elif type(V[0][0])==int:
            print "[",
            for i in x:
                print "{0:4d}".format(i),
            print "]"
            
        else:
            print str(x).decode("string-escape")
    
    #区切りのハイフン
    print "----------------------"

def checkConnivent(list1, list2, value):
    #チェックリストの初期化
    checkList = []
    
    #各要素の差がvalue以下ならチェックリストにTureを入れてく
    for y in range(len(list1)):
            for x in range(len(list1[0])):
                if list1[y][x] == None:
                    checkList.append(True)
                else:
                    checkList.append(abs(list1[y][x] - list2[y][x]) <= value)
                
    #チェックリストのすべての要素がTrueか確認
    return all(elem == True for elem in checkList)
    

def kachihanpuku(V, R, miss=None, connError = 1):
    #配列の初期化とコピー
    Vpre = copy.deepcopy(V)
    
    #与えられた配列の大きさが変わっても対応できる
    Vster =  [[0 for i in range(len(V[0]))] for j in range(len(V))]
    Varror = [[0 for i in range(len(V[0]))] for j in range(len(V))]
    i = 1
   
    #各要素の価値を計算
    while True:
        for y in range(len(V)):
            for x in range(len(V[y])):
                Vster[y][x],Varror[y][x] = argMax(Vpre, R, x, y, miss=miss)
        
        #計算途中の価値を表示
        showValueMap(Vster, "sweep "+str(i))
        i+=1
        
        #前回との差が一定なら収束したとみなして計算終了
        if checkConnivent(Vpre,Vster,connError):
            break
            
        Vpre = copy.deepcopy(Vster)
    
    return Vster, Varror


# # 問題1
# 
# <img src="https://lab.ueda.asia/wp-content/uploads/2016/11/questions1.png" width=200>
# 
# - エージェントが上図のようなグラフの環境を移動
# - エージェントは辺で結ばれたノードに1秒で移動可能
# - Gと書いてあるノードはゴール
# - 各ノードに対して価値反復で価値を求めてみましょう。
#     - 価値はゴールまでの秒数

# ## 回答1
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-10に設定

# In[2]:

print "問題1"
V=[[-10, -10,  0],
   [-10, -10, -10],
   [-10, -10, -10]]

R=[[0, 0, 0],
   [0, 0, 0],
   [0, 0, 0]]

ValueMap, ArrorMap = kachihanpuku(V, R)

print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説1
# 
# - 5回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -2   -1    0 ]
# [   -3   -2   -1 ]
# [   -4   -3   -2 ]
# ----------------------
# ---Arror Map---
# ['→', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```

# # 問題2
# 
# <img src="https://lab.ueda.asia/wp-content/uploads/2016/11/questions2.png" width=200>
# 
# - 今度は、灰色のノードに水たまりがあるとします。
# - 水たまりに入るペナルティーをRとします。
# - 以下の場合の各状態の価値を求めましょう。
#     - R=1[s]
#     - R=10[s]

# ## 回答2-1 
# 
# R = 1[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-10に設定
# - 水たまりの部分のペナルティを1に設定
#     - `R[0][1] = 1`

# In[3]:

print "問題2-1"
V=[[-10, -10,  0],
   [-10, -10, -10],
   [-10, -10, -10]]

R1=[[0, 1, 0],
   [0, 0, 0],
   [0, 0, 0]]

print "水たまりのペナルティが1の場合"
ValueMap,ArrorMap = kachihanpuku(V, R1)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説2-1
# 
# - 5回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -3   -1    0 ]
# [   -3   -2   -1 ]
# [   -4   -3   -2 ]
# ----------------------
# ---Arror Map---
# ['→', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# 水たまりのペナルティがR=1の場合、左上(0,0)をスタートとするとArror Mapの通り、水たまりに入ったほうが早いという結果になった

# ## 回答2-2 
# 
# R = 10[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-10に設定
# - 水たまりの部分のペナルティを1に設定
#     - `R[0][1] = 10`

# In[4]:

print "問題2-2"
R2=[[0, 10, 0],
   [0, 0, 0],
   [0, 0, 0]]

print "水たまりのペナルティが10の場合"
ValueMap,ArrorMap = kachihanpuku(V, R2)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説2-2
# 
# - 5回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -4   -1    0 ]
# [   -3   -2   -1 ]
# [   -4   -3   -2 ]
# ----------------------
# ---Arror Map---
# ['↓', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# 左上(0,0)をスタートとするとR=10の場合は、水たまりを回避し一度下に移動したほうがいいという方策が得られた

# # 問題3
# 
# <img src="https://lab.ueda.asia/wp-content/uploads/2016/11/questions1.png" width=200>
# 
# - 今度は、移動するエッジを選んでノードを移る時に、他のエッジに間違って入ることがある場合を考えましょう。
# - 間違える確率: 移動するエッジ以外のエッジがある場合、それらのエッジにそれぞれ10%の確率で入る
#     - 例: 4つエッジがあるノードの場合、正しく移動できる確率は70%、あとは10%ずつ間違えたエッジに入る

# ## 回答3
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　`miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする　`error=1`

# In[5]:

print "問題3"
V=[[-100, -100,    0],
   [-100, -100, -100],
   [-100, -100, -100]]

R=[[0, 0, 0],
   [0, 0, 0],
   [0, 0, 0]]

miss = 0.1
error= 1

ValueMap,ArrorMap = kachihanpuku(V, R, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説3
# 
# - 11回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -3.21 ,   -1.68 ,    0.00 , ]
# [   -4.57 ,   -3.57 ,   -1.68 , ]
# [   -6.49 ,   -4.57 ,   -3.21 , ]
# ----------------------
# ---Arror Map---
# ['→', '→', '・']
# ['↑', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# 左中段(0,1)が問題1とは違い上に移動するという結果になった。

# # 問題4
# 
# <img src="https://lab.ueda.asia/wp-content/uploads/2016/11/questions2.png" width=200>
# 
# - 今度は水たまりがある時について、問題3の遷移条件で解いてみましょう
# - 水たまりのペナルティー
#     - R=1[s]
#     - R=10[s]
#     - R=100[s]

# ## 回答4-1
# 
# R = 1[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R1[0][1]=1`

# In[6]:

print "問題4-1"
V=[[-100, -100,    0],
   [-100, -100, -100],
   [-100, -100, -100]]

R1=[[0, 1, 0],
   [0, 0, 0],
   [0, 0, 0]]

miss = 0.1
error = 1

print "水たまりのペナルティが1の場合"
ValueMap,ArrorMap = kachihanpuku(V, R1, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説4-1
# 
# - 12回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -4.04 ,   -1.81 ,    0.00 , ]
# [   -5.12 ,   -3.44 ,   -1.70 , ]
# [   -5.67 ,   -4.63 ,   -2.99 , ]
# ----------------------
# ---Arror Map---
# ['→', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# Arror Mapから最適方策は回答2-1と同じものになった

# ## 回答4-2
# 
# R = 10[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R2[0][1]=10`

# In[7]:

print "問題4-2"
V=[[-100, -100,    0],
   [-100, -100, -100],
   [-100, -100, -100]]

R2=[[0, 10, 0],
   [0, 0, 0],
   [0, 0, 0]]

miss = 0.1
error = 1

print "\n"
print "水たまりのペナルティが10の場合"
ValueMap,ArrorMap = kachihanpuku(V, R2, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説4-2
# 
# - 13回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -8.35 ,   -2.31 ,    0.00 , ]
# [   -6.22 ,   -4.72 ,   -1.79 , ]
# [   -6.14 ,   -4.62 ,   -3.16 , ]
# ----------------------
# ---Arror Map---
# ['↓', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# Arror Mapから最適方策は回答2-2と同じものになり水たまりを回避するようになった

# ## 回答4-3
# 
# R = 100[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R3[0][1]=100`

# In[8]:

print "問題4-3"
V=[[-100, -100,    0],
   [-100, -100, -100],
   [-100, -100, -100]]

R3=[[0, 100, 0],
   [0, 0, 0],
   [0, 0, 0]]

miss = 0.1
error = 1

print "水たまりのペナルティが100の場合"
ValueMap,ArrorMap = kachihanpuku(V, R3, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説4-3
# 
# - 15回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [  -22.64 ,   -4.82 ,    0.00 , ]
# [  -11.78 ,  -15.59 ,   -3.00 , ]
# [   -8.71 ,   -6.99 ,   -4.46 , ]
# ----------------------
# ---Arror Map---
# ['↓', '→', '・']
# ['↓', '→', '↑']
# ['→', '→', '↑']
# ----------------------
# ```
# 今度は左中段(0,1)から右へ進むと間違って水たまりに入る可能性があり、そのコストが高い(R=100)のため、水たまりを大きく迂回する下方向への方策を得ている

# # 問題5
# 
# <img src="https://lab.ueda.asia/wp-content/uploads/2016/11/questions3-215x300.png" width=200>
# 
# - 問題4の設定で、グラフにゴールを一つ加えます。
# - 上下二つのゴールのうち、下のゴールの価値や水たまりのペナルティーの値を変えて価値関数を解いてみましょう。
# 
# 今回はゴールの価値を変えず、水たまりのペナルティだけを変更した

# ## 回答5-1
# 
# R = 1[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - ノードのない部分は`None`で定義
#     - `V[3][0] =None`
#     - `V[3][1] =None`
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R1[0][1]=1`

# In[9]:

print "問題5-1"
V=[[-100, -100,     0],
   [-100, -100, -100],
   [-100, -100, -100],
   [ None,  None,     0]]

R1=[[0, 1, 0],
   [0, 0, 0],
   [0, 0, 0],
   [None, None, 0]]

miss = 0.1
error = 1

print "水たまりのペナルティが1の場合"
ValueMap,ArrorMap = kachihanpuku(V, R1, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説5-1
# 
# - 9回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -4.32 ,   -1.84 ,    0.00 , ]
# [   -5.00 ,   -3.40 ,   -1.53 , ]
# [   -4.84 ,   -3.21 ,   -1.52 , ]
# [    None ,    None ,    0.00 , ]
# ----------------------
# ---Arror Map---
# ['→', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↓']
# ['　', '　', '・']
# ----------------------
# ```
# 回答4-1と似た方策になった。
# 右下(2,2)のノードだけ下のゴールに入る方策になった。

# ## 回答5-2
# 
# R = 10[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - ノードのない部分は`None`で定義
#     - `V[3][0] =None`
#     - `V[3][1] =None`
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R2[0][1]=10`

# In[10]:

print "問題5-2"
V=[[-100, -100,     0],
   [-100, -100, -100],
   [-100, -100, -100],
   [ None,  None,     0]]

R2=[[0, 10, 0],
   [0, 0, 0],
   [0, 0, 0],
   [None, None, 0]]

miss = 0.1
error = 1

print "水たまりのペナルティが10の場合"
ValueMap,ArrorMap = kachihanpuku(V, R2, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説5-2
# 
# - 11回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [   -7.84 ,   -2.27 ,    0.00 , ]
# [   -5.86 ,   -4.32 ,   -1.59 , ]
# [   -4.53 ,   -3.13 ,   -1.49 , ]
# [    None ,    None ,    0.00 , ]
# ----------------------
# ---Arror Map---
# ['↓', '→', '・']
# ['→', '→', '↑']
# ['→', '→', '↓']
# ['　', '　', '・']
# ----------------------
# ```
# 回答4-2と似た方策になった。
# 左上(0,0)のノードは水たまりを迂回する方策となっている。
# 右下(2,2)のノードだけ下のゴールに入る方策になった。

# ## 回答5-3
# 
# R = 100[s]
# 
# - ゴールの価値を0に設定
# - ゴール以外のノードの初期値を-100に設定
# - ノードのない部分は`None`で定義
#     - `V[3][0] =None`
#     - `V[3][1] =None`
# - 間違えて他のノードに入る確率をそれぞれ0.1に設定　
#     - `miss=0.1`
# - 計算中にすべてのノードで前回との差が1以下になったら収束したとする
#     - `error=1`
# - 水たまりの部分のペナルティを1に設定 　
#     - `R3[0][1]=100`

# In[11]:

print "問題5-3"
V=[[-100, -100,     0],
   [-100, -100, -100],
   [-100, -100, -100],
   [ None,  None,     0]]

R3=[[0, 100, 0],
   [0, 0, 0],
   [0, 0, 0],
   [None, None, 0]]

miss = 0.1
error = 1

print "水たまりのペナルティが100の場合"
ValueMap,ArrorMap = kachihanpuku(V, R3, miss, error)
print "\n------solution ------\n"
showValueMap(ValueMap , "---Value Map---")
showValueMap(ArrorMap, "---Arror Map---")


# ## 解説5-3
# 
# - 12回の計算で収束した
# - 最終的な各ノードの価値は上記の`Value Map`に示す
# - `Value Map`から各ノードから隣接するノードへの移動を`Arror Map`に示す
# 
# ```
# ---Value Map---
# [  -20.59 ,   -4.62 ,    0.00 , ]
# [   -9.72 ,  -14.84 ,   -2.67 , ]
# [   -6.17 ,   -4.54 ,   -1.73 , ]
# [    None ,    None ,    0.00 , ]
# ----------------------
# ---Arror Map---
# ['↓', '→', '・']
# ['↓', '→', '↑']
# ['→', '→', '↓']
# ['　', '　', '・']
# ----------------------
# ```
# 回答4-3と似た方策になった。
# 左中段(1,0)のノードは水たまりを大きく迂回する方策となっている。
# その為下のゴールに入り安い最適方策となった。
