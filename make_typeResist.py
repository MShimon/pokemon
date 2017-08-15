#coding:utf-8

####################
#Author：MShimon
#Date：2017/7/19
#Abstract：単タイプの耐性表を用いて、全複合タイプの耐性表を作成する
####################

#-moduleのimport-#
import pandas as pd

#タイプをリストとして定義する
typelist=["ノーマル","ほのお","みず","くさ","でんき","こおり","かくとう","どく","じめん","ひこう","エスパー","むし","いわ","ゴースト","ドラゴン","あく","はがね","フェアリー"]
#csvファイルの読み込み
#読み込むときはtype[防御する側のタイプ][攻撃する側のタイプ]
type = pd.read_csv('data/TypeComp.csv',encoding='SHIFT-JIS',index_col = 0)

#-全タイプの組み合わせを作る-#
#全タイプの組み合わせを保存するリスト
typelist_all = []
#タイプの組み合わせをやるための2重forループ
for type1 in typelist:
    for type2 in typelist:
        ##条件によりタイプをリストに追加していく
        #条件１：単タイプなら追加
        if type1 == type2:
            typelist_all.append([type1])
            break
        #条件２：リスト内に存在していなければ追加
        tmp1 = [type1,type2]
        tmp2 = [type2,type2]
        if not((tmp1 in typelist_all)or(tmp2 in typelist_all)) : typelist_all.append(tmp1)
#デバッグ用のprint
"""
for type in typelist_all:
    print (len(type))
"""
##各複合タイプの耐性を計算する##
#計算結果はpandasにデータフレームに格納してcsvに保存
tmp_rst = []#耐性の結果を一時的に保存するリスト
#データフレームのcolumnを作成する
list_dfcol = ["タイプ１","タイプ２"]
list_dfcol.extend(typelist)
df_type = pd.DataFrame(columns=list_dfcol)#空のDataframe
for l in typelist_all:
    #単タイプの場合
    if len(l) == 1:
        tmp_rst.append(l[0])#タイプ１をリストに追加、タイプ２はNoneに
        tmp_rst.append(None)
        for t in typelist:
            tmp_rst.append(type[l[0]][t])#耐性の値を参照
    #複合タイプの場合　単タイプの場合とほぼ同様
    else:
        tmp_rst.append(l[0])
        tmp_rst.append(l[1])
        for t in typelist:
            tmp_rst.append(type[l[0]][t] * type[l[1]][t])#耐性の計算は、単タイプ時の掛け合わせで計算
    #データフレームへの追加は
    #①リスト→シリーズに変換
    #②作成したシリーズをデータフレームに追加の手順で行う
    tmp_ser = pd.Series(tmp_rst,index=df_type.columns)
    df_type = df_type.append(tmp_ser, ignore_index=True)
    #リストを初期化
    tmp_rst = []

#作成したデータフレームをcsvに保存する
df_type.to_csv("data/タイプ耐性表.csv",encoding="SHIFT-JIS",index=False)