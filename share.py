from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('share.html')

@app.route('/share')
def share():
    url = request.args.get('url')
    title = request.args.get('title')
    facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u={url}"
    return redirect(facebook_share_url)

if __name__ == '__main__':
    app.run(debug=True)
