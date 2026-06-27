const files = document.getElementById('files')
const itemsCount = document.getElementById('items')
const searchInput = document.querySelector('.search-bar input')
const breadcrumb = document.querySelector('.path')
const menu = document.getElementById('menu')
const newFolderBtn = document.querySelector('.new-folder')

let currentPath = '.'
let entries = []
let selectedEntry = null

function view(layout) {
   const gridbtn = document.querySelector('.grid')
   const listbtn = document.querySelector('.list')
   gridbtn.classList.toggle('active', layout === 'grid')
   files.classList.toggle('grid-view', layout === 'grid')
   listbtn.classList.toggle('active', layout === 'list')
   files.classList.toggle('list-view', layout === 'list')
}

const api = async (url, options = {}) => {
   const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options
   })

   if (!response.ok) throw new Error(await response.text())
   return response.headers.get('content-type')?.includes('application/json') ? response.json() : response.text()
}

const joinPath = (base, name) => (base === '.' || base === '' ? name : `${base}/${name}`)
const parentPath = path => {
   const parts = path.split('/').filter(Boolean)
   parts.pop()
   return parts.length ? parts.join('/') : '.'
}

const formatSize = size => {
   if (size === null || size === undefined) return 'Folder'
   if (size < 1024) return `${size} B`
   if (size < 1024 ** 2) return `${(size / 1024).toFixed(1)} KB`
   if (size < 1024 ** 3) return `${(size / 1024 ** 2).toFixed(1)} MB`
   return `${(size / 1024 ** 3).toFixed(1)} GB`
}

const getIconClass = entry => {
   if (entry.type === 'dir') return 'fa-solid fa-folder'

   const extension = entry.name.split('.').pop().toLowerCase()
   const iconMap = {
      zip: 'fa-solid fa-file-zipper', rar: 'fa-solid fa-file-zipper', '7z': 'fa-solid fa-file-zipper',
      jpg: 'fa-solid fa-file-image', jpeg: 'fa-solid fa-file-image', png: 'fa-solid fa-file-image', gif: 'fa-solid fa-file-image', webp: 'fa-solid fa-file-image',
      md: 'fa-brands fa-markdown', py: 'fa-brands fa-python', html: 'fa-brands fa-html5', css: 'fa-brands fa-css3-alt', js: 'fa-brands fa-js',
      mp4: 'fa-solid fa-file-video', mov: 'fa-solid fa-file-video', mkv: 'fa-solid fa-file-video',
      mp3: 'fa-solid fa-file-audio', wav: 'fa-solid fa-file-audio', pdf: 'fa-solid fa-file-pdf', txt: 'fa-solid fa-file-lines', json: 'fa-solid fa-code'
   }

   return iconMap[extension] || 'fa-solid fa-file'
}

const renderBreadcrumb = () => {
   const parts = currentPath === '.' ? [] : currentPath.split('/').filter(Boolean)
   breadcrumb.innerHTML = `<button class="crumb" data-path="."><span class="dir">Home</span></button>` + parts.map((part, index) => {
      const path = parts.slice(0, index + 1).join('/')
      return `<i class="fa-solid fa-chevron-right"></i><button class="crumb" data-path="${path}"><span class="dir">${part}</span></button>`
   }).join('')

   breadcrumb.querySelectorAll('.crumb').forEach(btn => {
      btn.addEventListener('click', () => loadFiles(btn.dataset.path))
   })
}

const actionButtons = entry => `
   <div class="buttons">
      ${entry.type === 'file' ? '<button data-action="download" aria-label="Download"><i class="fa-solid fa-download"></i></button>' : ''}
      <button data-action="rename" aria-label="Rename"><i class="fa-solid fa-pen-to-square"></i></button>
      <button class="delete" data-action="delete" aria-label="Delete"><i class="fa-solid fa-trash-can"></i></button>
   </div>
`

