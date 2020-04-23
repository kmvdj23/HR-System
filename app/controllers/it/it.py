from flask import redirect, request, render_template, url_for, flash, Blueprint
from flask_login import login_required, current_user
from lib import generate_random_password, password_encrypt, password_decrypt
from app.lib import Dashboard, it_user
from app.models import Account, Notification
from app.config import db
from app.forms import AccountForm
from wtforms.validators import DataRequired


it = Blueprint('it', __name__, url_prefix='/it')


# =========================== GET METHODS ===========================================

@it.route('/dashboard')
@login_required
@it_user
def home_page():
    accounts = Account.get_all_accounts()
    stats = Dashboard()
    return render_template('pages/account/it/dashboard.html', accounts=accounts, stats=stats)


@it.route('/accounts')
@login_required
@it_user
def accounts_page():
    accounts = Account.get_all_accounts()
    return render_template('pages/account/it/accounts.html' , accounts=accounts)


@it.route('/account/<username>')
@login_required
@it_user
def account_page(username):
    account = Account.find_account(username)
    if not account:
        flash('Account does not Exist')
        return redirect(url_for('it.accounts_page'))
    return render_template('pages/account/it/account.html' , account=account)


@it.route('/account/<username>/edit')
@login_required
@it_user
def edit_page(username):
    account = Account.find_account(username)
    generated_password = generate_random_password()

    if not account:
        flash('User does not exist', 'danger')
        return redirect(url_for('it.accounts_page'))

    form = AccountForm(obj=account)

    return render_template('pages/write_account.html', form=form, account=account, generated_password=generated_password)


@it.route('/account/register')
@login_required
@it_user
def register_page():
    form = AccountForm()

    # Set required fields
    form.password.validators.append(DataRequired())
    form.confirm_pass.validators.append(DataRequired())

    return render_template('pages/write_account.html', form=form)


# =========================== POST METHODS ===========================================

@it.route('/account/register', methods=['POST'])
@login_required
@it_user
def register():
    form = AccountForm()

    # Set required fields
    form.password.validators.append(DataRequired())
    form.confirm_pass.validators.append(DataRequired())

    if form.validate_on_submit():
        account = Account()
        form.populate_obj(account)

        account.password = password_encrypt(account.password)

        db.session.add(account)
        db.session.commit()

        notif = Notification(
            category='success',
            icon='fas fa-star',
            title='Welcome to HRSystem',
            redirect=url_for('main.home_page'),
            account_id=account.id
        )

        db.session.add(notif)
        db.session.commit()

        flash(f'Account for { account.username } created successfully',
            'success')
    else:
        flash('Account not created', 'danger')
        print('==================== ERRORS: register() ================')
        for err in form.errors:
            print(err)
            return render_template('pages/write_account.html', form=form)

    return redirect(url_for('it.accounts_page'))


@it.route('/account/<username>/edit', methods=['POST'])
@login_required
@it_user
def edit(username):
    account = Account.find_account(username)
    generated_password = generate_random_password()
    form = AccountForm(obj=account)

    if form.validate_on_submit():
        form.populate_obj(account)

        db.session.commit()

        flash(f'Account updated for { account.username }',
            'success')
    else:
        flash('Account not modified', 'danger')

        print('==================== ERRORS: edit() ================')
        for err in form.errors:
            print(err)

        return render_template('pages/write_account.html', form=form, account=account, generated_password=generated_password)

    return redirect(url_for('it.accounts_page'))


@it.route('/account/<username>/passwordreset', methods=['POST'])
@login_required
@it_user
def reset_password(username):
    account = Account.find_account(username)
    account.password = password_encrypt(request.form.get('generated_password'))
    db.session.commit()
    flash('Password for {0} has been reset: {1}'.format(account.username,
        request.form.get('generated_password')), 'success')
    return redirect(url_for('it.edit_page', username=username))


@it.route('/account/<username>/toggle', methods=['POST'])
@login_required
@it_user
def toggle_status(username):
    account = Account.find_account(username)
    account.active = not account.active
    db.session.commit()
    return redirect(url_for('it.accounts_page'))
