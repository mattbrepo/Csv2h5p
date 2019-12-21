#!/usr/bin/env python
import sys
import csv
import zipfile
import os
import shutil

# ==================================== DIALOG
dialog_template = '''{
   "description":"Learn Legal English Victims",
   "dialogs":[%blocks%
   ],
   "behaviour":{
      "enableRetry":true,
      "disableBackwardsNavigation":false,
      "scaleTextNotCard":false,
      "randomCards":false
   },
   "answer":"Turn",
   "next":"Next",
   "prev":"Previous",
   "retry":"Retry",
   "progressText":"Card @card of @total",
   "cardFrontLabel":"Card front",
   "cardBackLabel":"Card back",
   "tipButtonLabel":"Show tip",
   "audioNotSupported":"Your browser does not support this audio",
   "title":""
}
'''

dialog_block_template = '''
      {
         "tips":{

         },
         "text":"%text%",
         "answer":"%answer%",
         "imageAltText":"-",
         "audio":[
            {
               "path":"%audio%",
               "mime":"audio\/mp3",
               "copyright":{
                  "license":"U"
               }
            }
         ]
      }'''
# MTB [31/08/2019]: Lou doesn't want images anymore
#         ],
#         "image":{
#            "path":"images\/%image%",
#            "mime":"image\/jpeg",
#            "width":500,
#            "height":500
#         }
#      }'''

# ==================================== CARD
card_template = '''{
   "cards":[%blocks%
   ],
   "progressText":"Card @card of @total",
   "next":"Next",
   "previous":"Previous",
   "checkAnswerText":"Check",
   "showSolutionsRequiresInput":true,
   "defaultAnswerText":"Your answer",
   "correctAnswerText":"Correct",
   "incorrectAnswerText":"Incorrect",
   "showSolutionText":"Correct answer",
   "results":"Results",
   "ofCorrect":"@score of @total correct",
   "showResults":"Show results",
   "answerShortText":"A:",
   "retry":"Retry",
   "caseSensitive":false,
   "description":"Answer the questions with the correct Legal English vocabulary."
}'''

card_block_template = '''
      {
         "text":"%text%",
         "answer":"%answer%",
         "tip":"",
         "image":{
            "path":"images\/%image%",
            "mime":"image\/jpeg",
            "copyright":{
               "license":"CC BY"
            },
            "width":500,
            "height":500
         }
      }'''

# ==================================== SPEAK
speak_template = '''{
   "introduction":{
      "showIntroPage":true,
      "introductionText":"Instructions: Practise your pronunciation by reading the phrase. Speak slowly and clearly and enunciate each word."
   },
   "questions":[%blocks%
   ],
   "overallFeedback":[
      {
         "from":0,
         "to":25,
         "feedback":"Try speaking slower and clearer."
      },
      {
         "from":26,
         "to":50,
         "feedback":"Keep practising!"
      },
      {
         "from":51,
         "to":75,
         "feedback":"Great pronunciation!"
      },
      {
         "from":76,
         "to":100,
         "feedback":"Perfect pronunciation!"
      }
   ],
   "l10n":{
      "introductionButtonLabel":"Start Course!",
      "solutionScreenResultsLabel":"Your results:",
      "showSolutionsButtonLabel":"Show solution",
      "retryButtonLabel":"Retry",
      "nextQuestionAriaLabel":"Next question",
      "previousQuestionAriaLabel":"Previous question",
      "navigationBarTitle":"Slide :num",
      "answeredSlideAriaLabel":"Answered",
      "activeSlideAriaLabel":"Currently active"
   }
}
'''

speak_block_template = '''
      {
         "params":{
            "incorrectAnswerText":"Your pronunciation needs improving.",
            "correctAnswerText":"%correctAnswerText%",
            "inputLanguage":"en-GB",
            "l10n":{
               "retryLabel":"Retry",
               "showSolutionLabel":"Show solution",
               "speakLabel":"Push to speak",
               "listeningLabel":"Listening...",
               "correctAnswersText":"The correct answer(s):",
               "userAnswersText":"Your answer(s) was interpreted as:",
               "noSound":"I could not hear you, make sure your microphone is enabled",
               "unsupportedBrowserHeader":"It looks like your browser does not support speech recognition",
               "unsupportedBrowserDetails":"Please try again in a browser like Chrome"
            },
            "question":"%correctAnswerText%",
            "acceptedAnswers":[
               "%acceptedAnswers%"
            ]
         },
         "library":"H5P.SpeakTheWords 1.3",
         "metadata":{
            "contentType":"Speak the Words",
            "license":"U",
            "title":"%title%",
            "authors":[

            ],
            "changes":[

            ],
            "extraTitle":"%title%"
         }
      }'''

