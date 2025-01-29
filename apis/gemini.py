# Import necessary packages and define helper function to render output of models to markdown
import requests
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

from google.colab import userdata
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY') # Grab API Key from your secrets
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_template_response(level):
  lsas_responses = {
    'mild': ['https://gist.githubusercontent.com/muallagunay/87c0a8724350b14ced9e143fa69261d3/raw/c9975df295e42399c73fd9ae7127c32d98ef8202/LSAS_results_mild.txt'],
    'moderate': ['https://gist.githubusercontent.com/muallagunay/390c572dd08e76f1863475f8ba2b8afb/raw/6893cacc388a254555b260215f28bcfa4721f827/LSAS_results_moderate.txt'],
    'marked': ['https://gist.githubusercontent.com/muallagunay/9981be8eaceeb7e2efd688b4307d44c9/raw/f86a905d8ee63e44908b6cbffa016b7d827a4fa2/LSAS_results_marked.txt'],
    'severe': ['https://gist.githubusercontent.com/muallagunay/bc2f4f7f0145f56789952f0e721cf07f/raw/85f939fc4f4a06f79e053f83dcd4c186bd986f51/LSAS_results_severe.txt'],
    'very_severe': ['https://gist.githubusercontent.com/muallagunay/cb8d1390215fd23400a7ef4d31e2f838/raw/556b5c035b9f3894098fe0f2163b55ec72cb0230/LSAS_results_very_severe.txt']
  }

  link = lsas_responses[level][0]

  # Get the file content
  response = requests.get(link)

  # Check if the request was successful
  if response.status_code == 200:
      return response.text  # The content of the file as a string

def create_prompt(lsas_response):
  aim = "I am a cognitive behavioral therapist specializing in social anxiety in adults, could you please help me:"

  task_one = (
      "Firstly, analyze the Anonymized LSAS Responses, using the client's responses to each of the 24 items on the Liebowitz Social Anxiety Scale (LSAS)."
      "For analyzing, please do the following: a) Identify the specific social situations that elicit the highest levels of fear and avoidance. "
      "b) Determine the core themes and patterns within the client's responses. Here are the LSAS responses: "
      + lsas_response
  )

  task_two = (
      "Secondly, recommend Tailored Interventions. Do this based on the analyzed LSAS responses. Recommending tailored interventions mean"
      "suggesting and providing instructions for "
      "a) one mindfulness exercise the client can use when they feel anxious today (examples include: Daily "
      "Mindfulness practice (focusing on breath, walking), five senses exercise (Notice 5 see, 4 hear, 3 touch, "
      "2 smell, 1 taste while anxious), anchor statements (‘I can handle this moment.’), self-compassion journaling) "
      "b) one cognitive-behavioral exercise the client can try today to reframe their thoughts (examples include: "
      "Thought records, journaling, cognitive restructuring (replacing negative with positive thoughts)) "
      "c) one way the client can incorporate art or crafting into their life to mitigate anxiety today (examples include: "
      "- Art: emotion drawing, social confidence collage (like a manifest board), visual journaling, self-portrait) "
      "- Music: playlist (that helps you calm), improvisation through playing instruments, reflective listening, voice work "
      "- Drama: role rehearsals, character exploration, storytelling, public speaking practice in private "
      "- Movement: movement journaling, empowerment poses, dance your emotions, social flow practice "
      "- Writing: freewriting about emotions, letter writing (letter to your social anxiety as if it were a person), poetic "
      "reflection, affirmation scripts, alternative happy ending, future visualization, letter to future self "
      "- Crafting: mindful crafting, community workshops, gift creation, craft reflection) "
      "d) one resource the client can check out today (e.g., a book, podcast, movie, TV show, paper, thought piece, "
      "article that expresses the voices of others with social anxiety)"
  )

  prompt = aim + task_one + task_two

  return prompt

# Select a model and instantiate a GenerativeModel
model = genai.GenerativeModel('gemini-1.5-flash')

lsas_response = get_template_response('mild') # 'mild', 'moderate', 'marked', 'severe', 'very_severe'
prompt = create_prompt(lsas_response)

# You can now use the model defind about to generate content base on inputs
response = model.generate_content(prompt)

# This makes the response easier to read
to_markdown(response.text)