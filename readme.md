# flickr-email-osint

A specialized OSINT automation tool designed for deep enumeration of Flickr user entities using email vectors. This utility leverages undocumented API endpoints to resolve email addresses to NSIDs (user IDs) and extracts comprehensive profile metadata and high-resolution digital assets.

To obtain the tokens, you need an account, upload an image to /photos/upload/, and then, in the "Add People" menu, enter your account email address or another valid email address from another user. With DevTools open, in the Networks section, look for the server response that begins with "flickr.com/services/rest..." and then go to the Payloads section; there you will find the keys and temporary tokens.

![Main Interface](Captura%20de%20pantalla%202025-12-11%200217261.png)

## 🚀 Capabilities

*   **Email-to-NSID Resolution**: Reverse looks up target emails to identify persistent unique identifiers (NSID) using Flickr's legacy API endpoints.
*   **Account Information Retrieval**: Retrieves comprehensive account details including:
    *   `Real Name` & `Username`
    *   `NSID` (User ID) & `DBID`
    *   `Date Created`
    *   `Description` & `Location`
    *   `Path Alias`
    *   **Status Indicators**: `Is Pro`, `Is Deleted`, `Is Ad Free`, `Gift Eligible`
    *   **Statistics**: `Photos Count`, `Has Stats`
    *   **URLs**: `Profile URL`, `Photos URL`, `Mobile URL`
*   **Asset Retrieval**: Automatically fetches and downloads high-fidelity user assets:
    *   Profile avatars (retrieves `retina` quality 400x400 if available)
    *   Profile header banners (cover photos) in maximum resolution.
*   **Robust Authentication**: Supports session-based authentication via `api_key`, `auth_hash`, and `secret`.
*   **Internationalization (i18n)**: Native support for English and Spanish locales.

## 🛠️ Prerequisites

*   Python 3.8+
*   `requests` library

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/gn0sys11root/flickr-email-osint.git
    cd flickr-email-osint
    ```

2.  Install dependencies:
    ```bash
    pip install requests
    ```

## ⚙️ Configuration

The tool requires valid Flickr API session tokens (`api_key`, `auth_hash`, `secret`). These can be extracted from a logged-in session on Flickr (inspecting network traffic).

You can supply credentials in two ways:
1.  **Runtime Input**: Paste them directly when prompted.
2.  **File-based**: Create a `keys.txt` file in the root directory:

```ini
api_key=your_api_key_here
auth_hash=your_auth_hash_here
secret=your_secret_here
```

## 💻 Usage

Execute the script via terminal:

```bash
python flickr_osint.py
```

Follow the interactive prompts to select language, input target email, and authentication method.

## 📄 License
MIT License
