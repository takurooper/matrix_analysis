from functools import reduce
import random
import re
import string
import time

from matplotlib import pyplot as plt
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
import pandas as pd

#Clustering Method
# clustering algorithm
def cluster_parameter(dsm, pow_cc=1.0, pow_bid=1.0, pow_dep=4.0, times=2, max_size=0.8, rand=2):
    size = len(dsm)
    cluster_param = {'pow_cc': pow_cc,
                    'pow_bid': pow_bid,
                    'pow_dep': pow_dep,
                    'max_cluster_size': int(max_size * size),
                    'rand_accept': int(rand * size),
                    'rand_bid': int(rand * size),
                    'times': times}
    return cluster_param

def total_cost(dsm, cluster_matrix, cluster_size, cluster_param):
    pow_cc = cluster_param['pow_cc']
    io = np.dot(np.dot(cluster_matrix, dsm), cluster_matrix.T)
    penalty_cluster_size = np.array([pow(item, pow_cc) for item in cluster_size])
    io_intra = np.dot(np.diag(io), penalty_cluster_size)
    io_extra = (np.sum(io) - np.trace(io)) * pow(len(dsm), pow_cc)
    cost = io_intra + io_extra
    return cost

def initialize_elmt_list(dsm_size):
    elmt_list = [item for item in range(0, dsm_size)]
    list_empty = 0
    return elmt_list, list_empty

def pick_elmt(elmt_list):
    list_empty = 0
    elmt = random.choice(elmt_list)
    elmt_list.remove(elmt)
    if len(elmt_list) == 0:
        list_empty = 1
    return elmt, elmt_list, list_empty


def cluster_bids(elmt, dsm, cluster_matrix, cluster_size, cluster_param):
    pow_dep = cluster_param['pow_dep']
    pow_bid = cluster_param['pow_bid']
    max_cluster_size = cluster_param['max_cluster_size']
    dsm_size = len(dsm)
    n_clusters = len(dsm)
    bids = np.zeros(dsm_size)

    for i in range(0, n_clusters):
        bid_in = 0
        bid_out = 0
        for j in range(0, dsm_size):
            if cluster_matrix[i, j] == 1 and j != elmt:
                if dsm[j, elmt] > 0:
                    bid_in = bid_in + dsm[j, elmt]
                elif dsm[elmt, j] > 0:
                    bid_out = bid_out + dsm[elmt, j]
        if cluster_size[i] >= max_cluster_size:
            bids[i] = 0
        else:
            bids[i] = pow(bid_in + bid_out, pow_dep) / pow(cluster_size[i], pow_bid)
    return bids

def accept_bid(bids, cluster_param):
    rand_bid = cluster_param['rand_bid']
    best_bid = np.max(bids)
    best_bid_index = np.argwhere(bids == best_bid).flatten()

    if random.randint(0, rand_bid) == 1:
        bids_remove_best = np.delete(bids, best_bid_index)

        second_best_bid = best_bid
        second_bid_index = best_bid_index
        if len(bids_remove_best) > 0:
            second_best_bid = np.max(bids_remove_best)
            second_bid_index = np.argwhere(bids == second_best_bid).flatten()

        accepted_bid = second_best_bid
        if len(second_bid_index) == 1:
            cluster_index = second_bid_index[0]
        else:
            cluster_index = random.choice(second_bid_index)

    else:
        accepted_bid = best_bid
        if len(best_bid_index) == 1:
            cluster_index = best_bid_index[0]
        else:
            cluster_index = random.choice(best_bid_index)
    return accepted_bid, cluster_index


def process_bids(elmt, dsm, cluster_matrix, cluster_size, cluster_param):
    change = 0
    dsm_size = len(dsm)
    rand_accept = cluster_param['rand_accept']
    bids = cluster_bids(elmt, dsm, cluster_matrix, cluster_size, cluster_param)
    accepted_bid, cluster_index = accept_bid(bids, cluster_param)

    old_cost = total_cost(dsm, cluster_matrix, cluster_size, cluster_param)

    best_current_state = [cluster_matrix, cluster_size, old_cost]

    new_cluster_matrix = np.copy(cluster_matrix)

    elmt_col = np.zeros(dsm_size)
    elmt_col[cluster_index] = 1
    new_cluster_matrix[:, elmt] = elmt_col

    new_cluster_size = np.sum(new_cluster_matrix, axis=1)

    new_cost = total_cost(dsm, new_cluster_matrix, new_cluster_size, cluster_param)

    accept_state = best_current_state

    if new_cost < old_cost:
        change = 1
        accept_state = [new_cluster_matrix, new_cluster_size, new_cost]
        best_current_state = accept_state

    elif new_cost >= old_cost and random.randint(0, rand_accept) == 1:
        change = 1
        accept_state = [new_cluster_matrix, new_cluster_size, new_cost]
    return accept_state, best_current_state, change


