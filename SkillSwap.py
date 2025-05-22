from flask import Flask, render_template, request, redirect, session
import json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import webbrowser
#sigma
app = Flask(__name__)
app.secret_key = 'nekaj-zelo-tajnega'
YOUTUBE_API_KLJUC = 'AIzaSyAwAnuV__LH3lneUlREB-MdlcCOfw9CSNY'



@app.route('/')
def index():
    uporabnik = None
    if 'uporabnik' in session:
        ime = session['uporabnik']
        try:
            with open('users.json', 'r') as seznam:
                uporabniki = json.load(seznam)
            for u in uporabniki:
                if u['ime'] == ime:
                    uporabnik = u
                    break
        except FileNotFoundError:
            pass
    return render_template('index.html', uporabnik=uporabnik)

def nalozi_skills():
    try:
        with open('skills.json', 'r') as seznam:
            return json.load(seznam)
    except FileNotFoundError:
        return []

def shrani_skills(skills):
    with open('skills.json', 'w') as f:
        json.dump(skills, f, indent=4)

@app.route('/register', methods=['GET', 'POST'])
def registracija():
    skills = nalozi_skills()

    if request.method == 'POST':
        znam = request.form['znam_po_meri'] if request.form['znam_po_meri'] else request.form['znam_izbira']
        zelim_se_nauciti = request.form['zelim_po_meri'] if request.form['zelim_po_meri'] else request.form['zelim_izbira']

        
        for nova_vescina in [znam, zelim_se_nauciti]:
            if nova_vescina and nova_vescina not in skills:
                skills.append(nova_vescina)
        shrani_skills(skills)

        uporabnik = {
            "ime": request.form['name'],
            "password": generate_password_hash(request.form['geslo']),
            "znam": znam,
            "zelim_se_nauciti": zelim_se_nauciti,
            "discord": request.form['discord'],
            

        }

        try:
            with open('users.json', 'r') as f:
                uporabniki = json.load(f)
        except FileNotFoundError:
            uporabniki = []

        uporabniki.append(uporabnik)

        with open('users.json', 'w') as f:
            json.dump(uporabniki, f, indent=4)

        return redirect('/')
    return render_template('register.html', skills=skills)

@app.route('/search', methods=['GET', 'POST'])
def iskanje():
    skills = nalozi_skills()

    if request.method == 'POST':
        skill = request.form['skill']

        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        
        matching_users = [user for user in users if user.get('znam') == skill]

        return render_template('search.html', users=matching_users, skills=skills)

    return render_template('search.html', users=None, skills=skills)

@app.route('/login', methods=['GET', 'POST'])
def prijava():

    if request.method == 'POST':
        vneseno_ime = request.form['ime']
        vneseno_geslo = request.form['geslo']

        try:
            with open('users.json', 'r') as f:
                uporabniki = json.load(f)
        except FileNotFoundError:
            uporabniki = []

        for u in uporabniki:
            if u['ime'] == vneseno_ime and check_password_hash(u['password'], vneseno_geslo):

                session['uporabnik'] = vneseno_ime
                return redirect('/profil/' + vneseno_ime)

        return "Uporabnik ni najden ali napačni podatki", 401


    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('uporabnik', None)
    return redirect('/')

def shorten_url(long_url):
    api_url = 'http://tinyurl.com/api-create.php'
    params = {'url': long_url}
    r = requests.get(api_url, params=params)
    if r.status_code == 200:
        return r.text  
    else:
        return long_url  

@app.route('/profil/<ime>', methods=['GET', 'POST'])
def profil(ime):

    try:
        with open('users.json', 'r') as f:
            uporabniki = json.load(f)
    except FileNotFoundError:
        uporabniki = []

    for uporabnik in uporabniki:
        if uporabnik['ime'] == ime:
            if request.method == 'POST':
                prilepljen_url = request.form.get('slika_url')
                if prilepljen_url:
                    krajši_url = shorten_url(prilepljen_url)
                    uporabnik['slika_url'] = krajši_url
                
                nov_skill = request.form.get('nov_skill')
                if nov_skill:
                    if 'znam' in uporabnik:
                        if isinstance(uporabnik['znam'], list):
                            if nov_skill not in uporabnik['znam']:
                                uporabnik['znam'].append(nov_skill)
                        else:
                            if uporabnik['znam'] != nov_skill:
                                uporabnik['znam'] = [uporabnik['znam'], nov_skill]
                    else:
                        uporabnik['znam'] = [nov_skill]
                
                nova_zelja = request.form.get('nova_zelja')
                if nova_zelja:
                    if 'zelim_se_nauciti' in uporabnik:
                        if isinstance(uporabnik['zelim_se_nauciti'], list):
                            if nova_zelja not in uporabnik['zelim_se_nauciti']:
                                uporabnik['zelim_se_nauciti'].append(nova_zelja)
                        else:
                            if uporabnik['zelim_se_nauciti'] != nova_zelja:
                                uporabnik['zelim_se_nauciti'] = [uporabnik['zelim_se_nauciti'], nova_zelja]
                    else:
                        uporabnik['zelim_se_nauciti'] = [nova_zelja]
                
                with open('users.json', 'w') as profil:
                    json.dump(uporabniki, profil, indent=4)
                        

                
                    
            tema = uporabnik.get('zelim_se_nauciti', '')
            videi = pridobi_youtube_videe(tema, YOUTUBE_API_KLJUC)
            return render_template('profile.html', uporabnik=uporabnik, videi=videi)
            

    return "Uporabnik ni najden", 404


def pridobi_youtube_videe(tema, api_key):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=3&q=how+to+learn+{tema}&key={api_key}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    return [
        {
            "naslov": v['snippet']['title'],
            "video_url": f"https://www.youtube.com/watch?v={v['id']['videoId']}"

        }
        for v in data['items']
    ]


def upload_image(image_url):
    url = "https://api.imgur.com/3/image"
    headers = {
        "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
    }

    slika = {
        'image': image_url,
        'type': 'url'
    }
    
    response = requests.post(url, headers=headers, data=slika)
    
    if response.status_code == 200:
        data = response.json()['data']
        return {
            'image_url': data['link'],
            'delete_hash': data['deletehash']
        }
    else:
        return {'error': response.text}


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(host = '0.0.0.0', port=5000)
