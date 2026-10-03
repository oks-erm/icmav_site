"""Create private local credentials without printing secrets or overwriting files."""
import argparse
from pathlib import Path
import os
import secrets
import bcrypt
from cryptography.fernet import Fernet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend-dir', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    backend = args.backend_dir.resolve()
    state = backend.parent / '.local-state'
    env_file = backend / '.env'
    login_file = state / 'admin-login.txt'
    if env_file.exists() or login_file.exists():
        parser.error('Existing credentials found; refusing to overwrite them.')
    os.umask(0o077)
    backend.mkdir(parents=True, exist_ok=True)
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    password = secrets.token_urlsafe(32)
    values = {
        'ADMIN_USERNAME': 'admin',
        'ADMIN_PASSWORD_HASH': bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode(),
        'JWT_SECRET': secrets.token_urlsafe(64),
        'JWT_EXPIRE_MINUTES': '120',
        'SETTINGS_ENCRYPTION_KEY': Fernet.generate_key().decode(),
        'ICMAV_DATA_DIR': str(state / 'data'),
        'CORS_ORIGINS': 'http://localhost:5173,http://127.0.0.1:5173',
    }
    # Exclusive creates preserve any credentials created concurrently.
    with env_file.open('x', encoding='utf-8') as output:
        for key, value in values.items():
            # dotenv single-quoted strings escape literal quote/backslash characters.
            escaped = value.replace('\\', '\\\\').replace("'", "\\'")
            output.write(f"{key}='{escaped}'\n")
    with login_file.open('x', encoding='utf-8') as output:
        output.write(f'Local backend administrator (not deployed)\nUsername: admin\nPassword: {password}\n')
    print(f'Created private environment: {env_file}')
    print(f'Created private administrator login file: {login_file}')
    print('Back up the environment privately; losing SETTINGS_ENCRYPTION_KEY loses access to stored payment credentials.')


if __name__ == '__main__':
    main()
