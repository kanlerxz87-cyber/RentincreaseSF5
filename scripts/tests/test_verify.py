"""Synthetic fixtures only: no supplied tenant identifiers or real tenancy data."""
import csv
import io
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        (self.root / "pages").mkdir()
        self.row = {
            "id": "RULE-001", "category": "Notice", "finding": "Synthetic rule", "value": "30 days",
            "status": "verified", "source_url": "https://www.sf.gov/learn-about-rent-increases-san-francisco",
            "verified_at": "2020-01-01", "notes": "Synthetic fixture; official domain used for structure only.",
        }
        self.write_csv([self.row])
        self.write_site()

    def tearDown(self):
        self.temp.cleanup()

    def write_csv(self, rows):
        fields = list(self.row)
        if rows:
            fields = list(dict.fromkeys(k for row in rows for k in row))
        with (self.root / "data" / "rules.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def write_site(self, row_html=None):
        if row_html is None:
            row_html = '<tr data-row-id="RULE-001"><td>Synthetic rule</td><td>30 days</td><td><a href="https://www.sf.gov/learn-about-rent-increases-san-francisco">Official source</a></td></tr>'
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Synthetic test"><title>Synthetic site</title></head><body><nav><a href="index.html">Home</a><a href="pages/flagged.html">Flags</a></nav><main><h1>Synthetic site</h1><table><tr><th>Finding</th><th>Value</th><th>Source</th></tr>{row_html}</table></main></body></html>'''
        (self.root / "index.html").write_text(page, encoding="utf-8")
        (self.root / "pages" / "flagged.html").write_text('<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Synthetic flags"><title>Flagged for Review</title></head><body><nav><a href="../index.html">Home</a></nav><main><h1>Flagged for Review</h1><p id="F-001">Synthetic flag.</p><a href="https://www.sf.gov/rent-board-housing-inventory">Official context</a></main></body></html>', encoding="utf-8")

    def audit(self, **kwargs):
        kwargs.setdefault("sensitive", ["Synthetic Privateperson"])
        kwargs.setdefault("strict", False)
        kwargs.setdefault("require_sensitive", True)
        return verify.Audit(self.root, **kwargs).run()

    def codes(self, report):
        return {i["code"] for i in report["issues"]}

    def test_valid_fixture_passes_structural_checks(self):
        report = self.audit()
        self.assertTrue(report["passed"], report["issues"])
        self.assertEqual(report["counts"]["data_rows"], 1)
        self.assertEqual(report["counts"]["html_data_rows"], 1)

    def test_missing_official_row_link_fails(self):
        self.write_site('<tr data-row-id="RULE-001"><td>Synthetic rule</td><td>30 days</td><td>No link</td></tr>')
        report = self.audit()
        self.assertFalse(report["passed"])
        self.assertIn("ROW_SOURCE", self.codes(report))

    def test_unofficial_row_link_fails(self):
        self.write_site('<tr data-row-id="RULE-001"><td>Rule</td><td><a href="https://sf.gov.example.com/notice">Blog</a></td></tr>')
        self.row["source_url"] = "https://sf.gov.example.com/notice"
        self.write_csv([self.row])
        self.assertIn("SOURCE_OFFICIAL", self.codes(self.audit()))

    def test_unverified_value_must_be_blank_and_flagged(self):
        self.row.update(status="unverified", value="presumed value", verified_at="", notes="Missing evidence; see F-001", flag_id="F-001")
        self.write_csv([self.row])
        self.write_site('<tr data-row-id="RULE-001" data-status="unverified"><td>Unverified</td><td></td><td><a href="https://www.sf.gov/rent-board-housing-inventory">Context</a> <a href="pages/flagged.html#F-001">Review</a></td></tr>')
        self.assertIn("UNVERIFIED_VALUE", self.codes(self.audit()))

    def test_blank_unverified_with_source_and_flag_passes(self):
        self.row.update(status="unverified", value="", verified_at="", notes="Not confirmed; see F-001", flag_id="F-001")
        self.write_csv([self.row])
        self.write_site('<tr data-row-id="RULE-001" data-status="unverified"><td>Unverified</td><td></td><td><a href="https://www.sf.gov/rent-board-housing-inventory">Context</a> <a href="pages/flagged.html#F-001">Review</a></td></tr>')
        report = self.audit()
        self.assertTrue(report["passed"], report["issues"])

    def test_owner_report_is_not_government_verified(self):
        self.row.update(status="owner-reported", value="", owner_reported_value="$1,000.00", verified_at="", notes="Owner input only; F-001", flag_id="F-001")
        self.write_csv([self.row])
        self.write_site('<tr data-row-id="RULE-001" data-status="owner-reported"><td>Owner-reported</td><td>$1,000.00</td><td><a href="https://www.sf.gov/rent-board-housing-inventory">Context</a> <a href="pages/flagged.html#F-001">Review</a></td></tr>')
        report = self.audit()
        self.assertTrue(report["passed"], report["issues"])

    def test_missing_retrieval_date_fails(self):
        self.row["verified_at"] = ""
        self.write_csv([self.row])
        self.assertIn("VERIFIED_DATE", self.codes(self.audit()))

    def test_future_retrieval_date_fails(self):
        self.row["verified_at"] = "2999-01-01"
        self.write_csv([self.row])
        self.assertIn("VERIFIED_DATE", self.codes(self.audit()))

    def test_missing_local_link_and_fragment_fail(self):
        with (self.root / "index.html").open("a") as f:
            f.write('<a href="missing.html">Missing</a><a href="pages/flagged.html#missing">Missing fragment</a>')
        codes = self.codes(self.audit())
        self.assertIn("LOCAL_LINK", codes)
        self.assertIn("LOCAL_FRAGMENT", codes)

    def test_project_base_links_resolve(self):
        with (self.root / "index.html").open("a") as f:
            f.write('<a href="/RentincreaseSF5/pages/flagged.html#F-001">Project link</a>')
        self.assertTrue(self.audit()["passed"])
        with (self.root / "index.html").open("a") as f:
            f.write('<a href="/pages/flagged.html">Wrong base</a>')
        self.assertIn("LOCAL_LINK", self.codes(self.audit()))

    def test_missing_rendered_record_fails(self):
        self.write_site('<tr><td>No record mapping</td><td><a href="https://www.sf.gov/">Official</a></td></tr>')
        self.assertIn("ROW_ID_MAPPING", self.codes(self.audit()))

    def test_duplicate_ids_fail(self):
        self.write_csv([self.row, self.row.copy()])
        self.assertIn("DUPLICATE_ROW_ID", self.codes(self.audit()))

    def test_private_term_never_appears_in_report(self):
        secret = "Synthetic Privateperson"
        (self.root / "leak.md").write_text("Do not publish " + secret, encoding="utf-8")
        report = self.audit(sensitive=[secret])
        self.assertIn("SENSITIVE_TERM", self.codes(report))
        self.assertNotIn(secret, json.dumps(report))

    def test_initial_variant_detection_without_echo(self):
        (self.root / "leak.md").write_text("Private S.P.", encoding="utf-8")
        report = self.audit(sensitive=["S P"])
        self.assertIn("SENSITIVE_TERM", self.codes(report))
        self.assertNotIn("S.P.", json.dumps(report))

    def test_missing_private_terms_cannot_strict_pass(self):
        report = self.audit(sensitive=[])
        self.assertFalse(report["passed"])
        self.assertIn("SENSITIVE_AUDIT_NOT_RUN", self.codes(report))

    def test_official_domain_spoof_rejected(self):
        for url in ["http://www.sf.gov/page", "https://sf.gov.evil.example/x", "https://www.sf.gov@evil.example/x", "https://evil.example?url=https://sf.gov", "https://codelibrary.amlegal.com/codes/other/latest/1"]:
            self.assertFalse(verify.official_source(url), url)
        for url in ["https://www.sf.gov/page", "https://sf.gov/page", "https://portal.sfrb.org/", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827", "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-16540"]:
            self.assertTrue(verify.official_source(url), url)

    def test_arithmetic_is_exact(self):
        self.row.update(status="calculated", value="$1,016.00", notes="Synthetic: 1000 * 1.6 / 100; input provenance synthetic.", base_rent="1000", rate_percent="1.6", increase_amount="16", new_rent="1016")
        self.write_csv([self.row])
        self.assertTrue(self.audit()["passed"])
        self.row["increase_amount"] = "17"
        self.write_csv([self.row])
        self.assertIn("ARITHMETIC", self.codes(self.audit()))

    def test_aliases_and_percent_parsing(self):
        raw = {"Row ID": "X", "Verification Status": "verified", "Official Source URL": "https://www.sf.gov/", "Verified Value": "x", "Retrieved At": "2020-01-01", "Verification Notes": "fixture"}
        row = verify.normalize_row(raw)
        self.assertEqual(row["id"], "X")
        self.assertEqual(row["source_url"], "https://www.sf.gov/")
        self.assertEqual(Decimal("3995") * Decimal("1.6") / Decimal(100), Decimal("63.920"))
        self.assertEqual(Decimal("3150") * Decimal("1.6") / Decimal(100), Decimal("50.400"))

    def test_http_soft_404_is_error(self):
        class Response:
            status = 200
            url = "https://www.sf.gov/missing"
            def read(self, n): return b"<html><title>Not Found | SF.gov</title></html>"
            def __enter__(self): return self
            def __exit__(self, *args): return False
        with patch("verify.urllib.request.urlopen", return_value=Response()):
            report = self.audit(external=True)
        self.assertIn("EXTERNAL_SOFT_404", self.codes(report))
        self.assertFalse(report["passed"])

    def test_http_block_is_not_silent_success(self):
        import urllib.error
        with patch("verify.urllib.request.urlopen", side_effect=urllib.error.HTTPError("https://www.sf.gov/", 403, "Forbidden", {}, None)):
            report = self.audit(external=True, strict=True)
        self.assertIn("EXTERNAL_BLOCKED", self.codes(report))
        self.assertFalse(report["passed"])

    def test_empty_repo_is_not_a_pass(self):
        for path in sorted(self.root.rglob("*"), reverse=True):
            if path.is_file(): path.unlink()
            elif path.is_dir(): path.rmdir()
        report = self.audit()
        self.assertFalse(report["passed"])
        self.assertIn("SITE_MISSING", self.codes(report))
        self.assertIn("DATA_MISSING", self.codes(report))


if __name__ == "__main__":
    unittest.main()
