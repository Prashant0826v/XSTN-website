import os
import re

BASE_DIR = r'c:\Users\prash\Desktop\XSTN Project\frontend'

# List of HTML files that need updating
pages_to_update = [
    'join-developer.html',  'team.html', 'pricing.html', 'blog.html',
    'services.html', 'projects.html', 'partner.html', 'faq.html',
    'consultation.html', 'test-form.html'
]

# Complete navbar with auth buttons
navbar_html = '''    <!-- NAVBAR -->
    <nav>
        <!-- LEFT AUTH BUTTONS -->
        <div class="nav-auth-buttons">
            <button id="loginBtn" class="nav-btn login-btn">Login</button>
            <button id="signupBtn" class="nav-btn signup-btn">Sign Up</button>
        </div>

        <!-- CENTER LOGO -->
        <img src="media/XTN.jpeg" class="logo">

        <!-- RIGHT MENU -->
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="team.html">Team</a></li>
            <li><a href="pricing.html">Services</a></li>
            <li><a href="blog.html">Blog</a></li>
            <li><a href="projects.html">Projects</a></li>
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="contact.html">Contact</a></li>
        </ul>

        <!-- USER PROFILE (Hidden by default) -->
        <div id="userProfile" class="user-profile" style="display: none;">
            <span id="userEmail"></span>
            <button id="logoutBtn" class="logout-btn">Logout</button>
        </div>

    </nav>

    <!-- AUTH MODAL -->
    <div id="authModal" class="modal">
        <div class="modal-content auth-modal">
            <button class="close-modal">&times;</button>
            
            <!-- LOGIN FORM -->
            <div id="loginForm" class="auth-form active">
                <h2>Welcome Back</h2>
                <p class="form-subtitle">Sign in to your account</p>
                
                <form id="loginFormElement">
                    <div class="form-group">
                        <label for="loginEmail">Email Address</label>
                        <input type="email" id="loginEmail" name="email" placeholder="your@email.com" required>
                        <small class="error-msg"></small>
                    </div>
                    
                    <div class="form-group">
                        <label for="loginPassword">Password</label>
                        <input type="password" id="loginPassword" name="password" placeholder="Enter your password" required>
                        <small class="error-msg"></small>
                    </div>

                    <div class="remember-forgot">
                        <label><input type="checkbox" name="remember"> Remember me</label>
                        <a href="#" id="forgotPasswordLink">Forgot password?</a>
                    </div>

                    <button type="submit" class="auth-submit-btn">Sign In</button>
                </form>

                <p class="auth-toggle">Don't have an account? <a href="#" id="toggleSignup">Create one</a></p>
            </div>

            <!-- SIGNUP FORM -->
            <div id="signupForm" class="auth-form">
                <h2>Create Account</h2>
                <p class="form-subtitle">Join XSTN community</p>
                
                <form id="signupFormElement">
                    <div class="form-group">
                        <label for="signupFirstName">First Name</label>
                        <input type="text" id="signupFirstName" name="first_name" placeholder="John" required>
                        <small class="error-msg"></small>
                    </div>

                    <div class="form-group">
                        <label for="signupLastName">Last Name</label>
                        <input type="text" id="signupLastName" name="last_name" placeholder="Doe" required>
                        <small class="error-msg"></small>
                    </div>

                    <div class="form-group">
                        <label for="signupEmail">Email Address</label>
                        <input type="email" id="signupEmail" name="email" placeholder="your@email.com" required>
                        <small class="error-msg"></small>
                    </div>

                    <div class="form-group">
                        <label for="signupPassword">Password (min 8 chars, 1 uppercase, 1 number)</label>
                        <input type="password" id="signupPassword" name="password" placeholder="Create strong password" required>
                        <small class="error-msg"></small>
                        <div class="password-strength">
                            <div class="strength-bar"></div>
                            <small id="strengthText"></small>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="signupConfirmPassword">Confirm Password</label>
                        <input type="password" id="signupConfirmPassword" name="confirm_password" placeholder="Re-enter password" required>
                        <small class="error-msg"></small>
                    </div>

                    <div class="form-group checkbox">
                        <input type="checkbox" id="signupTerms" name="terms" required>
                        <label for="signupTerms">I agree to Terms of Service and Privacy Policy</label>
                        <small class="error-msg"></small>
                    </div>

                    <button type="submit" class="auth-submit-btn">Create Account</button>
                </form>

                <p class="auth-toggle">Already have an account? <a href="#" id="toggleLogin">Sign in</a></p>
            </div>

            <!-- EMAIL VERIFICATION FORM -->
            <div id="verificationForm" class="auth-form">
                <h2>Verify Your Email</h2>
                <p class="form-subtitle">Enter the 6-digit code sent to <strong id="verifyEmail"></strong></p>
                
                <form id="verificationFormElement">
                    <div class="form-group">
                        <label for="verificationCode">Verification Code</label>
                        <input type="text" id="verificationCode" name="code" placeholder="000000" maxlength="6" required pattern="[0-9]{6}">
                        <small class="error-msg"></small>
                    </div>

                    <button type="submit" class="auth-submit-btn">Verify Email</button>
                </form>

                <p class="auth-toggle">Didn't receive code? <a href="#" id="resendCodeLink">Resend</a></p>
                <p class="auth-toggle"><a href="#" id="backToSignup">Back to signup</a></p>
            </div>

        </div>
    </div>

'''

for page in pages_to_update:
    file_path = os.path.join(BASE_DIR, page)
    if not os.path.exists(file_path):
        print(f"⚠ {page} - NOT FOUND")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'nav-auth-buttons' in content:
        print(f"✓ {page} - Already updated")
        continue

    # Replace <body> with <body> + navbar + modal
    content = re.sub(
        r'<body>',
        '<body>\n\n' + navbar_html,
        content,
        count=1
    )

    # Update script tags - add utils.js and auth.js before form.js or other scripts
    # Find the script section and insert utils.js and auth.js
    script_pattern = r'(<script src="config\.js"><\/script>)'
    if re.search(script_pattern, content):
        content = re.sub(
            script_pattern,
            r'    <script src="config.js"></script>\n    <script src="utils.js"></script>\n    <script src="auth.js"></script>',
            content
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ {page} - Updated successfully")

print("\n✅ All HTML pages updated!")
