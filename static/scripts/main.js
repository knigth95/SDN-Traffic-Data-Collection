document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('start-button').addEventListener('click', function() {
        fetch('/start_network', { method: 'POST' })
        .then(response => response.json())
        .then(data => alert(data.message));
    });

    const setupScriptButton = (hostId) => {
        document.getElementById(`run-${hostId}`).addEventListener('click', function() {
            fetch(`/run_script/${hostId}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => alert(data.message));
        });
    };

    setupScriptButton('h1');
    setupScriptButton('h2');
    setupScriptButton('h3');
    setupScriptButton('h4');

    const setupFileButton = (fileId) => {
        document.getElementById(fileId).addEventListener('click', function() {
            fetch(`/get_file/${fileId}`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.content) {
                    document.querySelector('.content').textContent = data.content;
                } else {
                    alert(data.error);
                }
            });
        });
    };

    setupFileButton('file1');
    setupFileButton('file2');
    setupFileButton('file3');
    setupFileButton('file4');
});