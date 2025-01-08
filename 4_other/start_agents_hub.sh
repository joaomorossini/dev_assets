#!/bin/bash

# Start Docker Desktop
echo "Starting Docker Desktop..."
open -a "Docker"

# Open Evolution Manager in a new Brave tab with the specified URL
echo "Opening Evolution Manager in Brave Browser..."
open -a "Brave Browser" "https://wpp-prod.cogmo.com.br/manager/morossini_secretaria"

# Open a new Terminal window to run Ngrok command
echo "Opening new Terminal window to run 'ngrok http 5002'..."
osascript <<EOF
tell application "Terminal"
    do script "/Applications/ngrok http 5002"
    activate
end tell
EOF

# Wait a few seconds to ensure ngrok has started and generated a forwarding URL
sleep 5

# Extract the Ngrok forwarding URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -Eo 'https://[a-zA-Z0-9.-]+\.ngrok-free\.app')

if [ -z "$NGROK_URL" ]; then
    echo "Ngrok URL could not be found. Make sure Ngrok is running and try again."
    exit 1
fi

# Copy the URL to the clipboard
echo "$NGROK_URL" | pbcopy
echo "Ngrok URL copied to clipboard: $NGROK_URL"

# Use AppleScript to paste the URL into the Evolution Manager webhook URL field
osascript <<EOF
tell application "Brave Browser"
    activate
    tell window 1
        set tabFound to false
        repeat with t in tabs
            if (URL of t) contains "wpp-prod.cogmo.com.br/manager/morossini_secretaria" then
                set current tab to t
                set tabFound to true
                exit repeat
            end if
        end repeat

        if tabFound then
            delay 1  -- Wait for the page to be fully active
            tell application "System Events"
                keystroke "v" using {command down}  -- Paste the URL
            end tell
        else
            display dialog "Could not find the Evolution Manager tab. Please open it manually."
        end if
    end tell
end tell
EOF

echo "All applications have been launched, and the Ngrok URL has been pasted into the Evolution Manager webhook field."