def dsm_clustering(dsm, cluster_param, itc=1):
    stable = 0
    dsm_size = len(dsm)
    elmt_list, list_empty = initialize_elmt_list(dsm_size)
    cluster_matrix = np.eye(dsm_size)
    cluster_size = np.ones(dsm_size)
    cost_history = []
    cost = total_cost(dsm, cluster_matrix, cluster_size, cluster_param)
    accept_state = [cluster_matrix, cluster_size, cost]
    states = [accept_state]
    iteration = 0
    times = cluster_param['times']
    max_times = dsm_size * times
    start = time.time()

    if itc == 1:
        while stable == 0 and iteration <= max_times:
            elmt, elmt_list, list_empty = pick_elmt(elmt_list)
            cluster_matrix, cluster_size, cost = accept_state
            accept_state, better_state, change = process_bids(elmt, dsm, cluster_matrix, cluster_size, cluster_param)
            states.append(better_state)
            if change > 0:
                cost_history.append(accept_state[2])
                stable = 0
                elmt_list, list_empty = initialize_elmt_list(dsm_size)
            else:
                stable = list_empty
            iteration += 1

    elif itc == 0:
        while iteration <= max_times:
            elmt, elmt_list, list_empty = pick_elmt(elmt_list)
            cluster_matrix, cluster_size, cost = accept_state
            accept_state, better_state, change = process_bids(elmt, dsm, cluster_matrix, cluster_size, cluster_param)
            states.append(better_state)
            if change > 0:
                cost_history.append(accept_state[2])
                stable = 0
                elmt_list, list_empty = initialize_elmt_list(dsm_size)
            else:
                stable = list_empty
                if stable == 1:
                    elmt_list, list_empty = initialize_elmt_list(dsm_size)
            iteration += 1

    best_cost_history = np.array([item[2] for item in states])
    best_index = np.argmin(best_cost_history)
    best_state = states[int(best_index)]
    cluster_matrix, cluster_size, cost = best_state

    return cluster_matrix, cost, cost_history

# reorder
def reorder_dsm_by_cluster(dsm_matrix, cluster_matrix, dsm_label):
    # place zeros along the diagonals of the DSM matrix.

    length = len(dsm_matrix)
    dsm_matrix = np.tril(dsm_matrix, -1) + np.triu(dsm_matrix, 1) + np.diag(np.zeros(length))

    # find all element-to-cluster assignments

    cluster_num_and_element = np.argwhere(cluster_matrix)
    cluster_number = np.array([item[0] for item in cluster_num_and_element])
    element = np.array([item[1] for item in cluster_num_and_element])

    # sort the element-to-cluster list in ascending order of clusters.

    cluster_list_index = np.argsort(cluster_number)

    new_number_elmts = len(cluster_list_index)

    # Initialization

    temp_dsm_matrix = np.array([np.zeros(len(dsm_matrix)).tolist()])
    new_dsm_label = []
    new_dsm_matrix = np.zeros((new_number_elmts, new_number_elmts))

    #  Get the new rows of the DSM matrix.

    for i in range(0, new_number_elmts):
        new_row = np.array([dsm_matrix[element[cluster_list_index[i]], :].tolist()])
        temp_dsm_matrix = np.append(temp_dsm_matrix, new_row, axis=0)

        new_dsm_label.append(dsm_label[element[cluster_list_index[i]]])

    temp_dsm_matrix = np.delete(temp_dsm_matrix, 0, axis=0)

    # Now add the new columns of the DSM matrix.

    for i in range(0, new_number_elmts):
        new_dsm_matrix[:, i] = temp_dsm_matrix[:, element[cluster_list_index[i]]]

    return new_dsm_matrix, new_dsm_label


def reorder_cluster(cluster_matrix):
    num_clstelm = np.sum(cluster_matrix, axis=1)

    index = np.argsort(num_clstelm)
    flipped_index = np.flipud(index)
    new_cluster_matrix = np.zeros((len(cluster_matrix), len(cluster_matrix)))
    new_cluster_matrix[:, :] = cluster_matrix[flipped_index, :]

    return new_cluster_matrix

def place_diag(old_matrix, diagonal_element):
    diag_matrix = np.diag(diagonal_element * np.ones(len(old_matrix)))
    new_matrix = np.tril(old_matrix, -1) + np.triu(old_matrix, 1) + diag_matrix

    return new_matrix

def DSM_clustering(input_dsm):
    pow_cc=3.0
    pow_bid=0.0
    pow_dep=1.0
    times=60
    max_size=0.8
    rand=2
    itc=1

    dsm_label = input_dsm.columns.tolist()
    dsm_matrix = input_dsm.values
    cluster_param = cluster_parameter(dsm_matrix, pow_cc=pow_cc, pow_bid=pow_bid, pow_dep=pow_dep,
                                    times=times, max_size=max_size, rand=rand)
    cluster_matrix, total_coord_cost, cost_history = dsm_clustering(dsm_matrix, cluster_param, itc=itc)

    cluster_matrix = reorder_cluster(cluster_matrix)
    (new_dsm_matrix, new_dem_labels) = reorder_dsm_by_cluster(dsm_matrix, cluster_matrix, dsm_label)
    new_dsm_matrix = place_diag(new_dsm_matrix, 1)
    new_dsm_matrix = np.around(new_dsm_matrix, decimals=4)

    df = pd.DataFrame(new_dsm_matrix, columns=new_dem_labels, index=new_dem_labels)
    return df