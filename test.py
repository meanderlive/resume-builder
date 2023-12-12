def compress_string(s, current_char=None, count=0, result=""):
    if not s:
        print(s)
        return result

    if current_char is None:
        current_char = s[0]
        count = 1
    else:
        if s[0] == current_char:
            count += 1
        else:
            result += current_char + str(count)
            current_char = s[0]
            count = 1

    return compress_string(s[1:], current_char, count, result)

# Example usage:
input_string = "cccggvvvr"
output = compress_string(input_string)
print(output)
