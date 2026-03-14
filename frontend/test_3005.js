const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', error => console.log('BROWSER JS ERROR:', error.message));

    // Navigating to simple python server port
    await page.goto('http://127.0.0.1:3005/join.html', { waitUntil: 'domcontentloaded' });

    console.log('Typing into form...');
    await page.type('input[name="full_name"]', 'Puppet');
    await page.type('input[name="email"]', 'puppet@example.com');
    await page.select('select[name="role"]', 'Frontend Developer');
    await page.type('textarea[name="message"]', 'Test message here');

    console.log('Clicking Submit button...');
    await page.click('.submit-btn');

    await new Promise(r => setTimeout(r, 2000));
    console.log('Final URL:', page.url());

    await browser.close();
})();
