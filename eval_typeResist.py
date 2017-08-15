#coding:utf-8

####################
#Author：MShimon
#Date：2017/7/19
#Abstract：単タイプの耐性表を用いて、全複合タイプの耐性表を作成する
####################

#-moduleのimport-#
import pandas as pd

#複合タイプの耐性csvファイルの読み込み
type_res = pd.read_csv('data/タイプ耐性表.csv',encoding='SHIFT-JIS')

##forループで全タイプに対して評価値を計算する
##計算した評価値はdataframeに保存してからcsv
#全部の複合タイプの数を取得
len_type = len(type_res)
#columnの一覧（タイプ耐性の一覧）を表示
head = type_res.columns
type_list = list(head)#タイプ耐性の一覧を表示
##csvファイルの検索に使うために、columnからタイプ１とタイプ２を除く
remove_list = ["タイプ１","タイプ２"]#除く要素を追加
[type_list.remove(name) for name in remove_list]#リスト内包表記で一気に取り除く

tmp_rst = []#タイプとそのスコアを保存するリスト
list_dfcol = ["タイプ１","タイプ２","スコア"]
df_type = pd.DataFrame(columns=list_dfcol)#空のDataframe
for i in range(len_type):
    col = type_res.iloc[i]#csvファイルを一行ずつ　＝　１タイプずつ耐性を所得
    score = 0#スコアを初期化
    for h in head:#取り出した行に対して、一つずつcolumnを参照
        if h in ["タイプ１","タイプ２"]:
            if col[h] in head:
                tmp_rst.append(col[h])
            else:
                tmp_rst.append(None)
        else:
            score += col[h]
    #tmpリストにスコアを追加
    tmp_rst.append(score)
    #データフレームへの追加は
    #①リスト→シリーズに変換
    #②作成したシリーズをデータフレームに追加の手順で行う
    tmp_ser = pd.Series(tmp_rst,index=df_type.columns)
    df_type = df_type.append(tmp_ser, ignore_index=True)
    #tmpリストの初期化
    tmp_rst = []

#作成したデータフレームをcsvに保存する
df_type.to_csv("data/タイプ評価値表.csv",encoding="SHIFT-JIS",index=False)