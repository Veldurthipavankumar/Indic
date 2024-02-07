from flask import Flask, render_template, session, url_for, session, request, jsonify, make_response
import json

app = Flask(__name__)

app.secret_key = b'bharat mata ki jay'

data_stats = {}

for stats_t in ['base_stats','clean_stats','merge_stats','languages','references']:
    with open('./stats/' + stats_t + '.json') as f:
        data_stats[stats_t] = json.load(f)

print(data_stats)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    return render_template('stats.html',stats=data_stats,enumerate_stats_langs=[x for x in enumerate(data_stats['languages'])])
    
def processPair(pair):
    pair_stats = {}
    pair_stats['code'] = pair
    pair_stats['clean'] = data_stats['clean_stats'][pair]
    pair_stats['base'] = data_stats['base_stats'][pair]
    
    clean_total = 0
    base_total = 0

    for key in pair_stats['clean'].keys():
        clean_total += pair_stats['clean'][key]

    for key in pair_stats['base'].keys():
        clean_total += pair_stats['base'][key]

    pair_stats['clean_total'] = clean_total
    pair_stats['base_total'] = base_total

    return pair_stats


@app.route('/catalogue',methods=['GET', 'POST'])
def catalogue():
    if request.method == 'POST':
        lang1 = str(request.form['language1'])
        lang2 = str(request.form['language2'])
        
        pair = ""

        if lang1 > lang2:
            pair = lang2 + '-' + lang1
        else:
            pair = lang1 + '-' + lang2

        pairStats = processPair(pair)    
        return render_template('catalogue.html',stats=data_stats,enumerate_stats_langs=[x for x in enumerate(data_stats['languages'])],lang1=lang1,lang2=lang2,show=True,pairStats = pairStats)
    else:
        return render_template('catalogue.html',stats=data_stats,enumerate_stats_langs=[x for x in enumerate(data_stats['languages'])],lang1='hi',lang2='mr',show=False)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/references')
def references():
    return render_template('references.html',references=data_stats['references'],source=None)

@app.route('/references/<source>')
def reference(source=None):
    print(source)
    return render_template('references.html',references=data_stats['references'],source=source)


if __name__ == '__main__':
    app.run()