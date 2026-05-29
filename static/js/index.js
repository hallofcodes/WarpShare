const files = document.getElementById("files");
function view(layout) {
    const gridbtn = document.querySelector(".grid");
    const listbtn = document.querySelector(".list");
    gridbtn.classList.toggle('active', layout === 'grid');
    files.classList.toggle('grid-view', layout === 'grid');
    listbtn.classList.toggle('active', layout === 'list');
    files.classList.toggle('list-view', layout === 'list');
}

let currentDir = {
    name: "Projects",
    files: [
        {
            name: "Class",
            files: [["Projects.zip", 45200], ["photo.jpg", 3800], ["notes.md", 12], ["main.py", 8.1], ["index.html", 24]]
        },
        ["Projects.zip", 45200],
        ["photo.jpg", 3800],
        ["notes.md", 12],
        ["main.py", 8.1],
        ["index.html", 24],
        ["demo-video.mp4", 128000],
        ["report.pdf", 2200],
    ]
};

document.getElementById("items").innerText = `${currentDir.files.length} items`;

const fragment = document.createDocumentFragment();

for (file of currentDir.files) {
    const fileIcon = document.createElement("div");
    fileIcon.className = 'icon';
    fileIcon.addEventListener('contextmenu', (e) => {
        const m = document.getElementById("menu");
        e.preventDefault();
        m.style.top = e.clientY + 'px';
        m.style.left = e.clientX + 'px';
        m.style.display = "flex";
    }, 'false')
    if (Array.isArray(file)) {
        fileIcon.innerHTML = `
            <div class="buttons">
                <button>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="M480-336 288-528l51-51 105 105v-342h72v342l105-105 51 51-192 192ZM263.72-192Q234-192 213-213.15T192-264v-72h72v72h432v-72h72v72q0 29.7-21.16 50.85Q725.68-192 695.96-192H263.72Z"/></svg>
                </button>
                <button>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="M216-216h51l375-375-51-51-375 375v51Zm-72 72v-153l498-498q11-11 23.84-16 12.83-5 27-5 14.16 0 27.16 5t24 16l51 51q11 11 16 24t5 26.54q0 14.45-5.02 27.54T795-642L297-144H144Zm600-549-51-51 51 51Zm-127.95 76.95L591-642l51 51-25.95-25.05Z"/></svg>
                </button>
                <button class='delete'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="m400-325 80-80 80 80 51-51-80-80 80-80-51-51-80 80-80-80-51 51 80 80-80 80 51 51Zm-88 181q-29.7 0-50.85-21.15Q240-186.3 240-216v-480h-48v-72h192v-48h192v48h192v72h-48v479.57Q720-186 698.85-165T648-144H312Zm336-552H312v480h336v-480Zm-336 0v480-480Z"/></svg>
                </button>
            </div>
            <div class="thumbnail">
                <span class="img">📁</span>
                <h3 class="name">${file[0]}</h3>
            </div>
            <p class="size">${(file[1] < 1000) ? `${file[1]} KB` : `${file[1] / 1000} MB`}</p>
        `;
    } else {
        fileIcon.innerHTML = `
            <div class="buttons">
                <button>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="M480-336 288-528l51-51 105 105v-342h72v342l105-105 51 51-192 192ZM263.72-192Q234-192 213-213.15T192-264v-72h72v72h432v-72h72v72q0 29.7-21.16 50.85Q725.68-192 695.96-192H263.72Z"/></svg>
                </button>
                <button>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="M216-216h51l375-375-51-51-375 375v51Zm-72 72v-153l498-498q11-11 23.84-16 12.83-5 27-5 14.16 0 27.16 5t24 16l51 51q11 11 16 24t5 26.54q0 14.45-5.02 27.54T795-642L297-144H144Zm600-549-51-51 51 51Zm-127.95 76.95L591-642l51 51-25.95-25.05Z"/></svg>
                </button>
                <button class='delete'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6b7280"><path d="m400-325 80-80 80 80 51-51-80-80 80-80-51-51-80 80-80-80-51 51 80 80-80 80 51 51Zm-88 181q-29.7 0-50.85-21.15Q240-186.3 240-216v-480h-48v-72h192v-48h192v48h192v72h-48v479.57Q720-186 698.85-165T648-144H312Zm336-552H312v480h336v-480Zm-336 0v480-480Z"/></svg>
                </button>
            </div>
            <div class="thumbnail">
                <span class="img">📁</span>
                <h3 class="name">${file.name}</h3>
            </div>
            <p class="size">${file.files.length} files</p>
        `;
    }
    fragment.appendChild(fileIcon);
}
files.appendChild(fragment);
document.body.addEventListener('click', () => {
    document.getElementById("menu").style.display = 'none';
}, 'false')