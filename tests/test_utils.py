from unittest import TestCase

from ordipool.utils.utils import convert_to_hex, has_ordinal_in_inner_witnessscript, \
    get_inscription_content_from_inner_witnessscript, chunk_range


class Test(TestCase):
    def test_convert_to_hex(self):
        string = "ord"
        hex_string = convert_to_hex(string)
        self.assertTrue(hex_string == "6f7264")

    def test_has_ordinal_in_witness_script_asm(self):
        inner_witness_script_asm = "OP_PUSHBYTES_32 b8ea323c3cf12325ea6123ce021580bee839f7e070ff7f86fa3788d48d1a31ae " \
                                   "OP_CHECKSIG OP_0 OP_IF OP_PUSHBYTES_3 6f7264 OP_PUSHBYTES_1 01 OP_PUSHBYTES_24 " \
                                   "746578742f706c61696e3b636861727365743d7574662d38 OP_0 OP_PUSHBYTES_13 " \
                                   "3830323334312e6269746d6170 OP_ENDIF"
        self.assertTrue(has_ordinal_in_inner_witnessscript(inner_witness_script_asm))

    def test_get_inscription_id_from_inner_witnessscript(self):
        inner_witness_script_asm = "OP_PUSHBYTES_32 6bf9d0831566ae4fd35e837ee22ac2eaae8cba0c833de3f076a1206b5894e692 " \
                                   "OP_CHECKSIG OP_0 OP_IF OP_PUSHBYTES_3 6f7264 OP_PUSHBYTES_1 01 OP_PUSHBYTES_24 " \
                                   "746578742f706c61696e3b636861727365743d7574662d38 OP_0 OP_PUSHBYTES_13 " \
                                   "3830333330322e6269746d6170 OP_ENDIF"
        inscription_content = get_inscription_content_from_inner_witnessscript(inner_witness_script_asm)
        self.assertTrue(inscription_content == "803302.bitmap")

    def test_chunk_range(self):
        chunked = chunk_range(0, 100, 33)
        self.assertEqual(chunked, [(0, 33), (33, 66), (66, 99), (99, 100)])
