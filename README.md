# WarpShare

#

WarpShare lets someone share files directly from their own device and give another person a link to browse, download, and work with those files immediately.

It is different from GitHub forks.
With WarpShare, they do not need to publish anything first, set up a repository, or add people as collaborators. They just share a direct link to files on their device. While you work, they can see the output directly.

## Install

Download the latest release here:
https://github.com/hallofcodes/WarpShare/releases/latest

Built executables:

- `warpshare-linux-amd64`
- `warpshare-linux-musl-aarch64`
- `warpshare-windows-amd64.exe`

Quick install with script:

```bash
curl -fsSL https://raw.githubusercontent.com/hallofcodes/WarpShare/master/install.sh | bash
```

If `curl` is not available:

```bash
wget -qO- https://raw.githubusercontent.com/hallofcodes/WarpShare/master/install.sh | bash
```

Manual install

Linux x64:

```bash
curl -L https://github.com/hallofcodes/WarpShare/releases/latest/download/warpshare-linux-amd64 -o warpshare
chmod +x warpshare
sudo mv warpshare /usr/local/bin/warpshare
warpshare
```

Linux ARM64 musl:

```bash
curl -L https://github.com/hallofcodes/WarpShare/releases/latest/download/warpshare-linux-musl-aarch64 -o warpshare
chmod +x warpshare
sudo mv warpshare /usr/local/bin/warpshare
warpshare
```

Windows:

```powershell
Invoke-WebRequest -Uri https://github.com/hallofcodes/WarpShare/releases/latest/download/warpshare-windows-amd64.exe -OutFile warpshare.exe
Start-Process .\warpshare.exe
```

To keep it as a global command on Windows, move it to a folder already in your `Path`, or create one:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\bin" | Out-Null
Move-Item .\warpshare.exe "$env:USERPROFILE\bin\warpshare.exe" -Force
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\bin", "User")
```

## Use

Start WarpShare in the current folder:

```bash
warpshare local
```

Share a specific folder on your local network:

```bash
warpshare local /path/to/folder
```

Use a custom port:

```bash
warpshare local /path/to/folder --port 8080
```

Share over the internet:

```bash
warpshare remote
```

Remote share with a specific folder:

```bash
warpshare remote /path/to/folder
```

After it starts:

- choose the link WarpShare gives you
- send it to the other person
- they open it in the browser and work from there

## Browser actions

From the web interface, they can:

- browse folders
- download files
- create folders
- create files
- rename items
- delete items

## Why people use it

- direct access to files on a real device
- no repository setup
- no fork workflow
- no collaborator setup
- fast sharing and review
- useful when files should stay on the owner’s machine
