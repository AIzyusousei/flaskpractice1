from flask import render_template, request, redirect, url_for
from plana import app
from plana import db
from plana.models import Employee
from random import randint


@app.route('/')
def index():
    mydict = {
              'insert_something1' : 'views.pyのinsert_something1部分です．',
              'insert_something2' : 'views.pyのinsert_something2部分です．',
              'test_titles' : ['title1', 'title2', 'title3']
    }
    return render_template('htmls/index.html', my_dict = mydict)#htmlでmy_dictがmy_dictという引き数として使える

@app.route('/test')
def other1():
    return render_template('htmls/index2.html')

@app.route('/sampleform', methods = ['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('htmls/sampleform.html')
    if request.method == 'POST':
        # ジャンケンの手を文字列の数字0~2で受け取る
        hands = {
            '0': 'グー',
            '1': 'チョキ',
            '2': 'パー',
        }
        janken_mapping = {
            'draw': '引き分け',
            'win': '勝ち',
            'lose': '負け',
        }

        player_hand_ja = hands[request.form['janken']]  # 日本語表示用
        player_hand = int(request.form['janken'])  # str型→数値に変換必要
        enemy_hand = randint(0, 2)  # 相手は0~2の乱数
        enemy_hand_ja = hands[str(enemy_hand)]  # 日本語表示用
        if player_hand == enemy_hand:
            judgement = 'draw'
        elif (player_hand == 0 and enemy_hand == 1) or (player_hand == 1 and enemy_hand == 2) or (player_hand == 2 and enemy_hand == 0):
            judgement = 'win'
        else:
            judgement = 'lose'
        print(f'じゃんけん開始: enemy_hand: {enemy_hand}, player_hand: {player_hand}, judgement: {judgement}')
        
        result = {
            'enemy_hand_ja': enemy_hand_ja,
            'player_hand_ja': player_hand_ja,
            'judgement': janken_mapping[judgement],
        }
        return render_template('htmls/janken_result.html', result=result)






@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('htmls/add_employee.html')
    if request.method == 'POST':
        #request.formは，str型で出力される．type=によって型を変換する必要がある．
        form_name = request.form.get('name')
        form_mail = request.form.get('mail')
        form_is_remote = request.form.get('is_remote', default=False, type=bool)  #defaultは，noneのとき（この場合はチェックボックスが未入力のときの値を指定する）
        form_department = request.form.get('department')
        form_year = request.form.get('year', type=int)
        employee = Employee(
            name = form_name,
            mail = form_mail,
            is_remote = form_is_remote,
            department = form_department,
            year = form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))
    
@app.route('/employees')
def employee_list():
    employees = Employee.query.all()                                          #.all()などは，各データがリストで帰ってくる．
    return render_template('/htmls/employee_list.html', employees=employees)

@app.route('/employees/<int:id>')
def employee_detail(id):
    employee = Employee.query.get(id)
    return render_template('/htmls/employee_detail.html', employee=employee)

@app.route('/employees/<int:id>/edit', methods = ['GET'])
def employee_edit(id):
    employee = Employee.query.get(id)
    return render_template('htmls/employee_edit.html', employee=employee)

@app.route('/employee/<int:id>/update', methods = ['POST'])
def employee_update(id):
    employee = Employee.query.get(id)  # 更新するデータをDBから取得
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)  #mergeは，インスタンスの持っているidがあれば，それについて変更を行い，なければinsert1する
    db.session.commit()
    return redirect(url_for('employee_list'))  #redirectだと，もう一回データベースとやり取りを行う．

@app.route('/employees/<int:id>/delete', methods=['POST'])  
def employee_delete(id):  
    employee = Employee.query.get(id)   
    db.session.delete(employee)  
    db.session.commit()  
    return redirect(url_for('employee_list'))

@app.route('/aa')
def aaa():
    print("テスト")