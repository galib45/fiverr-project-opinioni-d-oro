from datetime import datetime, timedelta

from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from myapp import app, db
from myapp.forms import NewCampaignForm
from myapp.models import Campaign
from myapp.utils import generate_campaign_code


@app.route("/dashboard/campaigns")
def dashboard_campaigns():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            return render_template("dashboard-campaigns.html")
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/dashboard/campaigns/add", methods=["GET", "POST"])
def dashboard_campaigns_add():
    if current_user.is_anonymous:
        return redirect(url_for("login"))
    elif current_user.username == "admin":
        return redirect(url_for("dashboard"))
    else:
        form = NewCampaignForm()
        if form.validate_on_submit():
            store = current_user.stores[0]
            name = form.name.data
            description = form.description.data
            offer = form.offer.data
            expire_date = datetime.strptime(
                form.expire_date.data, "%B %d, %Y"
            ) - timedelta(hours=1)
            campaign_code = generate_campaign_code(store.name, name)
            campaign = Campaign(
                name=name,
                description=description,
                offer=offer,
                expire_date=expire_date,
                code=campaign_code,
            )
            store.campaigns.append(campaign)
            db.session.commit()
            return redirect(url_for("dashboard_campaigns"))
        return render_template("dashboard-campaigns-add.html", form=form)
