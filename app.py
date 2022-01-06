# coding: UTF-8
import sys
from flask import Flask, request, jsonify , render_template, session, redirect
import pandas as pd
from pandas import json_normalize
import numpy as np
from pylibrary import DSMClustering, DSMPartitioning, tradeoff, coordinate, utilityChange, ChangePropagation, OperationPreference

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  #JSONでの日本語文字化け対策

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/test/<int:baz>', methods=['POST'])
def post_foobar(baz):
    return 'you posted {}\n'.format(baz)

@app.route('/test/get_json', methods=['GET'])
def get_json_from_dictionary():
    dic = {
        'foo': 'bar',
        'ほげ': 'ふが'
    }
    return jsonify(dic)  # JSONをレスポンス

@app.route('/test/post_json', methods=['POST'])
def post_json():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    try:
        return jsonify(jsonData)  # JSONをレスポンス
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/test/post_dataframe', methods=['POST'])
def post_dataframe():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    #input_df = json_normalize(jsonData["data"]) #Results contain the required data
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print(input_df, file=sys.stderr)
    return "Input Dataframe successful"  # Dataframeをレスポンス

@app.route('/tradeoff', methods=['POST'])
def apply_tradeoff():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print("Input Dataframe successful", file=sys.stderr)
    print(input_df, file=sys.stderr)
    output_df = tradeoff.solve_tradeoff_matrix(input_df)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/coordinate', methods=['POST'])
def apply_coordinate():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print("Input Dataframe successful", file=sys.stderr)
    print(input_df, file=sys.stderr)
    output_df = coordinate.solve_coordinate_matrix(input_df)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/clustering', methods=['POST'])
def apply_clustering():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print("Input Dataframe successful", file=sys.stderr)
    print(input_df, file=sys.stderr)
    output_df = DSMClustering.DSM_clustering(input_df, jsonData["pow_cc"], jsonData["pow_bid"], jsonData["pow_dep"], jsonData["times"], jsonData["max_size"], jsonData["rand"], jsonData["itc"])
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/partitioning', methods=['POST'])
def apply_partitioning():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print("Input Dataframe successful", file=sys.stderr)
    print(input_df, file=sys.stderr)
    output_df = DSMPartitioning.DSM_partitioning(input_df)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/utility-change', methods=['POST'])
def apply_utilityChange():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    df1 = pd.DataFrame(jsonData["data_1"]) #Results contain the required data
    df2 = pd.DataFrame(jsonData["data_2"])
    df3 = pd.DataFrame(jsonData["data_3"])
    df4 = pd.DataFrame(jsonData["data_4"])
    output = utilityChange.utility_change(df1, df2, df3, df4)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output, file=sys.stderr)
    try:
        return jsonify({"data": output})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/change-propagation', methods=['POST'])
def apply_changePropagation():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    input_df = pd.DataFrame(jsonData["data"]) #Results contain the required data
    input_df.index = jsonData["index"]
    input_df.columns = jsonData["columns"]
    #return render_template('simple.html',  tables=[input_df.to_html(classes='data')], titles=input_df.columns.values)
    print("Input Dataframe successful", file=sys.stderr)
    print(input_df, file=sys.stderr)
    output_df = ChangePropagation.Change_propagation_df_DSM(input_df)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

@app.route('/operation-preference', methods=['POST'])
def operation_preference():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    data_1 = jsonData["data_1"]
    data_1_columns = data_1.pop(0)
    df_qfd = pd.DataFrame(data_1, columns=data_1_columns) #Results contain the required data
    data_2 = jsonData["data_2"]
    data_2_columns = data_2.pop(0)
    df_fn_imp = pd.DataFrame(data_2, columns=data_2_columns)
    data_3 = jsonData["data_3"]
    data_3_columns = data_3.pop(0)
    df_dp_precon = pd.DataFrame(data_3, columns=data_3_columns)
    output_df = OperationPreference.main(df_qfd, df_fn_imp, df_dp_precon, jsonData["calc_type"])
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output_df, file=sys.stderr)
    arrayData = output_df.values.tolist()
    index_list = list(output_df.index)
    columns_list = list(output_df.columns)
    try:
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception as e:
        return {
                    'error': "{}".format(e)
                }

if __name__ == "__main__":
    app.run()