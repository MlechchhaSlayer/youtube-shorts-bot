import random

prompts = [
    "Write a 40-word motivational script for a YouTube Short.",
    "Give a powerful quote in 40 words that inspires people to take action.",
    "Write a 40-word speech about not giving up."
]

def generate_script():
    prompt = random.choice(prompts)
    # For now we simulate the result manually (will automate with Poe or ChatGPT API later)
    print(f"Prompt: {prompt}")
    script = input("Paste AI response here: ")
    with open("scripts/script_1.txt", "w") as f:
        f.write(script)
    return script

if __name__ == "__main__":
    generate_script()
