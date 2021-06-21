from flask import Flask, render_template, request, session, redirect, url_for, flash,  g
import UserModel
import ProductModel
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
username = ''
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.before_request   # This take place before app runs
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']
        # user = UserModel.VeryfyEmail(g.username)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', "POST"])
def home():
    if 'username' in session:
        g.user = session['username']
        user = UserModel.VeryfyEmail(g.user)
        product = ProductModel.AllItem()
        return render_template('user.html', user=user, msg=user[5], len = len(product), products = product)
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        g.user = session['username']
        user = UserModel.VeryfyEmail(g.user)
        product = ProductModel.AllItem()
        return render_template('user.html', user=user, msg=user[5], len = len(product), products = product)

    if request.method == 'POST':
        session.pop('username', None)
        email = request.form['email']
        password = request.form['pass']
        pwd = UserModel.VerifyUser(email)
        if pwd is not None:
            if pwd[3] == password:
                session['username'] = request.form['email']
                return redirect(url_for('home'))  # This will redirect to the home function
            else:
                return render_template('login.html', msg='Incorrect Password for the account {mail}'.format(mail=email))
        else:
            return render_template('login.html', msg='User {mail} does not exist, Please register the user'.format(mail=email))
    return render_template('login.html')


@app.route('/signup', methods=['GET', "POST"])
def signup():
    if 'username' not in session:
        # g.user = session['username']
        # user = UserModel.VerifyUser(g.user)
        # return render_template('user.html', user=user, msg=user[5])

        if request.method == 'POST':
            email = request.form['email']
            pazz = request.form['pass']
            con_pazz = request.form['c_pass']
            if pazz == con_pazz:
                if UserModel.VerifyEmail(email) is not True:
                    if 'file' not in request.files:
                        return render_template('create-account.html', msg='No file part')
                    file = request.files['file']
                    if file.filename == '':
                        return render_template('create-account.html', msg='No image selected for uploading')
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        if UserModel.CreateAccount(email, pazz, filename):
                            session['username'] = request.form['email']
                            return redirect(url_for('home'))
                    else:
                        return render_template('create-account.html', msg='Allowed image types are -> png, jpg, jpeg, gif')

                else:
                    return render_template('create-account.html', msg='User with email {mail}, Already Exist'.format(mail=email))
            else:
                return render_template('create-account.html', msg='Passwords does not match, Please confirm passwords')
        else:
            return render_template('create-account.html')
    else:
        # g.user = session['username']
        return redirect(url_for('home'))
        #     if UserModel.VerifyEmail(email) is not None:
        #         pass
        #     else:
        #         return render_template('create-account.html', msg='User with {user} Already Exist'.format(user=email))
        #
        #         # if 'file' not in request.files:
        #         #     return render_template('create-account.html', msg='No file part')
        #         # file = request.files['file']
        #         # if file.filename == '':
        #         #     return render_template('create-account.html', msg='No image selected for uploading')
        #         # if file and allowed_file(file.filename):
        #         #     filename = secure_filename(file.filename)
        #         #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #         #     if UserModel.CreateAccount(email, pazz, filename):
        #         #         session['username'] = request.form['email']
        #         #         return redirect(url_for('home'))
        #         #     else:
        #         #         return render_template('create-account.html', msg='We\'re Sorry an error accured')
        #         # else:
        #         #     return render_template('create-account.html', msg='Allowed image types are -> png, jpg, jpeg, gif')
        # else:
        #     return render_template('create-account.html', msg='Passwords does not match, Please confirm passwords')
    # else:
    #     return render_template('create-account.html')


@app.route('/edit-username', methods=['GET', 'POST'])
def EditUsername():
    if 'username' in session:
        g.user = session['username']
        user = UserModel.VerifyUser(g.user)
        # return render_template('edit-user.html', user=user, msg=user[5], usmsg=user[0])

        if request.method == 'POST':
            username = request.form['username']
            update = UserModel.UpdateUserName(username, user[0])
            if update is True:
                return render_template('edit-user.html', username=username, usmsg='Username Updated Successfully')
        else:
            return render_template('edit-user.html', user=user, msg=user[5])
    else:
        return render_template('homepage.html')


@app.route('/add-product', methods=['GET', 'POST'])
def AddProduct():
    if 'username' in session:
        g.user = session['username']
        user = UserModel.VeryfyEmail(g.user)
        # product = ProductModel.AllItem()
        # return render_template('add-product.html', user=user, msg=user[5])
        if request.method == 'POST':
            pname = request.form['product_name']
            des = request.form['text']
            if 'file' not in request.files:
                return render_template('add-product.html', usmsg='No file part')
            file = request.files['file']
            if file.filename == '':
                return render_template('add-product.html', usmsg='No image selected for uploading')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if ProductModel.AddItem(pname, des, filename, user[0]):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return render_template('add-product.html', usmsg='Product added Successfully')
                else:
                    return render_template('add-product.html', usmsg='Sorry an error occured')
            else:
                return render_template('add-product.html', usmsg='Allowed image types are -> png, jpg, jpeg, gif')
        else:
            return render_template('add-product.html')
    else:
        return render_template('homepage.html')


@app.route('/product', methods=['get', 'post'])
def UpdateProduct():
    if 'username' in session:
        g.user = session['username']
        if request.method == 'POST':
            pname = request.form['product_name']
            text = request.form['text']
            id = request.form['id']
            if ProductModel.UpdateItem(pname, text, id):
                return redirect(request.url, msg='Product Updated Successfully')
                # return render_template('product.html', msg='Product Updated Successfully')
        else:
            return redirect(url_for('home'))
    else:
        return render_template('homepage.html')


@app.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    if 'username' in session:
        g.user = session['username']
        item = UserModel.VeryfyEmail(g.user)

        if request.method == 'POST':
            pname = request.form['product_name']
            text = request.form['text']
            if ProductModel.UpdateItem(pname, text, id):
                flash('Product Updated Successfully')
                return redirect(request.url)
                # return render_template('product.html', msg='Product Updated Successfully')
        else:
            item = ProductModel.GetItemById(id)
            if item:
                return render_template('product.html', item=item)
            else:
                return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
        # return render_template('homepage.html')


@app.route('/delete/<id>', methods=['GET'])
def DeleteProduct(id):
    if 'username' in session:
        g.user = session['username']
        if ProductModel.GetItemById(id):
            ProductModel.DeleteProduct(id)
            flash('Product Deleted Successfully')
            return redirect(url_for('home'))
        else:
            flash('Product Not Found'), 404
    else:
        return redirect(url_for('home'))
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=4000, debug=True)
