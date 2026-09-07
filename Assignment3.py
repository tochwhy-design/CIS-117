# Homework 3
# Author: Zhaochun Fu
# Date: September 7, 2026

highway = int(input("Enter a highway number: "))

if highway <= 0 or highway > 999:
    print("Invalid highway number.")

elif highway <= 99:
    if highway % 2 == 0:
        print(f"Interstate {highway} runs east/west.")
    else:
        print(f"Interstate {highway} runs north/south.")

else:
    primary = highway % 100

    if primary % 2 == 0:
        direction = "east/west"
    else:
        direction = "north/south"

    print(
        f"Interstate {highway} is an auxiliary highway serving I-{primary}, "
        f"which runs {direction}."
    )