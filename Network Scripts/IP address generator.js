function generateRandomIP() {
    return (Math.floor(Math.random() * 256) + 1) + "." +
        (Math.floor(Math.random() * 256)) + "." +
        (Math.floor(Math.random() * 256)) + "." +
        (Math.floor(Math.random() * 256));
}

var ip = generateRandomIP();
console.log(ip);