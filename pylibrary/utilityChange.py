#価値-機能3種類-Act4種類-構造4種類のネットワークを考えてみる

def utility_change(df1, df2, df3, df4):
#構造→提供Actへのリンク
    dF1 = df1.T

#提供Act→機能3種類へのリンク
    dF2 = df2.T

#機能3種類→価値へのリンク
    dF3 = df3.T
    return dF3.dot(dF2.dot(dF1.dot(df4)))[0][0]