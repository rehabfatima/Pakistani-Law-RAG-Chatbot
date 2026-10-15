
def check_scope(question):
    """Check whether a question relates to the selected Pakistani law."""

    keywords = [
        "child marriage",
        "child",
        "minor",
        "under 18",
        "under eighteen",
        "marriage",
        "married",
        "nikah",
        "minimum age",
        "age for marriage",
        "punishment",
        "penalty",
        "fine",
        "imprisonment",
        "registrar",
        "guardian",
        "parent",
        "section",
        "islamabad capital territory",
        "restraint act",
        "legal age"
    ]

    question = " ".join(question.lower().split())

    for keyword in keywords:
        if keyword in question:
            return True

    return False


if __name__ == "__main__":
    question = input("Enter your question: ")

    if check_scope(question):
        print("Question is IN SCOPE.")
    else:
        print("Question is OUT OF SCOPE.")

