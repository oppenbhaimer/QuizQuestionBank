import os, sys
import re
import json
from typing import Tuple
import requests
import concurrent.futures

prompt = """
<s>[INST] You need to clean up a set of quiz questions into JSON. Exactly copy over the question and the answer. Both question and answer MUST OCCUPY A SINGLE LINE, and your answer must be valid JSON. Follow the format given below:

```json
[
{
    "Q": "question 1",
    "A": "answer 1"
},
{
    "Q": "question 2",
    "A": "answer 2"
},
...
]
```

You MUST make sure each question and answer are a SINGLE LINE STRING, with NO NEWLINE CHARACTERS. Do NOT substitute the answer in the blanks, if there are any blanks in the question. If you have newline characters, your question or answer is incorrect. Also, the question in most cases is always longer than the answer, and precedes the answer. The answer is mostly separated from the question by one or more new line characters. Try not to leave the question or answer empty. [/INST]

Sure, I can help you with that. Can you give me the raw text to clean up?</s>

[INST]
Raw Text:
```text
Q.14

• As the oldest one in Dublin, this football club has a rich heritage in
terms of their sporting culture but their ground’s musical history is
something that truly captures their fans imagination.

• At the beginning of this year, they announced a special away
jersey (pic on the next slide) as a tribute to someone whose last
live performance took place in their ground.

• This musicians’ style and attitude were perhaps a subtle nod to
the name of the club which also had the likes of Queen and U2
perform once in their ground.



SAFETY

SLIDE


Bohemian FC, Bob Marley

A.14


What detail is being talked about and 

why the change?

Q.15

• When this artist completed his magnum opus, the cardinals
responsible for curating the works stayed for hours looking and
admiring the magnificent display. After analysis, they met with the
master of the arts and shouted “REMAKE”.

• The discontent was not with all the work, but with one detail. The
artist had conceived the most famous panel with two entities
touching. The curators demanded that there be no touch, but that
both entities be distant and more: that one entity was always
stretched to the max, but the other one had the last phalanges.


SAFETY

SLIDE


The hands of Adam and God in 

The Creation of Adam
```

Questions:[/INST]
```json
[
{
	"Q": "As the oldest one in Dublin, this football club has a rich heritage in terms of their sporting culture but their ground’s musical history is something that truly captures their fans imagination. At the beginning of this year, they announced a special away jersey (pic on the next slide) as a tribute to someone whose last live performance took place in their ground. This musicians’ style and attitude were perhaps a subtle nod to the name of the club which also had the likes of Queen and U2 perform once in their ground.",
	"A": "Bohemian FC, Bob Marley"
},
{
	"Q": "When this artist completed his magnum opus, the cardinals responsible for curating the works stayed for hours looking and admiring the magnificent display. After analysis, they met with the master of the arts and shouted “REMAKE”. The discontent was not with all the work, but with one detail. The artist had conceived the most famous panel with two entities touching. The curators demanded that there be no touch, but that both entities be distant and more: that one entity was always stretched to the max, but the other one had the last phalanges. What detail is being talked about and why the change?",
	"A": "The hands of Adam and God in The Creation of Adam"
}
]
```</s>

[INST]
Raw Text:
```text
Ques 10)

X is a Turkish software engineer who 

obtained a B.Sc in Computer engineering 
from Bilkent Univ ,Ankara

And a Phd in Computer Science from 

Stanford University.

He is engaged to his boy friend Derek 

X is known for his project Y which he  

launched in 2004.

What are we talking about?(identify X and the 

Holbrook.

project)

 

 

Ans)

The founder of Orkut:
Orkut Buyukkokten

 

 

Ques 11)

Moving from left to right,who are the other two people to complete the list
 

 

Ans)

Ronaldo and Miroslav klose

 

 

Ques 12)
“   Rules of the Garage: Believe you can change the 
world. Work quickly, keep the tools unlocked, work 
whenever. Know when to work alone and when to 
work together. Share - tools, ideas. Trust your 
colleagues. No politics. No bureaucracy. (These 
are ridiculous in a garage.) The customer defines 
a job well done. Radical ideas are not bad ideas. 
Invent different ways of working. Make a 
contribution every day. If it doesn't contribute, it 
doesn't leave the garage. Believe that together we 
can do anything." 

What are we talking about?

 

 

Ans)

   These rules are that of the garage 

where Hewlett and Packard first 
started their company.

 

 

Ques 13)

For work on model checking with finite automata
 For the PCP theorem and its applications to 

hardness of approximation,

For proving that equivalence of deterministic 

pushdown automata is decidable

For the AdaBoost algorithm
 For applications of topology to the theory of 

distributed computing

For the foundational contribution to streaming 

algorithms

For the ????!!!

 

 

Ans)

AKS Primality test

 
```

Questions:[/INST]
```json
[
{
	"Q": "X is a Turkish software engineer who obtained a B.Sc in Computer Engineering from Bilkent Univ, Ankara and a PhD in Computer Science from Stanford University. He is engaged to his boyfriend Derek. X is known for his project Y which he launched in 2004. What are we talking about? (Identify X and the project)",
	"A": "The founder of Orkut: Orkut Buyukkokten"
},
{
	"Q": "Moving from left to right,who are the other two people to complete the list",
	"A": "Ronaldo and Miroslav Klose"
},
{
	"Q": "\"Rules of the Garage: Believe you can change the world. Work quickly, keep the tools unlocked, work whenever. Know when to work alone and when to work together. Share - tools, ideas. Trust your colleagues. No politics. No bureaucracy. (These are ridiculous in a garage.) The customer defines a job well done. Radical ideas are not bad ideas. Invent different ways of working. Make a contribution every day. If it doesn't contribute, it doesn't leave the garage. Believe that together we can do anything.\" What are we talking about?" 
	"A": "These rules are that of the garage where Hewlett and Packard first started their company."
},
{
    "Q": "For work on model checking with finite automata, For the PCP theorem and its applications to hardness of approximation, For proving that equivalence of deterministic pushdown automata is decidable, For the AdaBoost algorithm, For applications of topology to the theory of distributed computing, For the foundational contribution to streaming algorithms, For the ????!!!"
    "A": "AKS Primality Test"
}
]
```</s>

[INST]
Raw Text:
```text
%s
```

Questions:[/INST]"""

