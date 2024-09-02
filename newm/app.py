from flask import Flask, render_template, request, jsonify, session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize WebDriver
def init_driver():
    service = Service(executable_path='/Users/markdsouza/Downloads/chromedriver-mac-arm64/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for testing
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to get translated messages
def get_translated_message(key, language):
    translations = {
        'are_you_indian': {
            'en': 'Are you Indian? (yes/no)',
            'hi': 'क्या आप भारतीय हैं? (हाँ/नहीं)',
            'mr': 'तुम भारतीय आहात का? (होय/नाही)'
        },
        'group_or_individual': {
            'en': 'Are you selecting for group or individual? (group/individual)',
            'hi': 'क्या आप समूह या व्यक्तिगत के लिए चयन कर रहे हैं? (समूह/व्यक्तिगत)',
            'mr': 'तुम गटासाठी किंवा वैयक्तिकासाठी निवडत आहात का? (गट/वैयक्तिक)'
        },
        'phone_number': {
            'en': 'Please enter your phone number:',
            'hi': 'कृपया अपना फोन नंबर दर्ज करें:',
            'mr': 'कृपया आपला फोन नंबर प्रविष्ट करा:'
        },
        'email': {
            'en': 'Please enter your email address:',
            'hi': 'कृपया अपनी ईमेल पता दर्ज करें:',
            'mr': 'कृपया आपला ईमेल पत्ता प्रविष्ट करा:'
        },
        'children_students': {
            'en': 'Please enter the number of children/students:',
            'hi': 'कृपया बच्चों/छात्रों की संख्या दर्ज करें:',
            'mr': 'कृपया मुलांचे/विद्यार्थ्यांचे संख्यांक प्रविष्ट करा:'
        },
        'adults_teachers': {
            'en': 'Please enter the number of adults/teachers:',
            'hi': 'कृपया वयस्कों/शिक्षकों की संख्या दर्ज करें:',
            'mr': 'कृपया प्रौढ/शिक्षकांची संख्या प्रविष्ट करा:'
        },
        'day': {
            'en': 'Enter the day (e.g., 15):',
            'hi': 'दिन दर्ज करें (उदा., 15):',
            'mr': 'दिन प्रविष्ट करा (उदा., 15):'
        },
        'month': {
            'en': 'Enter the month (e.g., September):',
            'hi': 'माह दर्ज करें (उदा., सितंबर):',
            'mr': 'महिना प्रविष्ट करा (उदा., सप्टेंबर):'
        },
        'year': {
            'en': 'Enter the year (e.g., 2024):',
            'hi': 'साल दर्ज करें (उदा., 2024):',
            'mr': 'वर्ष प्रविष्ट करा (उदा., 2024):'
        },
        'confirm_details': {
            'en': 'Please confirm that all your details are correct.',
            'hi': 'कृपया पुष्टि करें कि आपके सभी विवरण सही हैं।',
            'mr': 'कृपया पुष्टी करा की आपल्या सर्व तपशील योग्य आहेत.'
        },
        'confirm_screenshot': {
            'en': 'Please confirm if all details are correct before proceeding to screenshot.',
            'hi': 'कृपया स्क्रीनशॉट लेने से पहले पुष्टि करें कि सभी विवरण सही हैं।',
            'mr': 'स्क्रीनशॉट घेण्यापूर्वी कृपया सर्व तपशील योग्य आहेत का ते पुष्टी करा.'
        },
        'site_link': {
            'en': 'You can complete your booking by visiting the following link:',
            'hi': 'आप निम्नलिखित लिंक पर जाकर अपनी बुकिंग पूरी कर सकते हैं:',
            'mr': 'आप पुढील लिंकवर जाऊन आपली बुकिंग पूर्ण करू शकता:'
        }
    }
    return translations.get(key, {}).get(language, translations[key]['en'])

@app.route('/')
def index():
    session.clear()  # Clear session on new visit
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    language = request.json.get('language', 'en')  # Default to English if no language is provided
    response = ""
    step = session.get('step', 0)

    if 'language' not in session:
        session['language'] = language

    # Update the session language if it has changed
    if language != session.get('language'):
        session['language'] = language
        step = 0  # Restart the conversation if language changes

    if step == 0:
        response = get_translated_message('are_you_indian', session['language'])
        session['step'] = 1

    elif step == 1:
        if user_input.lower() in ['yes', 'no']:
            session['is_indian'] = user_input.lower()
            response = get_translated_message('group_or_individual', session['language'])
            session['step'] = 2
        else:
            response = get_translated_message('are_you_indian', session['language'])

    elif step == 2:
        if user_input.lower() in ['group', 'individual']:
            session['group_type'] = user_input.lower()
            response = get_translated_message('phone_number', session['language'])
            session['step'] = 3
        else:
            response = get_translated_message('group_or_individual', session['language'])

    elif step == 3:
        session['phone_number'] = user_input
        response = get_translated_message('email', session['language'])
        session['step'] = 4

    elif step == 4:
        session['email'] = user_input
        response = get_translated_message('children_students', session['language'])
        session['step'] = 5

    elif step == 5:
        session['no_of_children_students'] = user_input
        response = get_translated_message('adults_teachers', session['language'])
        session['step'] = 6

    elif step == 6:
        session['no_of_adults_teachers'] = user_input
        response = get_translated_message('day', session['language'])
        session['step'] = 7

    elif step == 7:
        session['day'] = user_input
        response = get_translated_message('month', session['language'])
        session['step'] = 8

    elif step == 8:
        session['month'] = user_input
        response = get_translated_message('year', session['language'])
        session['step'] = 9

    elif step == 9:
        session['year'] = user_input
        response = get_translated_message('confirm_details', session['language'])
        session['step'] = 10

    elif step == 10:
        # Start Selenium to perform scraping
        driver = init_driver()
        driver.get('https://nationalmuseumindia.gov.in/en/online-ticket-booking')

        # Perform steps based on session data
        is_indian = session.get('is_indian', 'yes')
        if is_indian == 'yes':
            driver.find_element(By.ID, 'user_type_1').click()
        else:
            driver.find_element(By.ID, 'user_type_2').click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'category_id'))).click()

        group_type = session.get('group_type', 'individual')
        if group_type == 'individual':
            driver.find_element(By.CSS_SELECTOR, 'option[value="1"]').click()
        else:
            driver.find_element(By.CSS_SELECTOR, 'option[value="2"]').click()

        driver.find_element(By.ID, 'mobile_no').send_keys(session.get('phone_number', ''))
        driver.find_element(By.ID, 'email').send_keys(session.get('email', ''))
        driver.find_element(By.ID, 'no_of_children_students').send_keys(session.get('no_of_children_students', ''))
        driver.find_element(By.ID, 'no_of_adults_teachers').send_keys(session.get('no_of_adults_teachers', ''))

        total_persons = int(session.get('no_of_children_students', '0')) + int(session.get('no_of_adults_teachers', '0'))
        driver.find_element(By.ID, 'no_of_total_persons').send_keys(str(total_persons))

        datepicker_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "datepicker")))
        datepicker_div.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "datepicker-days")))

        desired_year = session.get('year')
        year_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "datepicker-switch")))
        while year_selector.text.split()[-1] != desired_year:
            year_selector.click()
            year_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "datepicker-switch")))

        desired_month = session.get('month')
        current_month = driver.find_element(By.CLASS_NAME, "datepicker-switch").text.split()[0]
        while current_month != desired_month:
            if current_month < desired_month:
                driver.find_element(By.CLASS_NAME, "next").click()
            else:
                driver.find_element(By.CLASS_NAME, "prev").click()
            current_month = driver.find_element(By.CLASS_NAME, "datepicker-switch").text.split()[0]

        desired_day = session.get('day')
        day_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//tbody//td[contains(@class, 'day') and text()='{desired_day}']"))
        )
        day_element.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.showPopup.btn'))
        ).click()

        # Wait for 10 seconds before taking a screenshot
        time.sleep(10)

        # Screenshot
        screenshot_path = os.path.join('static', 'screenshot.png')
        driver.save_screenshot(screenshot_path)
        driver.quit()

        response = get_translated_message('confirm_screenshot', session['language']) + " " + get_translated_message('site_link', session['language']) + " https://nationalmuseumindia.gov.in/en/online-ticket-booking"

    return jsonify({'response': response, 'screenshot': screenshot_path if step >= 10 else None})

if __name__ == '__main__':
    app.run(debug=True)
