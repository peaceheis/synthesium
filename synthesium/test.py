import random

people = ["Adam", "Alex C,", "Alex G", "Anna", "Ben", "Daniel", "Emma", "Heather", "Julianne", "Kate", "Kim", "Michael",
          "Will"]
books = ["Good And Evil", "Nudge", "Last Night At the Telegraph Club", "Influence", "Queen of the Titles", "Shining",
         "Subtract", "Shadow of the Wind", "11/22/63", "Eating Animals", "Marsh King's", "Catching Wind",
         "You'll Be the Death of Me"]

while True:
    input()
    print(people[random.randint(0, len(people) - 1)], books[random.randint(0, len(books) - 1)])
