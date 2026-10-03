from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from dotenv import dotenv_values
import bcrypt
from cryptography.fernet import Fernet


class SecretSetupTests(unittest.TestCase):
    def test_private_credentials_are_valid_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            backend = Path(folder) / 'backend'
            script = Path(__file__).resolve().parents[1] / 'scripts/init_secrets.py'
            command = [sys.executable, str(script), '--backend-dir', str(backend)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            env = backend / '.env'
            login = backend.parent / '.local-state/admin-login.txt'
            env_bytes, login_bytes = env.read_bytes(), login.read_bytes()
            self.assertEqual(env.stat().st_mode & 0o777, 0o600)
            self.assertEqual(login.stat().st_mode & 0o777, 0o600)
            config = dotenv_values(env)
            password = login.read_text().split('Password: ',1)[1].strip()
            self.assertTrue(bcrypt.checkpw(password.encode(), config['ADMIN_PASSWORD_HASH'].encode()))
            self.assertGreaterEqual(len(config['JWT_SECRET']), 64)
            Fernet(config['SETTINGS_ENCRYPTION_KEY'].encode())
            for secret in [password, config['JWT_SECRET'], config['SETTINGS_ENCRYPTION_KEY']]:
                self.assertNotIn(secret, first.stdout + first.stderr)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(env.read_bytes(), env_bytes)
            self.assertEqual(login.read_bytes(), login_bytes)


if __name__ == '__main__': unittest.main()
