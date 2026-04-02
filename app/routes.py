from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .database import db
from .models import Branch, Service, Ticket


main = Blueprint('main', __name__)

@main.route('/')
def index():
    branches = Branch.query.all()
    services = Service.query.all()
    return render_template('index.html', branches=branches, services=services)

@main.route('/admin-panel')
def admin_panel():
    # Bazadagi barcha chiptalarni vaqt bo'yicha saralab olish
    all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('admin.html', tickets=all_tickets)

@main.route('/complete-ticket/<int:ticket_id>')
def complete_ticket(ticket_id):
    # Chipta holatini o'zgartirish tugmasi uchun
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = 'completed'
    db.session.commit()
    return redirect(url_for('admin_panel'))

@main.route('/api/ticket', methods=['POST'])
def create_ticket():
    data = request.get_json()
    branch = Branch.query.get(data.get('branch_id'))
    service = Service.query.get(data.get('service_id'))

    if not branch or not service:
        return jsonify({'error': 'Filial yoki xizmat topilmadi'}), 400

    ticket_number = Ticket.generate_number(branch.code)
    ticket = Ticket(
        ticket_number=ticket_number,
        branch_id=branch.id,
        service_id=service.id
    )
    db.session.add(ticket)
    db.session.commit()

    waiting_count = Ticket.query.filter_by(
        branch_id=branch.id,
        status='waiting'
    ).count()

    return jsonify({
        'ticket_number': ticket_number,
        'branch': branch.name,
        'service': service.name,
        'queue_position': waiting_count,
        'estimated_wait': waiting_count * service.duration
    })

@main.route('/api/status/<ticket_number>')
def ticket_status(ticket_number):
    ticket = Ticket.query.filter_by(ticket_number=ticket_number).first()
    if not ticket:
        return jsonify({'error': 'Chipta topilmadi'}), 404

    position = Ticket.query.filter(
        Ticket.branch_id == ticket.branch_id,
        Ticket.status == 'waiting',
        Ticket.created_at <= ticket.created_at
    ).count()

    return jsonify({
        'ticket_number': ticket.ticket_number,
        'status': ticket.status,
        'branch': ticket.branch.name,
        'service': ticket.service.name,
        'queue_position': position,
        'estimated_wait': position * ticket.service.duration,
        'created_at': ticket.created_at.strftime('%H:%M')
    })

@main.route('/api/branches/<int:branch_id>/queue')
def branch_queue(branch_id):
    tickets = Ticket.query.filter_by(
        branch_id=branch_id,
        status='waiting'
    ).order_by(Ticket.created_at).limit(10).all()

    return jsonify([{
        'ticket_number': t.ticket_number,
        'service': t.service.name,
        'time': t.created_at.strftime('%H:%M')
    } for t in tickets])