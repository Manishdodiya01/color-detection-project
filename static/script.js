document.addEventListener('DOMContentLoaded', () => {
    const image = document.getElementById('color-image');
    const output = document.getElementById('color-output');

    image.addEventListener('mousemove', (event) => {
        const rect = image.getBoundingClientRect();
        const x = Math.floor(event.clientX - rect.left);
        const y = Math.floor(event.clientY - rect.top);

        fetch('/detect-color', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ x, y })
        })
            .then(response => response.json())
            .then(data => {
                output.textContent = `Detected Color: ${data.color}`;
            })
            .catch(error => {
                output.textContent = "Error detecting color.";
                console.error(error);
            });
    });
});
