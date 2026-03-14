const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    
    // Catch console logs
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));

    // Use localhost:5500 exactly as user views it
    await page.goto('http://127.0.0.1:5500/signup.html', { waitUntil: 'networkidle0' });

    console.log('Testing the popup function directly...');
    
    // Inject showSuccessPopup call
    await page.evaluate(() => {
        showSuccessPopup('This is a test forced from Puppeteer!', document.getElementById('signupForm'), () => {
             console.log('Popup closed callback executed');
        });
    });

    // Wait 1 second for animation
    await new Promise(r => setTimeout(r, 1000));
    
    // Check if visible
    const isVisible = await page.evaluate(() => {
        const popup = document.querySelector('.xstn-popup-overlay.active');
        if (!popup) return false;
        const style = window.getComputedStyle(popup);
        return style.display !== 'none' && style.opacity !== '0';
    });
    console.log('Is popup visible?', isVisible);

    // Attempt to close it
    await page.click('#popupOkBtn');
    
    await new Promise(r => setTimeout(r, 500));
    
    await browser.close();
})();
