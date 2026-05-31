from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        p = request.form['p']
        r = request.form['r']
        t = request.form['t']

        if (p.isdigit() and r.isdigit() and t.isdigit()):

            p = float(p)
            r = float(r)
            t = int(t)

            if (p > 0 and r > 0) and (t > 0 and t < 150):
                result = p * (1 + r / 100) ** t
                result = round(result, 2)
            else:
                result = 'Введите корректные числа!'

        else:
            result = 'Введите корректные числа!'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=False)