const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', error => console.log('BROWSER JS ERROR:', error.message));

    // Navigating
    await page.goto('http://127.0.0.1:5500/frontend/join.html', { waitUntil: 'networkidle0' });

    console.log('Typing into form...');
    await page.type('input[name="full_name"]', 'Puppet');
    await page.type('input[name="email"]', 'puppet@example.com');
    await page.select('select[name="role"]', 'Frontend Developer');
    await page.type('textarea[name="message"]', 'Test message here');

    console.log('Clicking Submit button...');
    await page.click('.submit-btn');

    // Wait a bit to see if page reloads or shows popup
    await new Promise(r => setTimeout(r, 2000));
    
    // Check URL to see if it navigated
    console.log('Current URL after submit:', page.url());

    // Check if popup is visible
    const isVisible = await page.evaluate(() => {
        const popup = document.querySelector('.xstn-popup-overlay.active');
        return popup ? true : false;
    });
    console.log('Popup is visible:', isVisible);

    await browser.close();
})();
