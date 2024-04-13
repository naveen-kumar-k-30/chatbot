import random
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import wikipediaapi
import openai

# Define some responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm doing well, thanks for asking!", "I'm good, how about you?", "All good here!"],
    "goodbye": ["Goodbye!", "See you later!", "Bye!"],
    "thanks": ["You're welcome!", "No problem!", "Anytime!"],
    "name": ["I'm ChatGBT, nice to meet you!", "You can call me ChatGBT!", "I'm your friendly ChatGBT!"],
    "age": ["I don't have an age, I'm just a virtual assistant!", "Age is just a number for me!"],
    "default": ["Hmm, I'm not sure I understand.", "Could you please rephrase that?", "I didn't catch that."],
}

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="ChatGBT/1.0"
)

# Set up OpenAI API key
openai.api_key = ""

# Function to perform sentiment analysis
def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound_score = score['compound']
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Function to fetch Wikipedia summary
def fetch_wikipedia_summary(topic):
    page = wiki.page(topic)
    if page.exists():
        return page.summary
    else:
        return None

# Function to perform question answering using OpenAI API
def ask_question(question):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=question,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error:", e)
        return None

# Function to respond to user input
def respond(input_text):
    input_text = input_text.lower()  # Convert input to lowercase
    sentiment = analyze_sentiment(input_text)
    for key in responses.keys():
        if re.search(key, input_text):
            if sentiment == "positive":
                return random.choice(responses[key])
            elif sentiment == "negative":
                return "I'm sorry you're feeling that way."
            else:
                return random.choice(responses[key])
    # If the input doesn't match any predefined responses, try to find information on Wikipedia
    wikipedia_summary = fetch_wikipedia_summary(input_text)
    if wikipedia_summary:
        return wikipedia_summary
    # If Wikipedia search also fails, try question answering
    if "?" in input_text:
        answer = ask_question(input_text)
        if answer:
            return answer
    # Fallback to a default response
    return random.choice(responses["default"])

# Main loop
print("Hello! I'm ChatGBT. Feel free to say hello or ask me how I am.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    response = respond(user_input)
    print("ChatGBT:", response)
