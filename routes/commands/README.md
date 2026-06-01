# File Operations API

All request and response bodies use JSON unless specified otherwise.

### 1. List Current Working Directory

- **Endpoint:** `GET /cwd`
- **Response:** (Plain text) The current working directory path.

### 2. List Files and Directories

Returns a list of items inside the specified path, indicating whether each item is a file or a directory.

- **Endpoint:** `GET /ls`
- **Query Parameters:**
   - `path` (string): The target directory path.
- **Success Response (200 OK):**
   - **Content (JSON):**
      ```json
      [
      	{
      		"name": "folder1",
      		"type": "dir"
      	},
      	{
      		"name": "file1.txt",
      		"type": "file"
      	}
      ]
      ```
- **Error Response (500 Internal Server Error):**
- **Content (Plain Text):** `Error listing files/directories: [error details]`

### 3. Copy File or Folder

- **Endpoint:** `POST /cp`
- **Request Body:**

   ```json
   {
   	"from_path": "/source/path",
   	"dest_path": "/destination/path"
   }
   ```

- **Response (Success - 200):** (Plain text) The path to the newly copied item.
- **Response (Error - 500):** (Plain text) "Error copying file/folder: <error_details>"

### 4. Move File or Folder

- **Endpoint:** `POST /mv`
- **Request Body:**

   ```json
   {
   	"from_path": "/source/path",
   	"dest_path": "/destination/path"
   }
   ```

- **Response (Success - 200):** (Plain text) The path to the moved item.
- **Response (Error - 500):** (Plain text) "Error moving file/folder: <error_details>"
