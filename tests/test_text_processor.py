from tts_util.core.text_processor import TextProcessor


def test_multiline_and_hyphenated_sentence():
    processor = TextProcessor()
    text = (
        "THEOREM 2. Let M be an inductive inference machine and let S be the set\r\n"
        "of all partial recursive functions that M can identify by effective enumeration.\n"
        "Then there is a machine 2f/l uniform in M that can identify (by arbitrary enumera-\r"
        "tion) every f ~ S. Furthermore, ~ is order independent.\r\n"
        "Proof.\n"
        "We design a machine 37/with the property that whenever it is fed\r"
        "an enumeration f off ~ S, it looks for a sequence 6 with the properties of the\n"
        "lemma and then converges to M[6]:\r\n"
        "First let A be a subset of (N × N) k3 {,}. Let Z A ~ {6 ~Z ] each a i in 6\n"
        "belongs to A}. Note that if A C A' then Z A C_\r"
        "Z A, and if A is finite, so is Z A "
    )
    expected = [
        "THEOREM 2.",
        "Let M be an inductive inference machine and let S be the set of all partial recursive functions that M can identify by effective enumeration.",
        "Then there is a machine 2f/l uniform in M that can identify (by arbitrary enumera-tion) every f ~ S. Furthermore, ~ is order independent.",
        "Proof.",
        "We design a machine 37/with the property that whenever it is fedan enumeration f off ~ S, it looks for a sequence 6 with the properties of the lemma and then converges to M[6]: First let A be a subset of (N times N) k3 {,}.",
        "Let Z A ~ {6 ~Z ] each a i in 6 belongs to A}.",
        "Note that if A C A' then Z A C_Z A, and if A is finite, so is Z A",
    ]
    processed = processor._process_text(text)
    assert "enumeration" in processed
    sentences = processor._tokenize_sentences(processed)
    print("expected:", expected)
    print("sentences:", sentences)
    assert sentences == expected


def test_process_text_applies_replacements_and_strips():
    assert TextProcessor()._process_text("  \\displaystyle x ∈ A  ") == "x in A"


def test_tokenize_sentences_splits_on_punctuation_whitespace():
    processor = TextProcessor()
    text = "Hello world. This is a test! Is it split? Yes."
    expected = ["Hello world.", "This is a test!", "Is it split?", "Yes."]
    assert processor._tokenize_sentences(text) == expected


def test_tokenize_sentences_handles_common_abbreviations():
    processor = TextProcessor()
    text = "Dr. Smith wrote it. He sent it."
    expected = ["Dr. Smith wrote it.", "He sent it."]
    assert processor._tokenize_sentences(text) == expected


def test_default_replacements_load():
    processor = TextProcessor()
    mapping = dict(processor.pattern_replacements)
    assert mapping["\\displaystyle"] == ""
    assert mapping["∈"] == "in"


def test_tokenize_sentences_empty_or_whitespace_returns_empty_list():
    processor = TextProcessor()
    assert processor._tokenize_sentences("") == []
    assert processor._tokenize_sentences("   ") == []


def test_to_sentences_processes_and_tokenizes():
    assert TextProcessor().to_sentences(" x ∈ U.S.A. Test. ") == ["x in U.S.A. Test."]


def test_segmenter_is_constructed_once_and_reused(monkeypatch):
    created = []

    class FakeSegmenter:
        def segment(self, text):
            return [text]

    def fake_segmenter_ctor(*, language):
        assert language == "en"
        segmenter = FakeSegmenter()
        created.append(segmenter)
        return segmenter

    monkeypatch.setattr("tts_util.core.text_processor.pysbd.Segmenter", fake_segmenter_ctor)

    processor = TextProcessor()
    assert processor._tokenize_sentences("One.") == ["One."]
    assert processor._tokenize_sentences("Two.") == ["Two."]
    assert len(created) == 1
