def calculate_thresholds(max_events, levels):
    thresholds = [0]
    for i in range(levels - 1):
        thresholds.append(int(max_events / (levels - 1) * (i + 1)))
    return thresholds