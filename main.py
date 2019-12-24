from flask import Flask,request,render_template,redirect,flash,url_for
from flask_googlemaps import GoogleMaps
import stripe
app = Flask(__name__)
account_sid= 'ACe34a5e5038f0edf5fc936d013faceebc'
auth_token= '0b0caf5ae521d9d55dbd8d61e0ce3ee9'
stripe_keys = {
  'secret_key': 'sk_test_BjclD9riIOhVZG8kIZG7R7Sm00lGarjEXX',
  'publishable_key': 'pk_test_EBHYNqdWeJAZOpItEq8DUzjF00Qje3UdGg'
}
stripe.api_key = stripe_keys['secret_key']
from twilio.rest import Client
import nexmo
client = Client(account_sid,auth_token)
nexmoclient = nexmo.Client(key='d50de6d0', secret='7XRAZeDr8NBHzSNh')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/test')
def test():
    return render_template('base.html')
@app.route('/text/',methods=['GET','POST'])
def text():
    if request.method == "POST":
        number ='+12014646836'
        message = request.form.get('message')
        receiver = "+"+request.form.get('receiver')
        try:
            text= client.messages.create(to=receiver,from_=number,body=message)
            flash("Success Message sent!",'success')
            return redirect(url_for('home'))
        except BaseException as e:
            flash("Error sending the message "+ str(e),'danger')
            return redirect(url_for('home'))
    return render_template('text.html')
@app.route('/textunverified/')
def textunverified():
    if request.method == "POST":
        number ='17053160814'
        message = request.form.get('message')
        receiver = request.form.get('receiver')
        
    return render_template('text.html')
        
        
@app.route('/getinfo/',methods=['POST','GET'])
def info():
    if request.method == "POST":
        everything =[]
        phone_number = request.form.get('phone-number')
        everything.append(request.form.get('country-code'))
        everything.append(request.form.get('carrier'))
        everything.append(request.form.get('name'))
        types = ['country_code','carrier','name']
        full_data = []
        for i in range(len(everything)):
            if everything[i] != None:
                carrier = client.lookups.phone_numbers(phone_number).fetch(type=types[i])
                if types[i] == "country_code":
                    full_data.append(carrier.country_code)
                elif types[i] == "carrier":
                    full_data.append(carrier.carrier)
                elif types[i] == "name":
                    full_data.append(carrier.caller_name)
            else:
                full_data.append("not-requested")
                
        
        return render_template('response.html',full_list=full_data)
    return render_template('getinfo.html')
@app.route('/shop')
def shop():
    return render_template('shop.html',key=stripe_keys['publishable_key'])
@app.route('/pay',methods=['POST'])
def index():
    try:
        amount = 99999999  # amount in cents
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        flash('Payment of ' + str(amount) + ' Success','success')
        return redirect(url_for('home'))
    except BaseException as e:
        flash('Failed payment ' + str(e))
        return redirect(url_for('home'))

@app.route('/shoppingtest')
def shoppingtest():
    return render_template('new.html')
@app.route('/googlemaps',methods=['POST','GET'])
def maps():
    if request.method == "POST":
        return request.form
    return render_template('longlat.html')