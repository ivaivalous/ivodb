document.getElementById('submit-resource').onclick = createResource;

function createResource(event) {
    event.preventDefault();

    var name = document.getElementById('name').value;
    var rqPath = document.getElementById('path').value;
    var body = document.getElementById('body').value;

    var data = new FormData();
    data.append('name', name);
    data.append('path', rqPath);
    data.append('body', body);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/new', true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }

    xhr.send(data);
}