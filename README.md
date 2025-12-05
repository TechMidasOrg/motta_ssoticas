# SSotica RPA Client Registration

Automated bot to register mock clients on the SSotica platform.

## Features
- **Multi-Execution**: Runs 10 iterations of client creation in one session.
- **Dynamic Data**: Generates unique client names and randomized phone numbers.
- **Robustness**: 
  - Handles duplicate phone fields automatically.
  - Selects the correct "Principal" radio button.
  - Retries navigation and login waiting.
- **Observation Data**: Fills detailed observation fields.

## Prerequisites
- Python 3.8+
- Playwright

## Installation

1. Clone the repository.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```sh
   playwright install
   ```

## Configuration

1. Copy `.env.example` to `.env`:
   ```sh
   cp .env.example .env
   ```
2. Edit `.env` and add your SSotica credentials.

## Usage

Run the script:
```sh
python src/main.py
```

Arguments:
- `--close`: Close the browser automatically after execution (default is to keep it open).

```sh
python src/main.py --close
```
