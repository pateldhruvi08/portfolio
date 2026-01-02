from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime
import sqlite3
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
    
    # Admin email
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'dhruvi080504@gmail.com'

app.config.from_object(Config)

# Database setup
def init_db():
    """Initialize the database with contacts table"""
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        text = msg.as_string()
        server.sendmail(app.config['MAIL_USERNAME'], to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def index():
    """Serve the main portfolio page"""
    return send_from_directory('.', 'my.html')

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    """Handle contact form submissions"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        data = request.get_json()
        
        # Check if data is None or empty
        if not data:
            return jsonify({'error': 'Invalid request. Please provide name, email, and message.'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip()
        message = data['message'].strip()
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Save to database
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contacts (name, email, message)
            VALUES (?, ?, ?)
        ''', (name, email, message))
        
        conn.commit()
        conn.close()
        
        # Send notification email to admin
        subject = f"New Portfolio Contact: {name}"
        body = f"""
        You have received a new message through your portfolio website:
        
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        
        Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        email_sent = send_email(app.config['ADMIN_EMAIL'], subject, body)
        
        # Send confirmation email to user
        if email_sent:
            confirmation_subject = "Thank you for contacting me!"
            confirmation_body = f"""
            Hi {name},
            
            Thank you for reaching out through my portfolio website. I have received your message and will get back to you as soon as possible.
            
            Your message:
            {message}
            
            Best regards,
            Dhruvi Patel
            """
            send_email(email, confirmation_subject, confirmation_body)
        
        logger.info(f"New contact form submission from {name} ({email})")
        
        response = jsonify({'message': 'Message sent successfully!'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        response = jsonify({'error': 'Internal server error'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact form submissions (admin endpoint)"""
    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY created_at DESC
        ''')
        
        contacts = []
        for row in cursor.fetchall():
            contacts.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'message': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        
        return jsonify({'contacts': contacts}), 200
        
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic statistics about the portfolio"""
    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        # Get total contacts
        cursor.execute('SELECT COUNT(*) FROM contacts')
        total_contacts = cursor.fetchone()[0]
        
        # Get contacts this month
        cursor.execute('''
            SELECT COUNT(*) FROM contacts 
            WHERE created_at >= date('now', 'start of month')
        ''')
        monthly_contacts = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'total_contacts': total_contacts,
            'monthly_contacts': monthly_contacts,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/resume', methods=['GET'])
def get_resume():
    """Download resume file"""
    try:
        resume_path = os.path.join('assets', 'Dhruvi_Patel_Resume.pdf')
        if os.path.exists(resume_path):
            return send_from_directory('assets', 'Dhruvi_Patel_Resume.pdf', as_attachment=True)
        else:
            return jsonify({'error': 'Resume file not found'}), 404
    except Exception as e:
        logger.error(f"Error serving resume: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)