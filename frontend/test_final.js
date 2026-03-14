const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', error => console.log('BROWSER JS ERROR:', error.message));

    // Wait for networkidle2 to ensure scripts are done loading
    await page.goto('http://127.0.0.1:3005/join.html', { waitUntil: 'networkidle2' });

    console.log('Typing into form...');
    await page.type('input[name="full_name"]', 'Puppet');
    await page.type('input[name="email"]', 'puppet@example.com');
    await page.type('textarea[name="message"]', 'Test message here');

    console.log('Clicking Submit button...');
    await page.click('.submit-btn');

    await new Promise(r => setTimeout(r, 2000));
    console.log('Final URL:', page.url());

    await browser.close();
})();
