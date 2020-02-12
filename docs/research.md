# Research

This file includes the research done by our group.

## 02/09/2020 by Tiger Yu

### Merkle Trees in different cryptocurrencies

Goal of research: get a more in-depth understanding of the structure of Merkle trees in various cryptocurrencies. 

The Merkle Tree is also called Hash Tree in which each leaf node is a cryptographic hash digest of a data item (ex. transactions), and each non-leaf node is a hash digest of its children. So the root of the tree is the digest of the whole dataset. Merkle trees are used to calculate the digest of a large set of data, which is the basic building block in cryptocurrency and other blockchain systems. They are used to lock a set of transactions in a block, or record the states of the chain, and also can efficiently perform secure verification of content.


This research will do an in-depth analysis of Merkle Trees in cryptocurrencies, including Bitcoin, Ethereum, Libra, Ripple, and compile a report of the pros and cons of each system. For this project, we will come up with a new way to construct Merkle Tree more efficiently. We will create a simple cryptocurrency and our method of creating a Merkle tree.

#### ![Bitcoin logo]Bitcoin
double-sha-256 hash, to avoid “length extension attack”

##### Links
[Length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack)
[Merkle trees](https://en.bitcoin.it/wiki/Protocol_documentation#Merkle_Trees)

handling an odd number of items: duplicate the last item

#### [![Etherum Logo]Ethereum](https://blog.ethereum.org/2015/11/15/merkling-in-ethereum/)


Ethereum uses MPT (MPT  Merkle Patricia Tree) to calculate: 
- the state root: the hash root of the global state.
- the tx root: the hash root of all the transactions of a block
- the receipt root: the hash root of all the receipt and log of all transactions of a block

##### Links

[Block creation](https://github.com/ethereum/go-ethereum/blob/b6d4f6b66e99c08f419e6a469259cbde1c8b0582/core/types/block.go#L209)

[Derive sha](https://github.com/ethereum/go-ethereum/blob/461291882edce0ac4a28f64c4e8725b7f57cbeae/core/types/derive_sha.go#L32)

#### [Libra](https://developers.libra.org/docs/crates/storage)

Libra uses a novel Merkle accumulator to record transactions.

#### Ripple:  Not studied yet

<!-- Reference links -->
[Bitcoin Logo]: pictures/BC_Logo_32x32.png "Bitcoin"
[Etherum Logo]: pictures/etherum_32x32.png "Etherum"
