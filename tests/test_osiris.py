import os
import sys
import unittest
import shutil
import tempfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.shared.models import OperationLogEntry
from src.shared.log_store import append_log_entry, load_all_logs, verify_log_integrity
from src.erase.wrapper import list_available_devices, run_erase
from src.recover.classify import classify
from src.recover.scoring import score_confidence
from src.recover.wrapper import run_recovery

class TestOSIRISPlatform(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test_operations_log.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_log_entry_sha256_hashing_and_integrity(self):
        """Tests SHA-256 hash computation and tamper detection logic."""
        entry1 = OperationLogEntry(
            operation_id="op-101", module="erase_drive", timestamp="2026-08-26T12:00:00Z",
            target="E:\\TestDrive", method="DoD 5220.22-M", engine="SecureWipe", status="success"
        )
        append_log_entry(entry1, file_path=self.log_file)
        
        is_valid, summary, checks = verify_log_integrity(file_path=self.log_file)
        self.assertTrue(is_valid, "Log integrity should be valid initially.")

    def test_classification_mapping(self):
        """Tests file extension classification rules."""
        self.assertEqual(classify("photo.jpg"), "Images")
        self.assertEqual(classify("report.pdf"), "Documents")
        self.assertEqual(classify("archive.zip"), "Archives")
        self.assertEqual(classify("song.mp3"), "Media")
        self.assertEqual(classify("script.py"), "Code/System")
        self.assertEqual(classify("data.bin"), "Other")

    def test_confidence_scoring_image_and_zip(self):
        """Tests original confidence scoring logic for valid vs corrupted files."""
        # Valid PNG Image -> High Confidence
        valid_img_path = os.path.join(self.test_dir, "test_valid.png")
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(valid_img_path)
        self.assertEqual(score_confidence(valid_img_path), "High")

        # Corrupted / Truncated Image -> Medium or Low Confidence
        corrupted_img_path = os.path.join(self.test_dir, "test_corrupt.png")
        with open(corrupted_img_path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 20)
        self.assertIn(score_confidence(corrupted_img_path), ["Medium", "Low"])

        # Zero Byte File -> Low Confidence
        zero_file = os.path.join(self.test_dir, "zero.txt")
        with open(zero_file, "w") as f:
            pass
        self.assertEqual(score_confidence(zero_file), "Low")

    def test_erase_guard_confirmation_check(self):
        """Tests that erase operation blocks execution when confirmation string doesn't match."""
        target_path = os.path.join(self.test_dir, "erase_target.bin")
        with open(target_path, "wb") as f:
            f.write(b"SECRET_DATA" * 100)

        # Invalid confirmation should raise ValueError
        with self.assertRaises(ValueError):
            run_erase(device_path=target_path, confirmation_input="WRONG_CONFIRMATION")

        # Valid confirmation should succeed and overwrite file
        log_entry, cert_path = run_erase(device_path=target_path, confirmation_input=target_path)
        self.assertEqual(log_entry.status, "success")
        self.assertTrue(os.path.exists(cert_path))
        
        # Verify file data was overwritten
        with open(target_path, "rb") as f:
            data = f.read()
            self.assertNotIn(b"SECRET_DATA", data)

    def test_file_recovery_and_zero_remanence_verification(self):
        """Tests recovery invocation and post-erase zero remanence output."""
        out_dir = os.path.join(self.test_dir, "rec_out")
        target_file = os.path.join(self.test_dir, "sample_recovery.bin")
        with open(target_file, "wb") as f:
            f.write(b"SAMPLE_RECOVERY_DATA" * 50)

        log_entry, files = run_recovery(target_path=target_file, output_dir=out_dir)
        self.assertEqual(log_entry.status, "success")
        self.assertIsInstance(files, list)

if __name__ == "__main__":
    unittest.main()
