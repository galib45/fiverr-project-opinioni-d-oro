from threading import Thread
from myapp import app, db, mail
from myapp.models import *
from datetime import datetime, timedelta
from flask import render_template
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"ERROR sending email to {customer.email}: {e}")


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_coupon_email(customer, coupon):
    cet_expire_date = coupon.expire_date + timedelta(hours=1)
    formatted_expire_date = cet_expire_date.strftime("%B %d, %Y %I:%M %p")
    print(f"Sending email to {customer.email} for {coupon.code}")
    send_email(
        subject="Discount Coupon",
        recipients=[customer.email],
        text_body=render_template("email/coupon.txt", coupon=coupon, customer=customer, formatted_expire_date=formatted_expire_date),
        html_body=render_template("email/coupon.html", coupon=coupon, customer=customer, formatted_expire_date=formatted_expire_date)
    )
    coupon.email_sent = True
    db.session.commit()
    


def send_coupon_sms(customer, coupon):
    from myapp.utils import sendtext
    cet_expire_date = coupon.expire_date + timedelta(hours=1)
    formatted_expire_date = cet_expire_date.strftime("%B %d, %Y %I:%M %p")
    print(f"Sending sms to {customer.email} for {coupon.code}")
    status = sendtext(
        [customer.phone_number], 
        render_template("email/coupon.txt", coupon=coupon, customer=customer, formatted_expire_date=formatted_expire_date)
    )
    coupon.sms_sent = True
    db.session.commit()


@app.cli.command("send-coupons")
def send_coupons():
    customers = db.session.scalars(db.select(Customer)).all()
    for customer in customers:
        for coupon in customer.coupons:
            if not coupon.email_sent:
                send_coupon_email(customer, coupon)
            if not coupon.sms_sent:
                send_coupon_sms(customer, coupon)


@app.cli.command("fetch-reviews")
def fetch_reviews():
    from myapp.utils import generate_random_code, get_review_list

    stores = db.session.scalars(db.select(Store)).all()
    timestamp_now = datetime.utcnow()
    for store in stores:
        if store.package == 'basic': continue
        if store.package == 'basic-unlimited': continue
        if store.owner.state != 'active': continue
        print(f"Fetching reviews for {store.name}, package is {store.package}")
        account_id_list = [customer.account_id for customer in store.customers]
        review_list = get_review_list(
            store.hex_id, datetime.timestamp(store.upto_timestamp)
        )
        print(f"{len(review_list)} reviews fetched")
        for review in review_list:
            account_id, timestamp, rating, text, photos = review
            print(account_id, end="")
            if account_id in account_id_list:
                customer = db.session.scalar(
                    db.select(Customer).filter_by(account_id=review[0])
                )
                review = Review()
                update = Update(rating=rating, text=text, timestamp=timestamp)
                for item in photos:
                    photo = Photo(url=f"https://lh5.googleusercontent.com/p/{item}")
                    update.photos.append(photo)
                review.updates.append(update)

                if review.updates.count() == 1:
                    if customer.coupons.count() > 0:
                        days_after_last_coupon = (
                            timestamp_now - customer.got_coupon_date
                        ).days
                        if days_after_last_coupon < 15:
                            # generate coupon
                            coupon = Coupon(
                                code=generate_random_code(),
                                expire_date=timestamp_now + timedelta(days=30),
                                offer = store.general_coupon_offer
                            )
                            customer.coupons.append(coupon)
                            customer.got_coupon_date = timestamp_now
                            store.coupons.append(coupon)
                    else:
                        # generate coupon
                        coupon = Coupon(
                            code=generate_random_code(),
                            expire_date=timestamp_now + timedelta(days=30),
                        )
                        customer.coupons.append(coupon)
                        customer.got_coupon_date = timestamp_now
                        store.coupons.append(coupon)
                        store.coupons_generated += 1
                customer.reviews.append(review)
                store.reviews.append(review)
                print(" - registered")
            else:
                print(" - not registered")
            store.upto_timestamp = timestamp_now
            db.session.commit()
