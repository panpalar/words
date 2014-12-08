import json
import datetime
from flask import Flask, Response
from flask import request
from flask.ext.restful import abort
import mongoengine
from Question import Question
from Tag import Tag
from Tags import Tags
from random import randint

app = Flask(__name__)


@app.route('/get/question/<string:Id>', methods=['GET'])
def get_init(Id):
    mongoengine.connect('Words', host='mongodb://localhost/Words')

    tagItem = Tag(id="54803d32d70d2e1a984830cf", name='Developer', date=datetime.datetime.now)
    tagItem2 = Tag(id="54803e2ed70d2e1e10a58135", name='Developer', date=datetime.datetime.now)

    questionItem = Question()
    questionItem.word = 'content'
    questionItem.answer = 'reply'
    questionItem.tags.append(tagItem)
    questionItem.tags.append(tagItem2)

    questionItem.save()
    js = Question.objects().to_json()
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/api/question/<string:tag>', methods=['GET'])
def get_question(tag):
    mongoengine.connect('Words', host='mongodb://localhost/Words')

    questionList = Question.objects(tags__name=tag.encode())[:10]
    number = randint(0, len(questionList)-1)
    question = questionList[number]

    option = Question.objects(id__ne=question.id)[:3]
    wrong = []
    tag = []

    for index in option:
        wrong.append(index['word'].encode('utf8'))

    for index in question.tags:
        tag.append(index['name'].encode('utf8'))

    js = {
        'word': question.word,
        'answer': question.answer,
        'tags': json.dumps(tag),
        'option': json.dumps(wrong)
    }
    result = json.dumps(js)

    resp = Response(result, status=200, mimetype='application/json')
    return resp


@app.route('/post/addquestion/', methods=['POST'])
def add_question():
    mongoengine.connect('Words', host='mongodb://localhost/Words')

    if (not request.data) or (not 'tags' in request.data) or (not 'word' in request.data) or (
            not 'answer' in request.data):
        abort(400)

    tagList = []
    data = json.loads(request.get_data())
    content = data['word'].encode('utf8')
    answer = data['answer'].encode('utf8')

    for index in data['tags']:
        #todo:gets_or_create
        getTag = Tags.objects(id=index['id'])
        if 0 == len(getTag):
            addedTag = Tags(name=index['name'].encode('utf8'), date=datetime.datetime.now).save()
            tagList.append(Tag(id=addedTag.id, name=addedTag.name, date=addedTag.date))
        else:
            tagList.append(Tag(id=getTag[0].id, name=getTag[0].name, date=getTag[0].date))

    questionItem = Question()
    questionItem.word = content
    questionItem.answer = answer
    questionItem.tags = tagList

    questionItem.save()
    js = Question.objects().to_json()
    resp = Response(js, status=200, mimetype='application/json', charset='utf-8')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
