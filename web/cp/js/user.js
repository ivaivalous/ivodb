document.getElementById('submit-resource').onclick = createResource;

var resourcesList = document.getElementById("resources");
resourcesList.addEventListener("click", manageResource, false);

function createResource(event) {
    event.preventDefault();

    var name = document.getElementById('name').value;
    var rqPath = document.getElementById('path').value;
    var body = document.getElementById('body').value;
    var headers = document.getElementById('headers').value;

    var data = new FormData();
    data.append('name', name);
    data.append('path', rqPath);
    data.append('body', body);
    data.append('headers', headers);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/new', true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }

    xhr.send(data);
}

function publishResource(resourceId, published) {
    var resourceInfo = getResourceInfo(resourceId);
    var data = new FormData();
    var xhr = new XMLHttpRequest();
    var url = published ? '/activate' : '/deactivate';

    data.append('path', resourceInfo.path);
    xhr.open('POST', url, true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }

    xhr.send(data);
}

function manageResource(event) {
    if (event.target === event.currentTarget ||
            event.target.className !== 'action') {
        return;
    }
    event.stopPropagation();
    var id = event.target.id.split("-");
    var action = id[0]; // edit/activate/deactivate/delete
    var resourceId = id[1];

    switch (action) {
        case 'edit':
            editResource(resourceId);
            break;
        case 'activate':
            activateResource(resourceId);
            break;
        case 'deactivate':
            deactivateResource(resourceId);
            break;
        case 'delete':
            deleteResource(resourceId);
            break;
    }
}

function editResource(resourceId) {
    var resourceInfo = getResourceInfo(resourceId);
    document.getElementById('name').value = resourceInfo.name;
    document.getElementById('path').value = resourceInfo.path;
    document.getElementById('body').value = resourceInfo.body;
    document.getElementById('headers').value = resourceInfo.headers;
}

function activateResource(resourceId) {
    publishResource(resourceId, true);
}

function deactivateResource(resourceId) {
    publishResource(resourceId, false);
}

function deleteResource(resourceId) {
    var xhr = new XMLHttpRequest();

    xhr.open('DELETE', '/delete/' + resourceId, true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            alert(xhr.responseText);
        }
    }

    xhr.send(null);
}

function getResourceInfo(resourceId) {
    var resourceInfo = document.getElementById('resource-info-' + resourceId);
    var name = resourceInfo.querySelectorAll("[name='name']")[0].value;
    var path = resourceInfo.querySelectorAll("[name='path']")[0].value;
    var body = resourceInfo.querySelectorAll("[name='body']")[0].value;
    var headers = resourceInfo.querySelectorAll("[name='headers']")[0].value;

    return {
        name: name,
        path: path,
        body: body,
        headers: headers
    }
}