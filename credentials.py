# coding: utf-8
import requests as r
from bs4 import BeautifulSoup
import hashlib
import re as regex
from time import sleep
import csv

user = "16978232"
# GET home page
home_url = "https://cuentas.napsis.cl/index.phtml"
response = r.get(home_url)

# POST credentials to select roles
auth_url = "https://cuentas.napsis.cl/session/roles"
session_id = response.cookies["PHPSESSID"]
cookies = {"PHPSESSID": session_id}
data = {"username":user, "password":"hola1234", "iframe":"0", "negarNapsis":""}
auth_response = r.post(auth_url, data = data , cookies = cookies, allow_redirects = False)

sleep(5)
# Parse response for form data
soup = BeautifulSoup(auth_response.content, "lxml")
pass_name = hashlib.md5("password".encode("utf-8")).hexdigest()
pass_value = soup.find("input", attrs={"type": "hidden", "name": pass_name}).get('value')

# Request for selecting the platform
second_login_url = "https://cuentas.napsis.cl/session/login"
form_data = {pass_name:pass_value, "institucion":0, "roles":0, "run_usuario":"16978232-6", "username":user, "iframe":"0", "negarNapsis":"", "sistema":"3", "primer_ingreso":""}
napsis = r.post(second_login_url, cookies = cookies, data = form_data, allow_redirects = False)

sleep(5)

# GET new authenticated session cookie 
cookie_url = napsis.headers["Location"]
homepage = r.get(cookie_url, allow_redirects = True)
homepage_url = homepage.url[::-1].split("/",1)[-1][::-1]
auth_string = regex.search('(?<=ID\=)[\w]+', homepage.history[0].headers["Set-Cookie"]).group(0)
auth_cookie = {"PHPSESSID": auth_string}
# GET platform homepage
sleep(5)
# report_url = "http://snd2.napsis.cl/colegiosanleonardo/informes/notas/curso/index.phtml"
report_url = homepage_url.replace("1", "2") + "/informes/notas/curso/index.phtml" 
# set type, grade and course





#settings_one = {"fAnoEscolar":"2015"}
settings_two = {"fAnoEscolar":"2015", "fColegio":"9970"}
#settings_three = {"fTipoEns":"110"}
#settings_four = {"fTipoEns":"110", "fGrado":"1105"}
settings_five = {"fTipoEns":"110", "fGrado":"1105", "fCurso":"1"}

# r.post(report_url, data=settings_one, cookies=auth_cookie)
# step 1: select course and year
r.post(report_url, data=settings_two, cookies=auth_cookie)
sleep(5)
# r.post(report_url, data=settings_three, cookies=auth_cookie)
# r.post(report_url, data=settings_four, cookies=auth_cookie)
# step 2: select stage, grade & course
r.post(report_url, data=settings_five, cookies=auth_cookie)
sleep(5)
# step 3: select asignatura
#r.post(report_url, data={"fAsignatura":"TODAS"}, cookies=auth_cookie)
# request report 
#sleep(5)
report_form_data = {"fNivel":"2", "fReligion":"3", "fAsignatura":"TODAS", "fperiodos":"TODAS", "fDecimales":"1", "fMostrarDetalleMadres":"1", "fMostrarRunAlumno":"1", "fAjustarnAsignatura":"1", "fMostrarProfAsig":"1"}
report_request = r.post(report_url, data=report_form_data, cookies=auth_cookie)

# with open("report.html", "w") as f:
#   f.write(report_request.text)

base_web = BeautifulSoup(report_request.content, "lxml")
# get all the years available
years = base_web.find("select", attrs={"id":"fAnoEscolar"}).findAll("option")
years = [x['value'] for x in years]
# get all the educational stages (middle, high) available
stages = base_web.find("select", attrs={"id":"fTipoEns"}).findAll("option")
stages = [x['value'] for x in stages if x['value'] is not '']

# get all the grades available
form_data=[]
for year in years:
    year_form_data = {"fAnoEscolar":year}
    r.post(report_url, data=year_form_data, cookies=auth_cookie)
    for stage in stages:
        stage_form_data = {"fTipoEns":stage}
        stage_request= r.post(report_url, data=stage_form_data, cookies=auth_cookie)
        stage_web = BeautifulSoup(stage_request.content, "lxml")
        grades = stage_web.find("select", attrs={"id":"fGrado"}).findAll("option")
        grades = [x['value'] for x in grades if x['value'] is not '']
        for grade in grades:
            stage_form_data['fGrado'] = grade
            grade_form_data = stage_form_data
            grade_request= r.post(report_url, data=grade_form_data, cookies=auth_cookie)
            grade_web = BeautifulSoup(grade_request.content, "lxml")
            courses = grade_web.find("select", attrs={"id":"fCurso"}).findAll("option")
            courses = [x['value'] for x in courses if x['value'] is not '']
            for course in courses:
                form_data.append({"grade":grade, "stage":stage, "year":year, "course":course})


# get the subjects and teachers

def get_report_data(response, year, form):
    web_page = BeautifulSoup(response.content, "lxml")
    table = web_page.find("table", attrs={"class":"cuadriculaNotas"})
    subjects = []
    col = 0
    try:
        ths = table.find("tr").findAll("th")
    except:
        print(form)
    for th in ths:
        try:
            l = int(th['colspan'])
            for c in range(col, col + l):
                subjects.append(th)
        except:
            l = 1
            subjects.append(th)
        col = col + l
    #for row in table.findAll('tr')[1:]:
    grades = []
    # get the grades
    for row in table.findAll('tr')[3:]:
        # get data for row
        td = row.findAll('td')
        name = td[2].string
        run = td[1].string
        for index, grade in enumerate(td[3:-1], start=3):
            #cell.text.replace('&nbsp;', '')
            try:
                db_row = {"name":name, "run":run, "subject":subjects[index].div.text, "grade":grade.text, "year":year}
                grades.append(db_row)
            except AttributeError:
                print("Subject number {} says {}".format(index, subjects[index]))
    return grades

# filter courses with no grades HARCODED TO-DO
form_data = [x for x in form_data if x['stage'] != '10' and x['year'] != '2016']
reports=[]
for form in form_data:
    #step 1: select year and school
    year_request_form_data = {"fAnoEscolar":form['year'], "fColegio":"9970"}
    r.post(report_url, data=year_request_form_data, cookies=auth_cookie)
    #step 2: select course
    request_form_data = {"fTipoEns":form['stage'], "fGrado":form['grade'], "fCurso":form['course']}
    r.post(report_url, data=request_form_data, cookies=auth_cookie)
    # step 3: select asignatura
    r.post(report_url, data={"fAsignatura":"TODAS"}, cookies=auth_cookie)
    # step 4: 
    report_response = r.post(report_url, data=report_form_data, cookies=auth_cookie)
    report_data = get_report_data(report_response, form['year'], form)
    reports.append(report_data)

reports = [y for x in reports for y in x]

with open('grades.csv', 'w') as csvfile:
    fieldnames=['grade', 'name', 'subject', 'year', 'run']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for report in reports:
        writer.writerow(report)



