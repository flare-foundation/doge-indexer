# Indexer specifications

The indexer is used to store data from the Dogecoin blockchain, namely confirmed (60 confirmations) blocks and included transactions from the prescribed period (2 days).
One of the downsides of the Dogecoin node api is lack of data about inputs of the transaction. Queries about the transaction do not return addresses and values of the input transactions, only a reference an output.
This indexer in addition stores the data about the inputs.

Given a transaction from a confirmed block from the prescribed period the indexer provides the data that is needed for the state connector protocol for attestation types

- Payment
- BalanceDecreasingTransaction
- ReferenceTransactionNonexistence

For these types, the indexer stores and efficiently fetches all the transactions from the confirmed blocks from the given time range needed to calculate the PaymentSummary and BalanceDecreasingSummary.
In addition transactions with a defined standardPaymentReference are also indexed to support ReferenceTransactionNonexistence type.

Given a transactionId the indexer can efficiently provide the following data.

- transactionId (txid)
- blockNumber
- blockTimestamp
- standardPaymentReference (defined here)
- data about the transaction inputs
  - input index
  - address of the input
  - values of the input
- data about the transaction outputs
  - output index
  - address of the output
  - value of the output
