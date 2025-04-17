import random

def generate_question(difficulty):
    if difficulty == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"What is {a} + {b}?", a + b
    elif difficulty == 2:
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"What is {a} - {b}?", a - b
    elif difficulty == 3:
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"What is {a} * {b}?", a * b
    elif difficulty == 4:
        a, b = random.randint(1, 100), random.randint(1, 100)
        return f"What is {a} / {b} (round to 2 decimal places)?", round(a / b, 2)
    else:
        # Algebra questions
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"Solve for x: {a}x + {b} = {a * b}", a * b - b

def main():
    score = 0
    difficulty = 1

    while True:
        question, answer = generate_question(difficulty)
        user_answer = input(question + " (type 'quit' to exit) ")

        if user_answer.lower() == 'quit':
            print("Thanks for playing!")
            break

        if user_answer.strip() == "":
            print("Please enter a valid answer or 'quit' to exit.")
            continue

        try:
            if float(user_answer) == answer:
                print("Correct!")
                score += 1
                if score % 3 == 0:  # Increase difficulty every 3 correct answers
                    difficulty += 1
            else:
                print(f"Wrong! The correct answer was {answer}.")
                break
        except ValueError:
            print("Please enter a valid number or 'quit' to exit.")

    print(f"Your final score is: {score}")

if __name__ == '__main__':
    main()
