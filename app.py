# coding: UTF-8
import sys
from flask import Flask, request, jsonify , render_template, session, redirect
import pandas as pd
from pandas import json_normalize
import numpy as np
from pylibrary import DSMClustering, DSMPartitioning, tradeoff, coordinate, utilityChange, ChangePropagation, OperationPreference, tradeoff_diff, coordinate_diff, system1, system2, system4
import traceback

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
    try:
        jsonData = request.get_json(force=True)  # POSTされたJSONを取得
        return jsonify(jsonData)  # JSONをレスポンス
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
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
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/coordinate', methods=['POST'])
def apply_coordinate():
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/clustering', methods=['POST'])
def apply_clustering():
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/partitioning', methods=['POST'])
def apply_partitioning():
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/utility-change', methods=['POST'])
def apply_utilityChange():
    try:
        jsonData = request.get_json(force=True)  # POSTされたJSONを取得
        df1 = pd.DataFrame(jsonData["data_1"]) #Results contain the required data
        df2 = pd.DataFrame(jsonData["data_2"])
        df3 = pd.DataFrame(jsonData["data_3"])
        df4 = pd.DataFrame(jsonData["data_4"])
        output = utilityChange.utility_change(df1, df2, df3, df4)
        print("Analyzing Dataframe successful", file=sys.stderr)
        print(output, file=sys.stderr)
        return jsonify({"data": output})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/change-propagation', methods=['POST'])
def apply_changePropagation():
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/operation-preference', methods=['POST'])
def operation_preference():
    try:
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
        return jsonify({"index":index_list, "columns":columns_list, "data": arrayData})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/coordinate-diff', methods=['POST'])
def solve_coordinate_diff():
    try:
        jsonData = request.get_json(force=True)  # POSTされたJSONを取得
        data_1 = jsonData["data_1"]
        data_1_columns = data_1.pop(0)
        df1 = pd.DataFrame(data_1, columns=data_1_columns).set_index('背反') #Results contain the required data
        data_2 = jsonData["data_2"]
        data_2_columns = data_2.pop(0)
        df2 = pd.DataFrame(data_2, columns=data_2_columns).set_index('調整')
        output = coordinate_diff.coordinateDiff(df1, df2)
        print("Analyzing Dataframe successful", file=sys.stderr)
        print(output, file=sys.stderr)
        return jsonify({"data": output})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/tradeoff-diff', methods=['POST'])
def solve_tradeoff_diff():
    try:
        jsonData = request.get_json(force=True)  # POSTされたJSONを取得
        data_1 = jsonData["data_1"]
        data_1_columns = data_1.pop(0)
        df1 = pd.DataFrame(data_1, columns=data_1_columns).set_index('背反') #Results contain the required data
        data_2 = jsonData["data_2"]
        data_2_columns = data_2.pop(0)
        df2 = pd.DataFrame(data_2, columns=data_2_columns).set_index('調整')
        output = tradeoff_diff.tradeoffDiff(df1, df2)
        print("Analyzing Dataframe successful", file=sys.stderr)
        print(output, file=sys.stderr)
        return jsonify({"data": output})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }

@app.route('/system1', methods=['POST']) #utility-changeを参考にした
def apply_system1():
    try:
        jsonData = request.get_json(force=True)  # POSTされたJSONを取得
        df1 = pd.DataFrame(jsonData["data_1"]) #Results contain the required data
        df2 = pd.DataFrame(jsonData["data_2"])
        output = system1.main(df1, df2)
        print("Analyzing Dataframe successful", file=sys.stderr)
        print(output, file=sys.stderr)
        return jsonify({"data": output})
    except Exception:
        return {
                    'error': "{}".format(traceback.format_exc())
                }    

@app.route('/system2', methods=['POST']) #utility-changeを参考にした
def apply_system2():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    df1 = pd.DataFrame(jsonData["data_1"]) #Results contain the required data
    df2 = pd.DataFrame(jsonData["data_2"])
    output = system2.main(df1, df2)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output, file=sys.stderr)
    return jsonify({"data": output})

@app.route('/system4', methods=['POST']) #utility-changeを参考にした
def apply_system4():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    df1 = pd.DataFrame(jsonData["data_1"]) #Results contain the required data
    df2 = pd.DataFrame(jsonData["data_2"])
    output = system4.main(df1, df2)
    print("Analyzing Dataframe successful", file=sys.stderr)
    print(output, file=sys.stderr)
    return jsonify({"data": output})

if __name__ == "__main__":
    app.run()