# Portfolio Website - Setup Instructions

## Quick Start

1. **Assets Setup:**
   - Create a folder named `assets` in the same directory as `my.html`
   - **Profile Photo:** Place your profile photo in the `assets` folder
     - Name it exactly: `profile.jpg` (or update the path in HTML)
     - Recommended size: 400x500px or similar portrait orientation
     - Formats supported: JPG, PNG, WebP
   - **Resume File:** Place your resume PDF file in the `assets` folder
     - Name it exactly: `Dhruvi_Patel_Resume.pdf`
     - The download button will automatically work once the file is in place

2. **Open the Website:**
   - Simply open `my.html` in your web browser
   - Or use a local server (recommended):
     ```bash
     # Using Python
     python -m http.server 8000
     
     # Using Node.js (if you have it)
     npx http-server
     ```
   - Then visit: `http://localhost:8000`

## Features

### ✅ Contact Form
- Currently uses **mailto** link (opens your default email client)
- Form validates all fields before submitting
- Pre-fills email with subject and message

### ✅ Resume Download
- Click "Download Resume" button
- Automatically downloads `assets/Dhruvi_Patel_Resume.pdf`
- Shows error message if file is not found

### ✅ Email Me Button
- Opens email client with pre-filled subject
- Works without any backend

## Optional: Enable Direct Email Sending (EmailJS)

If you want the contact form to send emails directly (without opening email client):

1. Sign up at [EmailJS.com](https://www.emailjs.com/) (free tier available)
2. Create an email service and template
3. Get your Public Key, Service ID, and Template ID
4. In `my.html`, find the commented EmailJS code (around line 970)
5. Uncomment it and replace:
   - `YOUR_PUBLIC_KEY` with your EmailJS public key
   - `YOUR_SERVICE_ID` with your service ID
   - `YOUR_TEMPLATE_ID` with your template ID
6. The form will then send emails directly!

## File Structure

```
portfolio/
├── my.html                    # Main portfolio file
├── assets/
│   ├── profile.jpg            # Your profile photo (add this)
│   └── Dhruvi_Patel_Resume.pdf # Your resume (add this)
├── server.js                  # Optional Node.js server
├── package.json               # Optional Node.js dependencies
└── README.md                  # This file
```

## Troubleshooting

**Profile photo not showing?**
- Make sure the `assets` folder exists
- Check that the file is named exactly `profile.jpg` (or update the path in HTML line 640)
- File path is case-sensitive
- Supported formats: JPG, PNG, WebP
- If photo doesn't load, a placeholder will appear

**Resume not downloading?**
- Make sure the `assets` folder exists
- Check that the file is named exactly `Dhruvi_Patel_Resume.pdf`
- File path is case-sensitive

**Email not working?**
- Make sure you have a default email client configured
- Try clicking the "Email me" button to test
- Contact form uses mailto which requires an email client

**Contact form not submitting?**
- Check browser console for errors (F12)
- Make sure all fields are filled
- Email format must be valid (e.g., name@example.com)

## Support

If you need help, email: dhruvi080504@gmail.com

