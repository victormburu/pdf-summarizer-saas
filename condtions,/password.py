import pdb
pdb.set_trace()
def char(input_string):
    """Return the first character of the password."""
    if len(input_string) != 10:
        print("Input must be exactly 10 characters.")
    elif not input_string.islower():
        print("Input must be a lowercase letter.")
    elif input_string[0] in "aeiou":
        raise ValueError("Input must be a consonant.")
    elif input_string[0] in "bcdfghjklmnpqrstvwxyz":
        raise ValueError("Input must be a vowel.")
    else:
        return input_string[0]

if __name__ == "__main__":
    user_input = input("Enter a 10-character lowercase string: ")
    try:
        result = char(user_input)
        if result:
            print(f"The first character of the password is: {result}")
    except ValueError as e:
        print(e)