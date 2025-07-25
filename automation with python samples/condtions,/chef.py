
import pdb
def describe_dish(input_str):
        pdb.set_trace()
        if input_str == "stir-fry":
            print("adding soy sauce for stir-fry")
        elif input_str == "marinade":
            print("mixing soy sauce marinade")
        elif input_str == "dipping sauce":
            print("soy sauce dipping sauce")
        elif input_str == "soup":
            print("adding soy sauce to enhance soup flavor")
        else:
            print("soy sauce is not used in this dish")

if __name__ == "__main__":
    # loop until user types 'q'
    while True:
        user_input = input("Enter a dish type (or type 'q' to quit):  ")
        # break the loop and exit the program
        if user_input.lower() == 'q':
            print("Goodbye!") #break the loop and exit the program
            break
        describe_dish(user_input) #call the function function