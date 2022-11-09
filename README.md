# マトリクス分析ツール

## はじめに

以下のGoogle Spread Sheetの計算処理を行うWeb APIです
https://docs.google.com/spreadsheets/d/10c3or5ufoDtWm1sXgKMLwySM-vxwiUdwiqIhd8Z2_Ds/edit?usp=share_link
（内部のみ公開）

とはいえSheetとは独立した構成になっており、
各種マトリクス分析手法のPythonスクリプトを用いて、
JSON形式のマトリクスデータをJSON形式で返します

## 要件/Requirement 
**必要なライブラリ**
* Python
* pandas
* numpy
* flask

Web Appにはflaskを用いています

## デプロイ

PythonAnywhereでホストしています

- [Official](https://help.pythonanywhere.com/pages/UploadingAndDownloadingFiles)
- [わかりやすいサイト](https://www.google.co.jp/imgres?imgurl=https%3A%2F%2Fogimage.blog.st-hatena.com%2F10328537792365294202%2F8599973812342915803%2F1517489012&imgrefurl=https%3A%2F%2Ftechium.hatenablog.com%2Fentry%2F2018%2F02%2F01%2F214332&tbnid=YXKkKRvjuptlIM&vet=12ahUKEwiI5YWEp6D7AhW2RvUHHSizCRkQMygAegUIARCtAQ..i&docid=5F69A4JwPbPnnM&w=1200&h=630&q=pythonanywhere%20flask&ved=2ahUKEwiI5YWEp6D7AhW2RvUHHSizCRkQMygAegUIARCtAQ)