const renderFiles = () => {
   const query = searchInput.value.trim().toLowerCase()
   const visible = entries.filter(entry => entry.name.toLowerCase().includes(query))
   const fragment = document.createDocumentFragment()

   files.innerHTML = ''
   itemsCount.innerText = `${visible.length} item${visible.length === 1 ? '' : 's'}`

   if (currentPath !== '.') {
      visible.unshift({ name: '..', type: 'dir', size: null, path: parentPath(currentPath), isBack: true })
   }

   for (const entry of visible) {
      const card = document.createElement('div')
      const entryPath = entry.path || joinPath(currentPath, entry.name)

      card.className = `icon ${entry.type}`
      card.tabIndex = 0
      card.innerHTML = `
         ${entry.isBack ? '' : actionButtons(entry)}
         <div class="thumbnail">
            <span class="img"><i class="${entry.isBack ? 'fa-solid fa-arrow-turn-up' : getIconClass(entry)}"></i></span>
            <h3 class="name" title="${entry.name}">${entry.name}</h3>
         </div>
         <p class="size">${entry.isBack ? 'Parent folder' : formatSize(entry.size)}</p>
      `

      card.addEventListener('dblclick', () => entry.type === 'dir' && loadFiles(entryPath))
      card.addEventListener('click', e => handleAction(e, entry, entryPath))
      card.addEventListener('contextmenu', e => showMenu(e, entry, entryPath))
      fragment.appendChild(card)
   }

   files.appendChild(fragment)
}

const loadFiles = async (path = '.') => {
   files.innerHTML = '<div class="loading"><i class="fa-solid fa-spinner fa-spin"></i> Loading files...</div>'
   try {
      currentPath = path
      entries = await api(`/commands/ls?path=${encodeURIComponent(path)}`)
      entries.sort((a, b) => (a.type === b.type ? a.name.localeCompare(b.name) : a.type === 'dir' ? -1 : 1))
      renderBreadcrumb()
      renderFiles()
   } catch (error) {
      files.innerHTML = `<div class="empty-state"><i class="fa-solid fa-triangle-exclamation"></i><p>${error.message}</p></div>`
   }
}

const downloadEntry = path => {
   window.location.href = `/commands/download?path=${encodeURIComponent(path)}`
}

const renameEntry = async (entry, path) => {
   const nextName = prompt('Rename item', entry.name)
   if (!nextName || nextName === entry.name) return

   await api('/commands/mv', {
      method: 'POST',
      body: JSON.stringify({ from_path: path, dest_path: joinPath(currentPath, nextName) })
   })
   loadFiles(currentPath)
}

const deleteEntry = async (entry, path) => {
   if (!confirm(`Delete "${entry.name}"?`)) return

   await api('/commands/rm', {
      method: 'POST',
      body: JSON.stringify({ path })
   })
   loadFiles(currentPath)
}

const handleAction = (event, entry, path) => {
   const action = event.target.closest('button')?.dataset.action
   if (!action) return

   event.stopPropagation()
   if (action === 'download') downloadEntry(path)
   if (action === 'rename') renameEntry(entry, path)
   if (action === 'delete') deleteEntry(entry, path)
}

const showMenu = (event, entry, path) => {
   if (entry.isBack) return

   event.preventDefault()
   selectedEntry = { entry, path }
   menu.style.top = `${Math.min(event.clientY, window.innerHeight - 170)}px`
   menu.style.left = `${Math.min(event.clientX, window.innerWidth - 210)}px`
   menu.style.display = 'flex'
   menu.querySelector('[data-action="download"]').style.display = entry.type === 'file' ? 'flex' : 'none'
}

menu.addEventListener('click', event => {
   const action = event.target.closest('button')?.dataset.action
   if (!action || !selectedEntry) return

   if (action === 'download') downloadEntry(selectedEntry.path)
   if (action === 'rename') renameEntry(selectedEntry.entry, selectedEntry.path)
   if (action === 'delete') deleteEntry(selectedEntry.entry, selectedEntry.path)
   menu.style.display = 'none'
})

document.body.addEventListener('click', () => {
   menu.style.display = 'none'
})

searchInput.addEventListener('input', renderFiles)

newFolderBtn.addEventListener('click', async () => {
   const name = prompt('Folder name')
   if (!name) return

   await api('/commands/mkdir', {
      method: 'POST',
      body: JSON.stringify({ path: joinPath(currentPath, name) })
   })
   loadFiles(currentPath)
})

loadFiles()
