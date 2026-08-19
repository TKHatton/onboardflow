# Setting Up Your Gemini API Key

## Get Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## Set the API Key

### Option 1: Environment Variable (Recommended for Development)

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### Option 2: Create .env File

```bash
cd /home/tkhatton13/onboardflow
cat > .env << EOL
GOOGLE_API_KEY=your-api-key-here
EOL
```

## Verify It Works

```bash
python test_autonomous.py
```

You should see the agent reasoning about onboarding steps and executing tools.

## Important Notes

- The API key gives access to your Google Cloud account
- Keep it secure - don't commit it to git
- The .env file is already in .gitignore
- Free tier includes generous limits for development
