def convert_to_hex(string: str):
    return string.encode('utf-8').hex()


def convert_to_string(hex_string: str):
    return bytes.fromhex(hex_string).decode('utf-8')


def has_ordinal_in_inner_witnessscript(inner_witnessscript_asm: str) -> bool:
    return "OP_IF" in inner_witnessscript_asm and convert_to_hex('ord') in inner_witnessscript_asm and \
        "OP_PUSHBYTES_13" in inner_witnessscript_asm and "OP_ENDIF" in inner_witnessscript_asm


def extract_ordinal_content_from_tx(tx_data_json: []):
    for vin in tx_data_json["vin"]:
        if "inner_witnessscript_asm" in vin and has_ordinal_in_inner_witnessscript(vin["inner_witnessscript_asm"]):
            return get_inscription_content_from_inner_witnessscript(vin["inner_witnessscript_asm"])
    return None


def get_inscription_content_from_inner_witnessscript(inner_witnessscript_asm: str) -> str:
    if has_ordinal_in_inner_witnessscript(inner_witnessscript_asm):
        return convert_to_string(inner_witnessscript_asm.split("OP_PUSHBYTES_13 ")[1].split(" OP_ENDIF")[0])


def chunk_range(start: int, end: int, chunk_size: int) -> list[tuple[int, int]]:
    return [(i, min(i + chunk_size, end)) for i in range(start, end, chunk_size)]
