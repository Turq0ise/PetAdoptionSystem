def pet_compatibility():
    print("===Pet Compatibility Checker===")

    activity=input("How active are you?(high, med, or low): ")
    space=input("Do you have enough space for a pet?: ")
    time=input("How much time can you spend with a pet?: ")

    dog_score=0
    cat_score=0

    if activity == "high":
        dog_score += 2
    elif activity == "med":
        dog_score += 1
        cat_score += 1
    elif activity == "low":
        cat_score += 2

    if space == "yes":
        dog_score += 1
        cat_score += 1
    else:
        cat_score += 1

    if time == "high":
        dog_score += 2
    elif time == "med":
        dog_score += 1
        cat_score += 1
    elif time == "low":
        cat_score += 2

    print("\n === Compatibility Result ===")
    print("Dog score: ", dog_score)
    print("Cat score: ", cat_score)

    if dog_score >= 4 and dog_score>cat_score:
        print("You are most compatible with a dog")
    elif cat_score >= 4 and dog_score<cat_score:
        print("You are most compatible with a cat") 
    else:
        print("You are currently NOT compatible to adopt any pet")
