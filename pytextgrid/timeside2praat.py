from PraatTextGrid import PraatTextGrid, Tier, Interval

def segLabelRes2Tg(slr, infoname):
    """
    Convert Timeside SegmentLabelResult class to PraatTextGrid
    """
    labels = slr.data_object.label
    times = slr.data_object.time
    durations = slr.data_object.duration
    totaldur = (times[-1] + durations[-1])
    print 'total dur', totaldur
    
    ptg = PraatTextGrid(xmax = totaldur)
    tier = Tier(xmax = totaldur, name=infoname)
    ptg.append(tier)

    for lab, tim, dur in zip(labels, times, durations):
        tier.append(Interval(tim, tim+dur, str(lab)))

    return ptg