# ==================================== DRAG&DROP
dragdrop_template = '''{
   "introPage":{
      "showIntroPage":false,
      "startButtonText":"Start Quiz",
      "introduction":""
   },
   "progressType":"dots",
   "passPercentage":50,
   "questions":[%blocks%
   ],
   "disableBackwardsNavigation":false,
   "randomQuestions":true,
   "endGame":{
      "showResultPage":true,
      "showSolutionButton":true,
      "showRetryButton":true,
      "noResultMessage":"Finished",
      "message":"Your result:",
      "overallFeedback":[
         {
            "from":0,
            "to":100
         }
      ],
      "solutionButtonText":"Show solution",
      "retryButtonText":"Retry",
      "finishButtonText":"Finish",
      "showAnimations":false,
      "skippable":false,
      "skipButtonText":"Skip video"
   },
   "override":{
      "checkButton":true
   },
   "texts":{
      "prevButton":"Previous question",
      "nextButton":"Next question",
      "finishButton":"Finish",
      "textualProgress":"Question: @current of @total questions",
      "jumpToQuestion":"Question %d of %total",
      "questionLabel":"Question",
      "readSpeakerProgress":"Question @current of @total",
      "unansweredText":"Unanswered",
      "answeredText":"Answered",
      "currentQuestionText":"Current question"
   }
}
'''

dragdrop_block_template = '''
      {
         "params":{
            "taskDescription":"<p>Drag the words into the correct boxes<\/p>",
            "overallFeedback":[
               {
                  "from":0,
                  "to":25,
                  "feedback":"%feedback0-25%"
               },
               {
                  "from":26,
                  "to":50,
                  "feedback":"%feedback26-50%"
               },
               {
                  "from":51,
                  "to":75,
                  "feedback":"%feedback51-75%"
               },
               {
                  "from":76,
                  "to":100,
                  "feedback":"%feedback76-100%"
               }
            ],
            "checkAnswer":"Check",
            "tryAgain":"Retry",
            "showSolution":"Show solution",
            "dropZoneIndex":"Drop Zone @index.",
            "empty":"Drop Zone @index is empty.",
            "contains":"Drop Zone @index contains draggable @draggable.",
            "draggableIndex":"Draggable @text. @index of @count draggables.",
            "tipLabel":"Show tip",
            "correctText":"Correct!",
            "incorrectText":"Incorrect!",
            "resetDropTitle":"Reset drop",
            "resetDropDescription":"Are you sure you want to reset this drop zone?",
            "grabbed":"Draggable is grabbed.",
            "cancelledDragging":"Cancelled dragging.",
            "correctAnswer":"Correct answer:",
            "feedbackHeader":"Feedback",
            "behaviour":{
               "enableRetry":true,
               "enableSolutionsButton":true,
               "enableCheckButton":true,
               "instantFeedback":false
            },
            "scoreBarLabel":"You got :num out of :total points",
            "textField":"%text%"
         },
         "library":"H5P.DragText 1.8",
         "metadata":{
            "contentType":"Drag Text",
            "license":"U",
            "title":"%title%"
         }
      }'''

# ==================================== GAP&FILL
gapfill_template = '''{
   "introPage":{
      "showIntroPage":false,
      "startButtonText":"Start Quiz",
      "introduction":""
   },
   "progressType":"dots",
   "passPercentage":50,
   "questions":[%blocks%
   ],
   "disableBackwardsNavigation":false,
   "randomQuestions":true,
   "endGame":{
      "showResultPage":true,
      "showSolutionButton":true,
      "showRetryButton":true,
      "noResultMessage":"Finished",
      "message":"Your result:",
      "overallFeedback":[
         {
            "from":0,
            "to":100
         }
      ],
      "solutionButtonText":"Show solution",
      "retryButtonText":"Retry",
      "finishButtonText":"Finish",
      "showAnimations":false,
      "skippable":false,
      "skipButtonText":"Skip video"
   },
   "override":{
      "checkButton":true
   },
   "texts":{
      "prevButton":"Previous question",
      "nextButton":"Next question",
      "finishButton":"Finish",
      "textualProgress":"Question: @current of @total questions",
      "jumpToQuestion":"Question %d of %total",
      "questionLabel":"Question",
      "readSpeakerProgress":"Question @current of @total",
      "unansweredText":"Unanswered",
      "answeredText":"Answered",
      "currentQuestionText":"Current question"
   }
}
'''

