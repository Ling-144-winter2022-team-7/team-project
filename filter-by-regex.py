# Initiated by Kelsey Kraus

# Contributors: Jack McGreevy 
#
# Description: <UPDATE ME!> This file currently contains the instructions for replicating the data cleaning method implemented by CTK 2016.

# NOTE: the suggested approaches below are NOT the only way to complete this task! It is merely given as a starting point. You can choose to do this in a different way if you want, but be sure to comment on your process along the way.

# !!! You may need to run in your Shell: pip install pandas !!!

import os
import pandas
import re
import csv

allTweets = []
with open('pro-who-tweets.csv') as file:
  allTweets = file.read()
  print(allTweets)


# -- Preprocessing: -- We don't care about the other data in our .csv. We want to only get the tweet text data in 'content' column.
# -- Suggested approach: -- create a list variable and save the 'content' column of the pro-who-tweets.csv file as your list. Print the length of the list. See here for more: https://www.geeksforgeeks.org/python-read-csv-columns-into-list/

filename = open('pro-who-tweets.csv', 'r')
file = csv.DictReader(filename)

content = []

for col in file:
  content.append(col['content'])


# === Part 1: Filtering ===

# -- First filter: -- Remove duplicates. 
# -- Suggested approach: -- using your list, convert the list into a dictionary, which will automatically remove duplicates. Then convert your dictionary back into a list. Print the length of the list. https://www.w3schools.com/python/python_howto_remove_duplicates.asp

content = list(dict.fromkeys(content))
print(len(content))



# -- Second filter: -- Remove tweets where the last non-whitespace character before the word 'who' is not a letter or a comma. See Lecture 3 slides for more explanation of this!
# -- Suggested approach: -- Use the list you created as a result of the previous filter. Save the 10 possible pronouns in a list. Create a loop to run through each entry in your list. Use a conditional statement to construct a regular expression match, and save the list elements matching your condition. Print the length of the list.

pronouns = ['it', 'you', 'he', 'his', 'she', 'her', 'we', 'us', 'they', 'them']
pattern = "(\w|,) who"
pattern2 = "(it|you|he|his|she|her|we|us|they|them|,) who"

content2 = []

for tweet in content:
  if re.search(pattern2, tweet):
    content2.append(tweet)


# -- Third filter: -- Remove the pattern 'of PRO who'
# -- Suggested approach: -- Create another loop, and another conditional statement using a regular expression from the list you got from the previous filter. This time, save only those that DO NOT match the conditional statement. Print the length of the list.

pattern3 = "of (it|you|he|his|she|her|we|us|they|them|,) who"

for tweet in content2:
  if re.search(pattern3, tweet):
    content2.remove(tweet)

print(len(content2))
# -- Fourth filter: -- Remove tweets where the pronoun 'it' preceeds the word 'who' by 2-4 words
# -- Suggested approach: -- Write a regular expression that picks out this pattern. Using the list you generated from the previous filter, use create a loop with a conditional statement that removes this pattern. Print the length of the list.

pattern4 = "( it.\w.who| it.\w.\w.who| it.\w.\w.\w.who)"

for tweet in content2:
  if re.search(pattern4, tweet):
    content2.remove(tweet)


# -- Fifth filter: -- Remove tweets where 'PRO who' is preceded by the verbs 'ask', 'tell', 'wonder', 'inform', and 'show'.
# -- Suggested approach: --  Save the verbs above into a list. Create a loop that iterates through your pronoun list from above, and removes examples that contain the pattern '[element-from-verb-list] [element-from-PRO-list]'. Print the length of the list.

verbs = ['ask', 'tell', 'wonder', 'inform', 'show']

pattern5 = ' ask.\w.+who| tell.\w.+who| wonder.\w.+who| inform.\w.+who| inform.\w.+who| show.\w.+who'



for tweet in content2:
  if re.search(pattern5, tweet):
    content2.remove(tweet)



# output your list as a .csv or .tsv file.



with open('new_file.csv', 'w') as f:
  write = csv.writer(f)
  write.writerow(['Tweets'])

  for tweet in content2:
    write.writerow([tweet])




# === Part 2: Uniqueness ===

# -- Instruction: -- You now need to find out whether the tweets you have left are "literary" or "non-literary", according to CTK's classification. I've written a bit of this for you. Modify the block of code below so that it runs with your variable names. You should replace 'tweetList' in the 'for' block with your variable name that holds the final filtered list of 'PRO who' tweets.

# Test variable: contains a short list of test utterances for the pattern "who <word1> <word2>"
tweetList = ['this is a quote: he who shall not be named', 'who among us really', 'jeff is wondering who sings', 'he who shall not be named again', 'but who among us is perfect']

# This evaluates each tweet in TweetList for whether it contains the specified regex search, and whether that regex pattern in a tweet matches exactly to any other tweet in the list. If it does, it is assigned a value True. If it doesn't, it's assigned a value False.
trueFalseList = []
for tweet in content2:
  whoPhrase = re.search("who \w+ \w+", tweet)
  if whoPhrase is None:
      trueFalseList.append(False)
  else:
      trueFalseList.append(any(whoPhrase.group(0) in t for t in content2))
print(trueFalseList)


# The following takes our two lists, tweetList and trueFalseList, and zips them together. It then creates a dataframe out of this list, that can then be converted to a .csv file

list1 = []
count=0

for x in content2:
  if count <150:
    list1.append(x)
    count+=1


annotatedTweetList = list(zip(content2, trueFalseList))
tweetDataframe = pandas.DataFrame(annotatedTweetList)
tweetDataframe.to_csv('literary-annotated-tweets.csv', header=["Tweet-text", "Uniqueness"], index=False)

with open('manual-tweets.csv', 'w') as z:
  write = csv.writer(z)
  write.writerow(['Tweets', 'RC-type', 'RC-head', 'Role'])

  for x in list1:
    write.writerow([x])


