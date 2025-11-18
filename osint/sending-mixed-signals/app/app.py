from flask import Flask, render_template, request

app = Flask(__name__)

part_1 = 'enRR8UVVywXYbFkqU#QDPRkO'
part_2 = 'moti@telemessage.com'
part_3 = 'Release_5.4.11.20'

@app.route('/', methods=['GET', 'POST'])
def challenge():
    results = None
    if request.method == 'POST':
        correct_answers = {'part1': part_1, 'part2': part_2, 'part3': part_3}
        results = ['incorrect', 'incorrect', 'incorrect']
        for i, part in enumerate(['part1', 'part2', 'part3']):
            user_input = request.form.get(part, '').strip()
            if user_input == correct_answers[part]:
                results[i] = 'correct'

        if(results[0] == 'correct' and results[1] == 'correct' and results[2] == 'correct'):
            results.append(open('flag.txt').read())

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=False)
