import hashlib
from ecdsa import SECP256k1, SigningKey, VerifyingKey
from ecdsa.util import sigencode_der, sigdecode_der
import os
import json
from base58 import b58encode_check, b58decode, b58decode_check

KEYS_PATH = 'src/keys.json'


def getKeysStore() -> object:
    # init keys if there is no key pair
    if os.path.exists(KEYS_PATH) == False:
        with open(KEYS_PATH, 'w') as keys_file:
            json.dump([], keys_file, indent=2)

    #  open key pairs file
    with open(KEYS_PATH, 'r') as keys_file:
        keysStore = json.load(keys_file)

    return keysStore


def getKeys(alias: str) -> object:
    keysStore = getKeysStore()

    filtered = list(filter(lambda x: x['alias'] == alias, keysStore))
    if(any(filtered)):
        return list(filtered)[0]
    else:
        print(f"No alias '{alias}' Found!")
        return {}


def sha256d(data: str or bytes) -> str:
    """A double SHA-256 hash"""
    if (not isinstance(data, bytes)):
        data = data.encode()
    sha = hashlib.sha256(data).digest()
    return hashlib.sha256(sha).hexdigest()


def sha256(data: str or bytes) -> str:
    if (not isinstance(data, bytes)):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def pkToPkh(pk: str) -> str:
    """we only care P2PKH which begin with the number 1"""
    encoded = bytes.fromhex(pk)
    sha = hashlib.sha256(encoded).digest()
    ripe = hashlib.new('ripemd160', sha).digest()
    return b58encode_check(b'\x00' + ripe)


def generateKeys(alias: str):
    keysStore = getKeysStore()

    #  check if there exists the same alias
    keys = getKeys(alias)
    if(any(keys)):
        print(f"The alias '{alias}' already exists!")
        return

    print(f"Generating an alias '{alias}' ...")
    """
        sk = secret_key
        pk = public_key
        pkh = public_key_hash = address
    """
    sk = SigningKey.generate(curve=SECP256k1)
    pk = sk.get_verifying_key()
    pkh = pkToPkh(pk.to_string().hex())

    # convert to human friendly
    keyPair = {
        'alias': alias,
        'sk': sk.to_string().hex(),
        'pk': pk.to_string().hex(),
        'pkh': pkh.decode()
    }

    keysStore.append(keyPair)

    with open(KEYS_PATH, 'w') as keys_file:
        json.dump(keysStore, keys_file, indent=2)

    return keyPair


def signTransaction(sk: str, txHash: str) -> str:
    sk = bytes.fromhex(sk)
    sk = SigningKey.from_string(sk, curve=SECP256k1)
    signature = sk.sign(bytes.fromhex(txHash))
    return signature.hex()


def verifyTxSignature(txHash: str, signature: str, pk: str) -> bool:
    try:
        pk = bytes.fromhex(pk)
        pk = VerifyingKey.from_string(pk, curve=SECP256k1)
        pk.verify(bytes.fromhex(signature), bytes.fromhex(txHash))
        return True
    except BaseException:
        return False


def verifyPkh(pkh: str) -> bool:
    # checksum = b58decode(pkh).hex()[-8:]
    # payload = b58decode_check(pkh)
    # localChecksum = sha256d(payload)[:8]
    # return checksum == localChecksum
    try:
        b58decode_check(pkh)
        return True
    except BaseException:
        return False


def test():
    keys = [
        {
            "alias": "ada",
            "sk": "fc487a5adcb6fe82ac8de12f2c6cffa2b395bae0b694591c1a9ef973552e4030",
            "pk": "c621e37b2be6e83ce77b539a90f6fc99a218986499a5b7565283eb9ec369f5c08f527af268fa9a274613804f8773b042e1866a84c705ddc18bb6f05598d7456a",
            "pkh": "1G8RdTC6nSmuLVkBzkWEaWzqqsqM8f98cU"
        },
        {
            "alias": "ada2",
            "sk": "41b141e91e322881426fb36d1c7249248203265233966985526b4b210ae0bc61",
            "pk": "adf1d1c5664bbf34319f3b5d116cd0a27c3cfe02aa401cf551b7c44eea1c74e6e9b037a54c43440bb8b60e40a1a08e618be0fd8a3f0db178ef6007fecb754296",
            "pkh": "1Lnwdifen3szZbG1srBwBBYA3gvVaBtXaC"
        }
    ]

    testTx = {
        'txId': '7f1058266c8326acf223bc8ed79eca6960b792601ae22956024376e3bdcf72dd',
        'txIns': [
            {
                'txOutId':
                'da2f1e82a300e75433bf416b0765aa29b3129bf68bed3a22f1d163c24c8dbffc',
                'txOutIdx': 0,
            },
            {
                'txOutId':
                'f25cd44a098a0f9622ade2eb7be315b7cf86d23efc7131543cc57e1f61818e91',
                'txOutIdx': 0,
            },
            {
                'txOutId':
                '1bf86b22ce8a58469d90111f1967675b925ab3dcbbdf5b016ec4d68953697b1b',
                'txOutIdx': 0,
            },
            {
                'txOutId':
                '933a8f94ef9c69a87fd2f35a558cae28f84c439c08e2b74423d90b8e81d567b7',
                'txOutIdx': 0,
            },
        ],
        'txOuts': [
            {
                'address': '1LpUToTfVj6LVkwpyUnrFEXr3sNcdtRPkX',
                'amount': '153',
            },
            {
                'address': '1LpUToTfVj6LVkwpyUnrFEXr3sNcdtRPkX',
                'amount': 47,
            },
        ],
        'signature': '',
        'pk': ''
    }

    signature = signTransaction(
        keys[0]['sk'],
        testTx['txId'])

    verified = verifyTxSignature(
        testTx['txId'],
        signature,
        keys[0]['pk'])

    print(verified)

    verified = verifyTxSignature(
        testTx['txId'],
        signature,
        keys[1]['pk'])

    print(verified)


if __name__ == "__main__":
    test()
