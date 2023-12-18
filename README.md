# Quiz Question Bank

A question bank dataset for quizzes scraped from SlideShare.

[Huggingface](https://huggingface.co/datasets/oppenbhaimer/QuizQuestionBank) | [Blog](https://oppenbhaimer.github.io/posts/quiz-question-bank)

## Recreating the dataset

You must have a scribd subscription for this (they offer a free 
two-month trial, so make the most of it).

1. Clone the repo

```
git clone https://github.com/oppenbhaimer/QuizQuestionBank
```

2. Create a folder called `scrape`, with the following files:
```
scrape 
`- authtoken.json
`- cookies.json 
`- usernames.json
```

Where:

* `authtoken.json` is the authentication token that SlideShare posts while 
  retrieving downloadable files 
* `cookies.json` is the list of cookies that are sent by your browser 
* `usernames.json` is a list of SlideShare usernames whose slides you want to scrape

3. Once done, run a mistral-instruct server API using vLLM on either your machine or an endpoint.

4. Run the pipeline
```
bash run.sh <api endpoint>
```

You are limited to 100 slideshare downloads in 24 hours. It is possible to rerun
this multiple times, and the downloader will continue to add to the files you 
already have. Files are cached at every stage, in the `raw`, `text`, `clean`
and `fixed` directories.

5. Once you're done, you should have all the questions present in `final.json`.
All cleanup after that is done by hand.
