#get user input for set
def get_set(prompt):
    print(f"enter elements of the (prompt) set, separated by spaces:")
    return set(input().split())

def set_operations(set1, set2):
    print("\nChoose a set oparator:")
    print("1. Union")
    print("2. Intersection")
    print("3. Difference")
    print("4. Sysmmetric difference")
    choice = input("enter number of you choice 1-4: ")

    if choice == "1":
        print("\nUnion of the sets: ")
        print(set1.union(set2))

    elif choice == "2":
        print("\nIntersection of the sets: ")
        print(set1.intersection(set2))

    elif choice == "3":
        print("\nDifference of the sets: ")
        print(set3.difference(set2))

    elif choice == "4":
        print("\nSymmetric difference of the sets: ")
        print(set3.symmetric_difference(set2))

    else:
        print("Invalid choice")

def main():
    print("Welcome to the stes oparations program: ")
    set1 = get_set("first")
    set2 = get_set("second")
    

    set_operations(set1, set2)

if __name__ == "__main__":
    main()
