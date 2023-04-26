from flask import render_template, url_for, flash, redirect, Blueprint, request, session, jsonify
from flask_login import current_user, login_required
from sqlalchemy import func
from mar_tierra import db
from mar_tierra.models import User, Home, Project
from mar_tierra.views.admins.forms import NewHome_Project_Form
from bs4 import BeautifulSoup
import requests
import googlesearch as gs

from mar_tierra.views.projects.forms import UpdateHome_Project_Form

projects = Blueprint('projects', __name__)


def search(keyword, zipcode):
    url = f"https://www.google.com/search?q={keyword}+in+zip+code+{zipcode}&num=10"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    result_div = soup.find_all('div', attrs={'class': 'g'})
    search_results = []
    for r in result_div:
        try:
            link = r.find('a', href=True)
            if link != '':
                header = r.find('h3').text
                search_results.append({'link': link['href'], 'header': header})
        except:
            continue
    return search_results

@projects.route("/home_project_item/new", methods=['GET', 'POST'])
@login_required
def new_item_to_admin_project():
    form = NewHome_Project_Form(request.form)
    current_home_id = request.args.get('home_item')

    if request.method == 'POST' and request.form.get('submit') == 'search':
        # Handle search request
        keyword = request.form['keyword']
        zipcode = request.form['zipcode']
        results = search(keyword, zipcode)
        print(results)
        return render_template('project/new_project_item.html', title='New Product', form=form,
                           current_home_id=current_home_id, id=current_home_id, results=results)

    elif request.method == 'POST' and request.form.get('submit') == 'submit':
        # Handle form submission
        if form.validate_on_submit():
            project_item = Project(
                category=form.category.data,
                action=form.action.data,
                description=form.description.data,
                provider=form.provider.data,
                target_date=form.target_date.data,
                cost_estimate=form.cost_estimate.data,
                actual_cost=form.actual_cost.data,
                home_item_id=current_home_id)

            db.session.add(project_item)
            db.session.commit()
            flash('Amazing selections moving to our next phase', 'success')
            return redirect(url_for('projects.project_detail', id=current_home_id))
        else:
            # Form validation failed, render the form again with error messages
            return render_template('project/new_project_item.html', title='New Product', form=form,
                               current_home_id=current_home_id, id=current_home_id)

    # Render the form if no POST request has been made yet
    return render_template('project/new_project_item.html', title='New Product', form=form,
                       current_home_id=current_home_id, id=current_home_id)




@projects.route("/home_project/<int:id>", methods=['GET', 'POST'])
@login_required
def project_detail(id):
    home = Home.query.get_or_404(id)
    home_item = Home.query.filter_by(id=id).first()
    # get existing Home project items
    project_items = Project.query.filter_by(home_item_id=id).all()
    total_cost_estimate = db.session.query(func.sum(Project.cost_estimate)).\
        filter_by(home_item_id=id).scalar() or 0
    actual_cost = db.session.query(func.sum(Project.actual_cost)). \
                              filter_by(home_item_id=id).scalar() or 0

    cost_by_category = db.session.query(Project.category, func.sum(Project.cost_estimate)). \
        filter_by(home_item_id=id).group_by(Project.category).all()

    return render_template('project/project.html',
                           home_item=home_item,
                           home=home,
                           project_items=project_items,
                           total_cost_estimate=total_cost_estimate,
                           actual_cost=actual_cost,
                           cost_by_category=cost_by_category)

#################### Actions ####################


@projects.route("/update_project/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_project_item(id):
    project_item = Project.query.get_or_404(id)
    current_home_id = project_item.home_item_id
    form = UpdateHome_Project_Form(request.form)

    if form.validate_on_submit():
        project_item.category = form.category.data
        project_item.action = form.action.data
        project_item.description = form.description.data
        project_item.provider = form.provider.data
        project_item.target_date = form.target_date.data
        project_item.cost_estimate = form.cost_estimate.data
        project_item.actual_cost = form.actual_cost.data
        db.session.commit()

        flash('Your home project has been updated!', 'success')
        return redirect(url_for('projects.project_detail', id=current_home_id))

    elif request.method == 'GET':
        form.category.data = project_item.category
        form.action.data = project_item.action
        form.description.data = project_item.description
        form.provider.data = project_item.provider
        form.target_date.data = project_item.target_date
        form.cost_estimate.data = project_item.cost_estimate
        form.actual_cost.data = project_item.actual_cost

    return render_template('project/update_project_item.html', title='Update Home Project',
                           form=form, current_home_id=current_home_id, id=id)



@projects.route("/project_item_delete/<int:id>", methods=['GET','POST'])
@login_required
def delete_project_item(id):
    delete_project_item = Project.query.get_or_404(id)
    current_home_id = delete_project_item.home_item_id  # assuming home_item is a relationship
    db.session.delete(delete_project_item)
    db.session.commit()
    flash('The Project Item was deleted', 'danger')
    return redirect(url_for('projects.project_detail', id=current_home_id))