gapfill_block_template = '''
      {
         "params":{
            "text":"<p>%task%<\/p>",
            "overallFeedback":[
               {
                  "from":0,
                  "to":25,
                  "feedback":"%feedback0-25%"
               },
               {
                  "from":26,
                  "to":50,
                  "feedback":"%feedback26-50%"
               },
               {
                  "from":51,
                  "to":75,
                  "feedback":"%feedback51-75%"
               },
               {
                  "from":76,
                  "to":100,
                  "feedback":"%feedback76-100%"
               }
            ],
            "showSolutions":"Show solution",
            "tryAgain":"Retry",
            "checkAnswer":"Check",
            "notFilledOut":"Please fill in all blanks to view solution",
            "answerIsCorrect":"&#039;:ans&#039; is correct",
            "answerIsWrong":"&#039;:ans&#039; is wrong",
            "answeredCorrectly":"Answered correctly",
            "answeredIncorrectly":"Answered incorrectly",
            "solutionLabel":"Correct answer:",
            "inputLabel":"Blank input @num of @total",
            "inputHasTipLabel":"Tip available",
            "tipLabel":"Tip",
            "behaviour":{
               "enableRetry":true,
               "enableSolutionsButton":true,
               "enableCheckButton":true,
               "autoCheck":false,
               "caseSensitive":false,
               "showSolutionsRequiresInput":false,
               "separateLines":false,
               "confirmCheckDialog":false,
               "confirmRetryDialog":false,
               "acceptSpellingErrors":true
            },
            "scoreBarLabel":"You got :num out of :total points",
            "confirmCheck":{
               "header":"Finish ?",
               "body":"Are you sure you wish to finish ?",
               "cancelLabel":"Cancel",
               "confirmLabel":"Finish"
            },
            "confirmRetry":{
               "header":"Retry ?",
               "body":"Are you sure you wish to retry ?",
               "cancelLabel":"Cancel",
               "confirmLabel":"Confirm"
            },
            "questions":[
               "<p>%text%<\/p>"
            ],
            "media":{
               "disableImageZooming":false
            }
         },
         "library":"H5P.Blanks 1.12",
         "metadata":{
            "contentType":"Fill in the Blanks",
            "license":"U",
            "title":"%title%"
         }
      }'''

# ==================================== CODE
def convert(tsv, outfile, out_type):
  reader = csv.reader(tsv, dialect="excel-tab")
  next(reader, None)  # skip the headers
  
  blocks = ''
  for line in reader:
    line0 = line[0]
    line1 = line[1]
    line2 =  line[2]
    
    if out_type == 1:
      audio = line[3].replace('/', '\\/')
      blocks += dialog_block_template.replace('%text%', line0).replace('%image%', line2).replace('%answer%', line1).replace('%audio%', audio) + ','
    elif out_type == 2:
      blocks += card_block_template.replace('%text%', line0).replace('%image%', line2).replace('%answer%', line1) + ','
    elif out_type == 3:
      blocks += speak_block_template.replace('%title%', line0).replace('%correctAnswerText%', line1).replace('%acceptedAnswers%', line2) + ','
    elif out_type == 4:
      line1 = line1.replace("'", "&#039;")
      line3 = line[3]
      line4 = line[4]
      line5 = line[5]
      blocks += dragdrop_block_template.replace('%title%', line0).replace('%text%', line1).replace('%feedback0-25%', line2).replace('%feedback26-50%', line3).replace('%feedback51-75%', line4).replace('%feedback76-100%', line5) + ','
    elif out_type == 5:
      line1 = line1.replace("'", "&#039;")
      line2 = line2.replace("'", "&#039;")
      line3 = line[3]
      line4 = line[4]
      line5 = line[5]
      line6 = line[6]
      blocks += gapfill_block_template.replace('%title%', line0).replace('%task%', line1).replace('%text%', line2).replace('%feedback0-25%', line3).replace('%feedback26-50%', line4).replace('%feedback51-75%', line5).replace('%feedback76-100%', line6) + ','

  blocks = blocks[:-1] #remove last comma
  
  if out_type == 1:
    my_json = dialog_template.replace('%blocks%', blocks)
  elif out_type == 2:
    my_json = card_template.replace('%blocks%', blocks)
  elif out_type == 3:
    my_json = speak_template.replace('%blocks%', blocks)
  elif out_type == 4:
    my_json = dragdrop_template.replace('%blocks%', blocks)
  elif out_type == 5:
    my_json = gapfill_template.replace('%blocks%', blocks)

  print(my_json, file=outfile)

