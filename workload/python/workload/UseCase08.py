"""
DISCLAIMER

This file shows only the additions that we made to this use case.
Since the copyrights of the original TPCx-AI benchmark code belongs to the Transaction Processing Performance Council (TPC) and/or its contributors,
we omit all code belonging to them. 
Instead, we simply provide our own code as it should be placed at certain lines of the corresponding file.

We prefix the lines with their destination line numbers as a comment.

Additional lines are prefixed with a '+' character
"""

# 88
    def scan_count(values, index):
        return np.sum(values)

# 91
    def scan_count_abs(values, index):
        return np.sum(np.abs(values))

# 94
    def weekday(values, index):
        return np.min(values)

# 97
    def trip_type(values, index):
        return np.min(values)

# 100
# +
    if has_labels:
# 101
        agg_func = {
            'scan_count': [scan_count, scan_count_abs],
            'weekday': weekday,
            'trip_type': trip_type
        }
    else:
        agg_func = {
            'scan_count': [scan_count, scan_count_abs],
            'weekday': weekday,
        }

# 112 - 134 (all lines after 134 in the original code should be kept as is)
    raw_data['scan_count'] = raw_data['quantity']

    raw_data['weekday'] = raw_data['date'].dt.dayofweek

    features_scan_count = raw_data.groupby(['o_order_id'])

    manager = mp.Manager()
    return_dict = manager.dict()
    engine_kwargs = {"nopython":False, "nogil":False, "parallel":False}

    def agg_count_abs(input_df, return_dict):
        print("agg count abs started")
        df = pd.DataFrame(input_df["scan_count"].agg(scan_count_abs, engine="numba", engine_kwargs=engine_kwargs, raw=True))
        df.columns = ["scan_count_abs"]
        return_dict[1] = df
        print("agg count abs ended")

    def agg_count(input_df, return_dict):
        print("agg count started")
        return_dict[2] = pd.DataFrame(input_df["scan_count"].agg(scan_count, engine="numba", engine_kwargs=engine_kwargs, raw=True))
        print("agg count ended")

    def agg_weekday(input_df, return_dict):
        print("agg weekday started")
        return_dict[3] = pd.DataFrame(input_df["weekday"].agg(weekday, engine="numba", engine_kwargs=engine_kwargs, raw=True))
        print("agg weekday ended")

    def agg_trip_type(input_df, return_dict):
        print("agg trip type started")
        return_dict[4] = pd.DataFrame(input_df["trip_type"].agg(trip_type, engine="numba", engine_kwargs=engine_kwargs, raw=True))
        print("agg trip type ended")

    p1 = mp.Process(target=agg_count_abs, args=(features_scan_count, return_dict))
    p2 = mp.Process(target=agg_count, args=(features_scan_count, return_dict))
    p3 = mp.Process(target=agg_weekday, args=(features_scan_count, return_dict))

    p1.start()
    p2.start()
    p3.start()
    if has_labels:
        p4 = mp.Process(target=agg_trip_type, args=(features_scan_count, return_dict))
        p4.start()
        p4.join()
    p1.join()
    p2.join()
    p3.join()

    dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    return_dict[3]["weekday"] = return_dict[3]["weekday"].map(dayOfWeek)

    if has_labels:
        features_scan_count = (return_dict[1]
                        .join(return_dict[2])
                        .join(return_dict[3])
                        .join(return_dict[4]))
    else:
        features_scan_count = (return_dict[1]
                        .join(return_dict[2])
                        .join(return_dict[3]))
