from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

# flask is the name of the 'package' and it has a class called Flask inside of it.
#html 파일을 메인으로(유저에게) 어떻게 보내줄까?
#render_template는 html을? 로? 파이썬 파일로 보내준다.
#render_templates 함수
# 예를 들어 주소에 react를 넣었는데 이것만 넣어선 검색을 쓸 수 없잖아. word=react 이 단어를 request로 각각 쭉 뽑아올거야. 쭉 추출한 직업정보를 가져오기 위해서 우리는 requests를 추출할거야. 우리가 사실 홈페이지에서 보는 것들은 전부 requests지(계속계속 바뀌고 업데이트되)

app = Flask("SuperScrapper whre is it????")

db = {}
# db는 route 밖에 있으니 얼마나 route가 실행되든 상관없다. 만약 route 안에 있으면 report()가 실행될때마다 초기화됨.

@app.route("/") 
def home():
  return render_template("potato.html")


@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else :
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy = word, resultsNumber=len(jobs),
  jobs = jobs
  )
# @는 데코레이터를 뜻함. 이건 바로 아래에 있는 함수를 찾아서 그 함수를 decorate(꾸미다) 해주는 역할이지.
# 만약에 @ 아래에 함수말고 다른게 있으면 error가 날꺼임. 왜냐면 @는 바로 아래 함수만 받아들이기 때문이지.

  
# @app.route("/<username>") # 이런식으로 다른 url을 제어
# def potato(username) :
#   return "<h1>This is Job Serach</h1>"
  
@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    # word가 url에 있는지 확인한다.
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs :
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except :
    return redirect("/")
  

app.run(host = '0.0.0.0')