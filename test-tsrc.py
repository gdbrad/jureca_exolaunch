def generate_time_sources(tsrc, max_value=96):
    tsrc = int(tsrc)
    spacing = max_value // (tsrc - 1)
    return [i * spacing for i in range(tsrc)]
tsrc_values = generate_time_sources(24, max_value=96)
print(" ".join(map(str, tsrc_values)))
