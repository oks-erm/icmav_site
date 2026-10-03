import importlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cryptography.fernet import Fernet
from sqlmodel import SQLModel, Session, create_engine, select
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models import AppSetting
from app.crud import get_setting, upsert_setting, migrate_secret_settings


class SecretStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.engine = create_engine('sqlite:///' + str(Path(self.temp.name)/'test.db'))
        SQLModel.metadata.create_all(self.engine)
        self.env = patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': Fernet.generate_key().decode()})
        self.env.start()

    def tearDown(self):
        self.engine.dispose()
        self.env.stop()
        self.temp.cleanup()

    def test_gateway_secret_is_encrypted_and_read_does_not_flush_plaintext(self):
        secret = 'test-only-merchant-credential'
        with Session(self.engine) as session:
            value = {'mbway_key': secret, 'api_base': 'https://api.ifthenpay.com/spg/payment'}
            saved = upsert_setting(session, 'ifthenpay_config', json.dumps(value))
            self.assertEqual(json.loads(saved.value)['mbway_key'], secret)
            raw = session.exec(select(AppSetting)).one()
            self.assertNotIn(secret, raw.value)
            result = get_setting(session, 'ifthenpay_config')
            self.assertEqual(json.loads(result.value)['mbway_key'], secret)
            upsert_setting(session, 'welcome', 'public content')
            session.expire_all()
            raw = session.exec(select(AppSetting).where(AppSetting.key=='ifthenpay_config')).one()
            self.assertNotIn(secret, raw.value)

    def test_missing_key_cannot_persist_gateway_secrets(self):
        with patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': ''}):
            with Session(self.engine) as session:
                with self.assertRaises(RuntimeError):
                    upsert_setting(session, 'sibs_config', json.dumps({'mbway_key': 'test-credential'}))
                self.assertEqual(session.exec(select(AppSetting)).all(), [])

    def test_all_legacy_secret_aliases_are_encrypted(self):
        aliases = ['ifthenpay_mbway_key', 'sibs_client_id', 'sibs_client_secret', 'sibs_bearer_token']
        with Session(self.engine) as session:
            for field in aliases:
                secret = 'test-' + field
                saved = upsert_setting(session, 'sibs_config', json.dumps({field: secret}))
                self.assertEqual(json.loads(saved.value)[field], secret)
                self.assertNotIn(secret, session.exec(select(AppSetting)).one().value)

    def test_wrong_key_never_returns_ciphertext_as_a_credential(self):
        with Session(self.engine) as session:
            upsert_setting(session, 'ifthenpay_config', json.dumps({'mbway_key': 'test-credential'}))
            with patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': Fernet.generate_key().decode()}):
                with self.assertRaises(RuntimeError):
                    get_setting(session, 'ifthenpay_config')

    def test_public_settings_do_not_require_encryption_key(self):
        with patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': ''}):
            with Session(self.engine) as session:
                self.assertEqual(upsert_setting(session, 'welcome', 'public content').value, 'public content')

    def test_legacy_migration_preserves_fields_and_is_idempotent(self):
        with Session(self.engine) as session:
            session.add(AppSetting(key='sibs_config', value=json.dumps({
                'mbway_key': 'legacy-test-key', 'default_email': 'test@example.invalid'})))
            session.commit()
            migrate_secret_settings(session)
            first = session.exec(select(AppSetting)).one().value
            self.assertNotIn('legacy-test-key', first)
            migrate_secret_settings(session)
            self.assertEqual(session.exec(select(AppSetting)).one().value, first)
            restored = json.loads(get_setting(session, 'sibs_config').value)
            self.assertEqual(restored['mbway_key'], 'legacy-test-key')
            self.assertEqual(restored['default_email'], 'test@example.invalid')

    def test_legacy_migration_without_key_preserves_original_record(self):
        with Session(self.engine) as session:
            original = json.dumps({'mbway_key': 'legacy-test-key'})
            session.add(AppSetting(key='sibs_config', value=original))
            session.commit()
            with patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': ''}):
                with self.assertRaises(RuntimeError):
                    migrate_secret_settings(session)
            session.rollback()
            self.assertEqual(session.exec(select(AppSetting)).one().value, original)


if __name__ == '__main__': unittest.main()
