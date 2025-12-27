# Google Drive API Setup Instructions

## Step 1: Create Google Cloud Project and Enable Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

## Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add your email as a test user
   - Click "Save and Continue" through the scopes and test users sections
4. Back in Credentials, click "Create Credentials" > "OAuth client ID"
5. Choose "Desktop app" as the application type
6. Name it (e.g., "Drive Image Downloader")
7. Click "Create"
8. Download the JSON file by clicking the download icon
9. **IMPORTANT**: Rename the downloaded file to `credentials.json` and place it in this directory:
   ```
   /Users/sndyy/prime-optical-vision/credentials.json
   ```

## Step 3: Run the Download Script

**NOTE**: The image download scripts have been removed from this project as they were only needed for initial setup. If you need to re-download images, you can retrieve the script from the project's git history.

~~Once you have the `credentials.json` file in place, run:~~

~~```bash
cd /Users/sndyy/prime-optical-vision
./venv/bin/python download_drive_images.py
```~~

~~The script will:~~
~~1. Open a browser window for you to authenticate with Google~~
~~2. Ask you to grant permission to read your Google Drive files~~
~~3. Save the authentication token for future use~~
~~4. Download all images from the 27 folders to `downloaded_images/` directory~~

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth credentials file
- Rename it to exactly `credentials.json`
- Place it in `/Users/sndyy/prime-optical-vision/`

### "Access blocked: This app's request is invalid"
- Make sure you configured the OAuth consent screen
- Add your email as a test user in the OAuth consent screen

### "The user did not grant your application the requested scopes"
- Make sure you're using the correct Google account
- Try deleting `token.json` and re-authenticating

## What Gets Downloaded

The script will create a directory structure like this:
```
downloaded_images/
├── 1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── 2/
│   ├── image1.jpg
│   └── ...
├── 3/
└── ...
```

Each folder from Google Drive will have its own subdirectory with all images downloaded.
