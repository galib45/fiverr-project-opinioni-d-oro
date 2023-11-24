from myapp import app, db
from myapp.models import *


def send_coupon_email(customer, coupon):
    subject = f"Discount Coupon from {coupon.store.name}"
    sender = app.config["MAIL_USERNAME"]
    recipients = [customer.email]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = f"You received a discount coupon from {coupon.store.name}. Your coupon code is {coupon.code}. It will expire at {coupon.expire_date.strftime('%a %d %b %Y, %I:%M%p')} UTC"
    try:
        mail.send(msg)
        coupon.email_sent = True
        db.session.commit()
    except Exception as e:
        print(f"ERROR sending email to {customer.email}: {e}")
    # print(f'Sending email to {customer.email} for {coupon.code}')
    # print(f'ERROR: NOT IMPLEMENTED')


def send_coupon_sms(customer, coupon):
    print(f"Sending sms to {customer.email} for {coupon.code}")
    print(f"ERROR: NOT IMPLEMENTED")


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
        account_id_list = [customer.account_id for customer in store.customers]
        review_list = get_review_list(
            store.hex_id, datetime.timestamp(store.upto_timestamp)
        )
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
                customer.reviews.append(review)
                store.reviews.append(review)
                print(" - registered")
            else:
                print(" - not registered")
            store.upto_timestamp = timestamp_now
            db.session.commit()
