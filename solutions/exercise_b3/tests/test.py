import pytest

from transformers.transcript_genome_coordinates import TranscriptToGenome

class TestClass:

    @pytest.fixture(autouse=True)
    def init_tg(self):
        self.tg = TranscriptToGenome()

    def test_example_one(self):
        assert self.tg.resolve(
            gene_name='TR1',
            chromosome="CHR1",
            starting_position=3,
            cigar="8M7D6M2I2M11D7M",
            query_position=4
        )\
        == 7

    def test_example_two(self):
        assert self.tg.resolve(
            gene_name='TR1',
            chromosome="CHR1",
            starting_position=3,
            cigar="8M7D6M2I2M11D7M",
            query_position=13
        )\
        == 23

    def test_example_three(self):
        assert self.tg.resolve(
            gene_name='TR2',
            chromosome="CHR2",
            starting_position=10,
            cigar="20M",
            query_position=0
        )\
        == 10

    def test_example_four(self):
        assert self.tg.resolve(
            gene_name='TR2',
            chromosome="CHR2",
            starting_position=10,
            cigar="20M",
            query_position=10
        )\
        == 20