import json
from datetime import datetime, timedelta

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user

from myapp import app, db, decorators, mail
from myapp.forms import NewCampaignForm
from myapp.models import Action, Campaign, Customer, Coupon
from myapp.utils import generate_campaign_code, generate_random_code, sendtext
from threading import Thread
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

@app.route("/dashboard/campaigns")
@decorators.shop_owner_required
@decorators.verified_email_required
def dashboard_campaigns():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            return render_template("dashboard-campaigns.html")
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/dashboard/campaigns/add", methods=["GET", "POST"])
@decorators.shop_owner_required
@decorators.verified_email_required
def dashboard_campaigns_add():
    if current_user.is_anonymous:
        return redirect(url_for("login"))
    elif current_user.username == "admin":
        return redirect(url_for("dashboard"))
    else:
        store = current_user.stores[0]
        unlimited = False
        if store.package == 'basic': quota = 2
        elif store.package == '5star': quota = 4
        elif store.package == 'basic-unlimited' or store.package == '5star-unlimited': unlimited = True
        else: abort(500)
        campaigns_this_month = db.session.scalars(db.select(Campaign)
            .where(Campaign.store==store)
            .where(Campaign.date_created > datetime.utcnow() - timedelta(days=30))
        ).all()
        if not unlimited and len(campaigns_this_month) == quota: 
            flash('Sorry! You have used up your monthly quota', category='error')
            return redirect(url_for('dashboard_campaigns'))
        form = NewCampaignForm()
        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            offer = form.offer.data
            category = form.category.data
            expire_date = datetime.strptime(
                form.expire_date.data, "%B %d, %Y"
            ) - timedelta(hours=1)
            campaign_code = generate_campaign_code(store.name, name)
            campaign = Campaign(
                name=name,
                description=description,
                offer=offer,
                date_created = datetime.utcnow(),
                expire_date=expire_date,
                code=campaign_code,
                category=category
            )
            store.campaigns.append(campaign)
            db.session.commit()
            action = Action(
                category="campaign",
                data=str(campaign.id),
                date_created=datetime.utcnow(),
            )
            db.session.add(action)
            db.session.commit()
            return redirect(url_for("dashboard_campaigns"))
        return render_template("dashboard-campaigns-add.html", form=form)


@app.route("/dashboard/campaigns/<id>/delete")
@decorators.shop_owner_required
@decorators.verified_email_required
def delete_campaign(id):
    campaign = db.session.get(Campaign, id)
    if campaign:
        db.session.delete(campaign)
        flash(f"Removed campaign successfully")
        db.session.commit()
        return redirect(url_for("dashboard_campaigns"))
    abort(404)



@app.route("/dashboard/campaigns/<id>/view", methods=["GET", "POST"])
@decorators.shop_owner_required
@decorators.verified_email_required
def view_campaign(id):
    store = current_user.stores[0]
    campaign = db.session.get(Campaign, id)
    cet_expire_date = campaign.expire_date + timedelta(hours=1)
    formatted_expire_date = cet_expire_date.strftime("%B %d, %Y %I:%M %p")
    if not campaign: abort(404)
    if request.method == "POST":
        customer_id_list = request.form.getlist("customers")
        phone_numbers = []
        emails = []
        for customer_id in customer_id_list:
            customer = db.session.get(Customer, int(customer_id))
            if not customer: continue
            if customer in campaign.customers: continue
            campaign.customers.append(customer)
            if campaign.category == 'general':
                phone_numbers.append(customer.phone_number)
                emails.append(customer.email)
            else:
                coupon = Coupon(
                    code = campaign.code + generate_random_code(4),
                    expire_date = campaign.expire_date,
                    offer = campaign.offer
                )
                customer.coupons.append(coupon)
                customer.got_coupon_date = datetime.utcnow()
                store.coupons.append(coupon)
                message = render_template("email/campaign.txt", store=store, campaign=campaign, coupon=coupon, formatted_expire_date=formatted_expire_date)
                sendtext([customer.phone_number], message)
                send_email(
                    subject = "New Campaign",
                    recipients = [customer.email],
                    text_body = message,
                    html_body = render_template("email/campaign.html", store=store, campaign=campaign, coupon=coupon, formatted_expire_date=formatted_expire_date)
                )

        db.session.commit()
        if campaign.category == 'general':
            message = render_template("email/campaign.txt", store=store, campaign=campaign, formatted_expire_date=formatted_expire_date)
            sendtext(phone_numbers, message)
            send_email(
                subject = "New Campaign",
                recipients = emails,
                text_body = message,
                html_body = render_template("email/campaign.html", store=store, campaign=campaign, formatted_expire_date=formatted_expire_date)
            )
    return render_template("view-campaign.html", campaign=campaign, store=store)
    

