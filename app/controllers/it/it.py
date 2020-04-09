from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from lib import generate_random_password, password_encrypt
from app.models import Account
from app.config import db
from app.forms import AddUserForm, EditUserForm

it = Blueprint('it', __name__, url_prefix='/it')


# =========================== GET METHODS ===========================================
@it.route('/dashboard')
@login_required
def home_page():
    accounts = Account.get_all_accounts()
    return render_template('pages/account/dashboard_it.html', accounts=accounts)


@login_required
@it.route('/accounts')
def accounts_page():
    accounts = Account.get_all_accounts()
    return render_template('pages/account/it/accounts.html' , accounts=accounts)


@login_required
@it.route('/account/<username>')
def account_page(username):
    account = Account.find_account(username)
    if not account:
        flash('Account does not Exist')
        return redirect(url_for('it.accounts_page'))
    return render_template('pages/account/it/account.html' , account=account)   


@login_required
@it.route('/account/<username>/edit')
def edit_page(username):
    # Generate Password
    form = EditUserForm(request.form)
    account = Account.find_account(username)
    generated_password = generate_random_password()

    if not account:
        flash('User does not exist', 'danger')
        return redirect(url_for('it.accounts_page'))

    # TODO: Set other values here instead
    form.account_type.default = account.account_type
    form.process()

    return render_template('pages/account/it/edit_user.html', form=form, account=account, generated_password=generated_password)


@login_required
@it.route('/register')
def register_page():
    form = AddUserForm(request.form)
    return render_template('pages/account/it/add_user.html', form=form)


# ============================= POST METHODS =========================================


@login_required
@it.route('/register', methods=['POST'])
def register():
    form = AddUserForm(request.form)

    if form.validate_on_submit():
        account = Account(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            username=request.form.get('username'),
            mobile_number=request.form.get('mobile'),
            password=password_encrypt(request.form.get('password')), 
            account_type=int(request.form.get('account_type'))
        )

        db.session.add(account)
        db.session.commit()

        flash('Account for {0} created successfully'.format(account.username), 'success')
    else:
        flash('Account not created', 'danger')
        
        print('==================== ERRORS: register() ================')
        for err in form.errors:
            print(err)
        
        return render_template('pages/account/it/add_user.html', form=form)

    return redirect(url_for('it.register_page'))


@login_required
@it.route('/account/<username>/edit', methods=['POST'])
def edit(username):
    # Flask Form Change Password
    form = EditUserForm(request.form)
    account = Account.find_account(username)
    generated_password = generate_random_password()

    if form.validate_on_submit():
        account.first_name = request.form.get('first_name')
        account.last_name = request.form.get('last_name')
        account.username = request.form.get('username')
        account.mobile_number = request.form.get('mobile')
        account.account_type = int(request.form.get('account_type'))

        db.session.commit()

        flash('Account updated for {0}'.format(account.username))
    else:
        flash('Account not modified', 'danger')
        
        print('==================== ERRORS: edit() ================')
        for err in form.errors:
            print(err)
        
        return render_template('pages/account/it/edit_user.html', form=form, account=account, generated_password=generated_password)

    return redirect(url_for('it.edit_page', username=username))


@login_required
@it.route('/account/<username>/passwordreset', methods=['POST'])
def reset_password(username):
    account = Account.find_account(username)
    account.password = password_encrypt(request.form.get('generated_password'))
    db.session.commit()
    flash('Password for {0} has been reset: {1}'.format(account.username, account.password), 'success')
    return redirect(url_for('it.edit_page', username=username))


@login_required
@it.route('/account/<username>/toggle', methods=['POST'])
def toggle_status(username):
    account = Account.find_account(username)
    account.active = not account.active
    db.session.commit()
    return redirect(url_for('it.accounts_page'))
