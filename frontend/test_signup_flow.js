const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    
    // Catch console logs
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));

    // 1. Visit signup exactly as live server
    await page.goto('http://127.0.0.1:5500/frontend/signup.html', { waitUntil: 'networkidle0' });

    console.log('Typing into form...');
    
    // 2. Fill the form to pass all client side checks
    await page.type('input[name="username"]', 'puppet_test99');
    await page.type('input[name="first_name"]', 'Puppet');
    await page.type('input[name="last_name"]', 'Tester');
    await page.type('input[name="email"]', 'puppet99@example.com');
    await page.type('input[name="password"]', 'StrongPassw0rd!');
    await page.type('input[name="confirmPassword"]', 'StrongPassw0rd!');

    console.log('Clicking JOIN XTN...');
    // 3. Click Submit
    await page.click('.submit-btn');

    // 4. Wait to see if popup overlay appears
    console.log('Waiting for .xstn-popup-overlay.active...');
    try {
        await page.waitForSelector('.xstn-popup-overlay.active', { timeout: 3000 });
        console.log('SUCCESS: Popup IS visibly active on the page!');
        await page.screenshot({ path: 'popup_final.png' });
    } catch(e) {
        console.log('FAILED: Popup did not appear after 3 seconds.');
        await page.screenshot({ path: 'popup_fail.png' });
    }

    await browser.close();
})();
