def generate_time_sources(tsrc, max_value=96):
    """
    Generate a list of time sources with equal spacing from 0 to max_value.
    The number of sources is defined by tsrc.
    """
    # Ensure tsrc is an integer
    tsrc = int(tsrc)
    
    # Calculate spacing based on tsrc and max_value
    spacing = max_value // (tsrc - 1)
    
    # Generate the time sources using spacing
    return [i * spacing for i in range(tsrc)]

# Example usage
tsrc_values = generate_time_sources(24, max_value=96)

# Print result as a non-comma-separated list
print(" ".join(map(str, tsrc_values)))