def zipdir(path, ziph):
  # ziph is zipfile handle
  for root, dirs, files in os.walk(path):
    for file in files:
      ziph.write(os.path.join(root, file))

if __name__ == '__main__':
  # ask if it's for dialog or flashcard
  out_type = 1
  while True:
    res = input("1: dialog, 2: flashcard, 3: speak, 4: drag&drop, 5: gap&fill  ====> ")
    if (res == '1' or res == '2' or res == '3' or res == '4' or res == '5'):
      out_type = int(res)
      break;

  res = input("---a: ")

  # remove previous h5p files
  if out_type == 1:
    if os.path.isfile('dialogs.h5p'):
      os.remove('dialogs.h5p')
  elif out_type == 2:
    if os.path.isfile('flashcards.h5p'):
      os.remove('flashcards.h5p')
  elif out_type == 3:
    if os.path.isfile('speak.h5p'):
      os.remove('speak.h5p')
  elif out_type == 4:
    if os.path.isfile('dragdrop.h5p'):
      os.remove('dragdrop.h5p')
  elif out_type == 5:
    if os.path.isfile('gapfill.h5p'):
      os.remove('gapfill.h5p')

  res = input("---b: ")

  # remove previous temp.zip file
  if os.path.isfile('./temp.zip'):
    os.remove('./temp.zip')

  res = input("---c: ")

  # from input.txv to content.json
  if os.path.isfile('./data/content.json'):
    os.remove('./data/content.json')

  res = input("---d: ")
  
  convert(open('./data/input.tsv'), open('./data/content.json','w'), out_type)
  res = input("---1: ")

  # move in the dialog/flashcard folder
  if out_type == 1:
    os.chdir('./dir_dialogs.h5p')
  elif out_type == 2:
    os.chdir('./dir_flashcards.h5p')
  elif out_type == 3:
    os.chdir('./dir_speak.h5p')
  elif out_type == 4:
    os.chdir('./dir_dragdrop.h5p')
  elif out_type == 5:
    os.chdir('./dir_gapfill.h5p')

  # remove previous content
  if out_type == 1 or out_type == 2:
    for f in os.listdir('./content/images'):
      os.remove(os.path.join('./content/images', f))
  
  res = input("---2: ")
  
  if os.path.isfile('./content/content.json'):
    os.remove('./content/content.json')

  # copy new content
  #filelist = [ f for f in os.listdir('../data') if (f.endswith(".jpg") or f.endswith(".png")) ]
  #for f in filelist:
  #  os.remove(os.path.join(mydir, f))
  if out_type == 1 or out_type == 2:
    for f in os.listdir('../data'):
      if f.lower().endswith('.png') or f.lower().endswith('.jpg'):
        shutil.copy(os.path.join('../data', f), './content/images')
  res = input("---3: ")
  shutil.copy('../data/content.json', './content/')
  
  # zip
  zipf = zipfile.ZipFile('../temp.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir('.', zipf)
  zipf.close()
  res = input("---out_type: " + str(out_type))
  
  # rename zip
  os.chdir('..')
  if out_type == 1:
    os.rename('temp.zip', 'dialogs.h5p')
  elif out_type == 2:
    os.rename('temp.zip', 'flashcards.h5p')
  elif out_type == 3:
    os.rename('temp.zip', 'speak.h5p')
  elif out_type == 4:
    os.rename('temp.zip', 'dragdrop.h5p')
  elif out_type == 5:
    os.rename('temp.zip', 'gapfill.h5p')

  res = input("---5: ")
