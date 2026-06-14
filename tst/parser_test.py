import pytest
from src.parser import Parser

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def parser():
    """Fournit un Parser vierge à chaque test."""
    return Parser()

@pytest.fixture
def valid_line():
    """Ligne de log complète et valide."""
    return "2024-01-15 08:23:11 INFO  UserService    Login successful for user=alice latency=142ms"

@pytest.fixture
def sample_log_file(tmp_path):
    """Crée un fichier de log temporaire avec 3 lignes dont 1 invalide."""
    content = (
        "2024-01-15 08:23:11 INFO  UserService    Login successful for user=alice latency=142ms\n"
        "2024-01-15 08:23:45 ERROR DatabaseService Connection timeout latency=3200ms\n"
        "cette ligne est invalide\n"
    )
    log_file = tmp_path / "app.txt"
    log_file.write_text(content)
    return log_file

# ── Tests ─────────────────────────────────────────────────────────────────────

def test_parse_line_valid(parser, valid_line):
    """Cas nominal : tous les champs sont extraits correctement."""
    entry = parser.parse_line(valid_line)

    assert entry is not None
    assert entry["timestamp"]  == "2024-01-15 08:23:11"
    assert entry["level"]      == "INFO"
    assert entry["service"]    == "UserService"
    assert entry["user"]       == "alice"
    assert entry["latency_ms"] == 142

def test_parse_line_level_normalized(parser, valid_line):
    """Le level doit toujours être en majuscules."""
    line = valid_line.replace("INFO", "info")
    entry = parser.parse_line(line)

    assert entry["level"] == "INFO"  # normalisé par .upper()

def test_parse_line_no_user(parser):
    """Une ligne sans user= doit avoir user=None."""
    line = "2024-01-15 08:23:45 ERROR DatabaseService Connection timeout latency=3200ms"
    entry = parser.parse_line(line)

    assert entry is not None
    assert entry["user"] is None
    assert entry["latency_ms"] == 3200

def test_parse_line_no_latency(parser):
    """Une ligne sans latency= doit avoir latency_ms=None."""
    line = "2024-01-15 08:23:45 WARNING ApiGateway Rate limit exceeded for user=bob"
    entry = parser.parse_line(line)

    assert entry is not None
    assert entry["latency_ms"] is None
    assert entry["user"] == "bob"

def test_parse_line_empty(parser):
    """Une ligne vide doit retourner None."""
    assert parser.parse_line("") is None

def test_parse_line_malformed(parser):
    """Une ligne sans timestamp valide doit retourner None."""
    assert parser.parse_line("cette ligne est invalide") is None

# ── Tests parse_file ───────────────────────────────────────────────────────────

def test_parse_file_count(parser, sample_log_file):
    """parse_file doit retourner le nombre de lignes valides parsées."""
    count = parser.parse_file(str(sample_log_file))

    assert count == 2  # 3 lignes dont 1 invalide

def test_parse_file_entries_populated(parser, sample_log_file):
    """Après parse_file, get_entries() doit contenir les entrées."""
    parser.parse_file(str(sample_log_file))
    entries = parser.get_entries()

    assert len(entries) == 2
    assert entries[0]["service"] == "UserService"
    assert entries[1]["level"]   == "ERROR"

def test_parse_file_twice(parser, sample_log_file):
    """Appeler parse_file deux fois doit écraser les entrées."""
    parser.parse_file(str(sample_log_file))
    parser.parse_file(str(sample_log_file))

    assert len(parser.get_entries()) == 2  # 2 lignes × 1 fichier