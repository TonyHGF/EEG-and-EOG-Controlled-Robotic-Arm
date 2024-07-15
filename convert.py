def convert_signed_to_unsigned(signed_int):
    # Check if the signed integer is negative
    if signed_int < 0:
        # Convert the signed integer to its two's complement representation
        unsigned_int = (1 << 24) + signed_int
    else:
        unsigned_int = signed_int

    return unsigned_int


adc_to_microvolts = 5 / (1 << 24)

val = -8386041

res = convert_signed_to_unsigned(val)

print(res * adc_to_microvolts)