#!/usr/bin/env bash
set -euo pipefail

REPO="hallofcodes/WarpShare"
BINARY_NAME="warpshare"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
USER_BIN_DIR="${HOME:-$PWD}/.local/bin"
API_URL="https://api.github.com/repos/${REPO}/releases/latest"
RAW_BASE="https://github.com/${REPO}/releases/latest/download"

say() {
  printf '%s\n' "$*"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

fetch() {
  local url="$1"
  local out="$2"

  if need_cmd curl; then
    curl -fsSL "$url" -o "$out"
  elif need_cmd wget; then
    wget -qO "$out" "$url"
  else
    say "Error: curl or wget is required."
    exit 1
  fi
}

fetch_text() {
  local url="$1"

  if need_cmd curl; then
    curl -fsSL "$url"
  elif need_cmd wget; then
    wget -qO- "$url"
  else
    say "Error: curl or wget is required."
    exit 1
  fi
}

normalize_arch() {
  case "$1" in
    x86_64|amd64) echo "amd64" ;;
    aarch64|arm64) echo "arm64" ;;
    *) echo "$1" ;;
  esac
}

normalize_os() {
  case "$1" in
    Linux|linux) echo "linux" ;;
    Darwin|darwin) echo "darwin" ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT) echo "windows" ;;
    *) echo "unknown" ;;
  esac
}

is_musl() {
  if ldd --version 2>&1 | grep -qi musl; then
    return 0
  fi

  if [ -e /lib/ld-musl-aarch64.so.1 ] || [ -e /lib/ld-musl-x86_64.so.1 ]; then
    return 0
  fi

  return 1
}

pick_asset() {
  local os="$1"
  local arch="$2"

  if [ "$os" = "linux" ] && [ "$arch" = "amd64" ]; then
    echo "warpshare-linux-amd64"
    return 0
  fi

  if [ "$os" = "linux" ] && [ "$arch" = "arm64" ] && is_musl; then
    echo "warpshare-linux-musl-aarch64"
    return 0
  fi

  if [ "$os" = "windows" ] && [ "$arch" = "amd64" ]; then
    echo "warpshare-windows-amd64.exe"
    return 0
  fi

  return 1
}

latest_tag() {
  fetch_text "$API_URL" | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1
}

ensure_path_hint() {
  case ":${PATH}:" in
    *":${USER_BIN_DIR}:"*) ;;
    *) say "Add this to your shell profile if '${USER_BIN_DIR}' is not in PATH:" && say "export PATH=\"${USER_BIN_DIR}:\$PATH\"" ;;
  esac
}

install_binary() {
  local src="$1"
  local target_name="$2"

  chmod +x "$src"

  if [ -w "$INSTALL_DIR" ] || { [ ! -e "$INSTALL_DIR" ] && mkdir -p "$INSTALL_DIR" 2>/dev/null; }; then
    mv "$src" "${INSTALL_DIR}/${target_name}"
    say "Installed to ${INSTALL_DIR}/${target_name}"
    return 0
  fi

  if need_cmd sudo; then
    sudo mkdir -p "$INSTALL_DIR"
    sudo mv "$src" "${INSTALL_DIR}/${target_name}"
    say "Installed to ${INSTALL_DIR}/${target_name}"
    return 0
  fi

  mkdir -p "$USER_BIN_DIR"
  mv "$src" "${USER_BIN_DIR}/${target_name}"
  say "Installed to ${USER_BIN_DIR}/${target_name}"
  ensure_path_hint
}

main() {
  local os arch asset tmp_file tag
  os="$(normalize_os "$(uname -s 2>/dev/null || echo unknown)")"
  arch="$(normalize_arch "$(uname -m 2>/dev/null || echo unknown)")"

  if [ "$os" = "unknown" ]; then
    say "Unsupported operating system."
    exit 1
  fi

  if ! asset="$(pick_asset "$os" "$arch")"; then
    say "No prebuilt WarpShare binary for ${os}/${arch}."
    say "Available release assets from current workflow:"
    say "- warpshare-linux-amd64"
    say "- warpshare-linux-musl-aarch64"
    say "- warpshare-windows-amd64.exe"
    exit 1
  fi

  tag="$(latest_tag || true)"
  tmp_file="$(mktemp)"

  say "Downloading ${asset}${tag:+ (${tag})}..."
  fetch "${RAW_BASE}/${asset}" "$tmp_file"

  install_binary "$tmp_file" "$BINARY_NAME"

  say ""
  say "Run it with:"
  say "  ${BINARY_NAME} local"
  say "or"
  say "  ${BINARY_NAME} remote"
}

main "$@"