def extract_questions(files: Tuple[str, str], iter = 0):
    if iter >= 3:
        print(f"Too many iterations for {files[0]}. Saving last attempt.")
        return False

    text = ''.join(open(files[0]).readlines())
    text.replace('', '')
    subst_prompt = prompt % (text,)

    data = {
        'prompt': subst_prompt,
        'max_tokens': 16384,
        'use_beam_search': False,
        'top_p': 0.95,
        'temperature': 0.05
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        questions = response.json()['text'][0][len(subst_prompt):]
        questions = '\n'.join(questions.split('\n')[1:-1])
        try:
            n_questions = len(json.loads(questions))
            print(f"Got {n_questions} from {files[0]}")

            with open(files[1], 'w') as f:
                f.write(questions)

            return True

        except Exception:
            print(f"JSON Parsing error in {files[0]}, extracting again")
            result = extract_questions(files, iter=iter+1)
            if not result:
                with open(files[1], 'w') as f:
                    f.write(questions)
                return True
            else:
                return True

    else:
        print("Error at endpoint")
        return False



# Define the raw and text directories
text_dir = 'text'
clean_dir = 'clean'
api_url = sys.argv[1]

filedata = []

# Create the text directory if it doesn't exist
if not os.path.exists(text_dir):
    os.makedirs(text_dir)

# Iterate through all files in the raw directory
for root, dirs, files in os.walk(text_dir):
    # Create the corresponding directory in the text directory
    clean_root = root.replace(text_dir, clean_dir)
    if not os.path.exists(clean_root):
        os.makedirs(clean_root)
    # Iterate through all PDF files in the current directory
    for file in files:
        if file.endswith('.txt'):
            # Construct the full file paths
            text_file = os.path.join(root, file)
            json_file = os.path.join(clean_root, file.replace('.txt', '.json'))
            # Extract text from the PDF if the text file doesn't exist
            if not os.path.exists(json_file):
                filedata.append((text_file, json_file))

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    results = executor.map(extract_questions, filedata)
