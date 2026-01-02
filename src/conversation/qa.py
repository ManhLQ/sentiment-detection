import dspy
import os

class QA(dspy.Signature):
    """Answer the question based on conversation history."""
    question: str = dspy.InputField(desc="Question to answer")
    history: dspy.History = dspy.InputField(desc="Conversation history")
    answer: str = dspy.OutputField(desc="Answer to the question")

def run_interactive_chat():
    """Start an interactive QA session."""
    predict = dspy.Predict(QA)
    history = dspy.History(messages=[])

    print("--- DSPy Interactive Chat ---")
    print("Type 'finish' or 'exit' to end the conversation.")
    
    while True:
        try:
            question = input("\nYou: ")
            if question.lower() in ["finish", "exit", "quit"]:
                break
            
            if not question.strip():
                continue
                
            outputs = predict(question=question, history=history)
            
            # Update history
            history.messages.append({"question": question, "answer": outputs.answer})
            
            print(f"Assistant: {outputs.answer}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    print("\n--- Conversation Ended ---")
    dspy.inspect_history()

# No standalone execution here to keep functionality pure.
# Run via dspy-agent chat or src/cli.py