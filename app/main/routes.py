from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from .forms import ProjectForm, CollabForm
from .models import Project, Collaborator, Note
from . import bp

@bp.route('/')
@login_required
def homepage():
    user_notes = Note.query.filter_by(user_id=current_user.id).first()
    projects = Project.query.all()
    collaborators = Collaborator.query.all()
    return render_template('main/homepage.html', user_notes=user_notes, projects=projects, collaborators=collaborators)

@bp.route('/save_note', methods=['POST'])
@login_required
def save_note():
    content = request.json.get('content')
    note = Note.query.filter_by(user_id=current_user.id).first()
    if not note:
        note = Note(user_id=current_user.id, content=content)
        db.session.add(note)
    else:
        note.content = content
    db.session.commit()
    return jsonify({"status": "success"})

@bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.particularities = form.particularities.data
        project.status = form.status.data
        project.pcollaborators = form.pcollaborators.data
        db.session.commit()
        return redirect(url_for('main.homepage'))
    return render_template('main/edit_project.html', form=form, project=project)

@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            particularities=form.particularities.data,
            status=form.status.data,
            pcollaborators=form.pcollaborators.data,
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('main.homepage'))
    return render_template('main/add_project.html', form=form)

@bp.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully', 'success')
    return redirect(url_for('main.homepage'))

@bp.route('/edit_collaborator/<int:collab_id>', methods=['GET', 'POST'])
@login_required
def edit_collaborator(collab_id):
    collaborator = Collaborator.query.get_or_404(collab_id)
    form = CollabForm(obj=collaborator)
    if form.validate_on_submit():
        collaborator.type_ = form.type_.data
        collaborator.name = form.name.data
        collaborator.particularities = form.particularities.data
        collaborator.email = form.email.data
        collaborator.othercontact = form.othercontact.data
        db.session.commit()
        return redirect(url_for('main.homepage'))
    return render_template('main/edit_collaborator.html', form=form, collaborator=collaborator)

@bp.route('/add_collaborator', methods=['GET', 'POST'])
@login_required
def add_collaborator():
    form = CollabForm()
    if form.validate_on_submit():
        new_collaborator = Collaborator(
            type_=form.type_.data,
            name=form.name.data,
            particularities=form.particularities.data,
            email=form.email.data,
            othercontact=form.othercontact.data,
        )
        db.session.add(new_collaborator)
        db.session.commit()
        flash('Collaborator added successfully!', 'success')
        return redirect(url_for('main.homepage'))
    return render_template('main/add_collaborator.html', form=form)

@bp.route('/delete_collaborator/<int:collab_id>', methods=['POST'])
@login_required
def delete_collaborator(collab_id):
    collaborator = Collaborator.query.get_or_404(collab_id)
    db.session.delete(collaborator)
    db.session.commit()
    flash('Collaborator deleted successfully', 'success')
    return redirect(url_for('main.homepage'))

