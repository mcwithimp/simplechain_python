from customTypes.utxo import UTxO
from customTypes.block import Block

UTxOContext = []


def updateUTxOContext(blockLevel, block: Block):
    # 가장 최근의 UTxOContext를 가져온다.
    utxoContext = UTxOContext if len(UTxOContext) else {}

    transactions = block.transactions
    for tx in transactions:
        for txOutIdx, txOut in enumerate(tx.txOuts):
            utxo = UTxO(
                txOutId=tx.txId,
                txOutIdx=txOutIdx,
                address=txOut.address,
                amount=txOut.amount
            )

            utxoContext["tx.txId_{idx}".format(idx=txOutIdx)] = utxo

    UTxOContext.append(utxoContext)
    # UTxOContext[blockLevel] = utxoContext
