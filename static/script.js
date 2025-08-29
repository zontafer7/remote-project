function sendKey(key) {
    fetch(`/press/${key}`)
        .then(response => response.text());
}